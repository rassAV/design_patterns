import connexion
from flask import jsonify, Response, request
from src.core.object_types import format_reporting
from src.storage_reposity import storage_reposity
from src.reports.report_factory import report_factory
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.logics.prototype_manager import prototype_manager
from src.dto.filter import filter
from src.processes.process_manager import process_manager
from src.processes.turnover_process import turnover_process
from src.processes.dateblock_process import dateblock_process
from src.processes.balance_process import balance_process
from src.file_manager import file_manager
from src.logics.observe_service import observe_service
from src.core.object_types import event_type
from src.core.object_types import log_type
from src.logics.nomenclature_service import nomenclature_service
from src.log_manager import log_manager

app = connexion.FlaskApp(__name__, specification_dir='./')

data_mapping = {
    'ranges': storage_reposity.ranges_key(),
    'groups': storage_reposity.groups_key(),
    'nomenclature': storage_reposity.nomenclature_key(),
    'receipts': storage_reposity.receipts_key()
}

manager = settings_manager()
manager.open("settings2.json", "../")
reposity = storage_reposity()
start = start_service(reposity, manager)
nmcl_service = nomenclature_service(reposity)
start.create()

processes = process_manager()
processes.register('turnover', turnover_process)
processes.register('dateblock', dateblock_process)
processes.register('balance', balance_process)

report = report_factory().create(manager)
file = file_manager()
logs = log_manager(manager)

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    try:
        result = [{"name": item.name, "value": item.value} for item in format_reporting]
        observe_service.raise_event(event_type.FORMATS, logs, {"log_level": log_type.INFO, "message": "GET formats successfully completed"})
    except:
        observe_service.raise_event(event_type.FORMATS, logs, {"log_level": log_type.ERROR, "message": "GET formats can not completed"})
    return jsonify(result)

@app.route("/api/reports/<category>/<format_type>", methods=["GET"])
def get_report(category, format_type):
    if category not in data_mapping:
        return jsonify({"error": "Invalid category"}), 400

    try:
        manager.settings.report_format = format_reporting[format_type.upper()]
    except KeyError:
        return jsonify({"error": "Invalid report format"}), 400

    report.create(reposity.data[data_mapping[category]])

    return Response(report.result, status=200)

@app.route("/api/filter/<category>", methods=["POST"])
def filter_data(category):
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    if category not in data_mapping:
        return jsonify({"error": "Invalid category"}), 400
    
    data = reposity.data[data_mapping[category]]
    filt = filter.from_dict(request.get_json())
    prototype = prototype_manager(data)
    report.create(prototype.create(data, filt).data)

    return Response(report.result, status=200)

@app.route("/api/transactions", methods=["POST"])
def transactions():
    data = start.data["transactions"]

    if not data:
        return jsonify({"error": "No transactions found"}), 404

    report.create(data)
    return report.result

@app.route("/api/turnover", methods=["POST"])
def turnover():
    data = start.data["transactions"]

    if not data:
        return jsonify({"error": "No transactions found"}), 404

    turnover = processes.get('turnover')
    turnover_data = turnover.process(data)

    if not turnover_data:
        return jsonify({"error": "No turnovers found"}), 404

    report.create(turnover_data)
    return report.result

@app.route("/api/dateblock", methods=["POST"])
def dateblock():
    data = start.data["transactions"]

    if not data:
        return jsonify({"error": "No transactions found"}), 404

    dateblock = processes.get('dateblock')
    state = dateblock.process(data)

    if not state:
        return jsonify({"error": "Dateblock error"}), 404
    return jsonify({"datablock_state": state}), 200

@app.route("/api/dateblock", methods=["GET"])
def get_dateblock():
    try:
        data = file.json_read("../data/turnovers", "blocked_turnovers.json")
    except:
        return jsonify({"error": "Dateblock file not found"}), 404
    return jsonify({"datablock": data['date']}), 200

@app.route('/api/nomenclature', methods=['GET'])
def get_nomenclature():
    result = nmcl_service.get_nomenclature(request.args)
    if "error" in result:
        return jsonify(result), 404
    report.create(list(result))
    return Response(report.result, status=200)

@app.route('/api/nomenclature', methods=['PUT'])
def add_nomenclature():
    result = nmcl_service.add_nomenclature(request.args)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/nomenclature', methods=['PATCH'])
def update_nomenclature():
    result = observe_service.raise_event(event_type.UPDATE_NOMENCLATURE, request.json)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/nomenclature', methods=['DELETE'])
def delete_nomenclature():
    result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request.json)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/balance_list', methods=['GET'])
def get_balance_list():
    data = start.data["transactions"]
    if not data:
        return jsonify({"error": "No transactions found"}), 404
    balance = processes.get('balance')
    balance_list = balance.process(data)
    if not balance_list:
        return jsonify({"error": "No balance list found"}), 404
    return jsonify(balance_list), 200

@app.route('/api/data/save', methods=['POST'])
def save_data():
    result = start.save()
    if not result:
        return jsonify({"error": "Data not save"}), 500
    return jsonify({"status": "Data successfully saved"}), 200

@app.route('/api/data/load', methods=['POST'])
def load_data():
    result = start.load()
    if not result:
        return jsonify({"error": "Data not load"}), 500
    return jsonify({"status": "Data successfully loaded"}), 200

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(host="0.0.0.0", port=8080)