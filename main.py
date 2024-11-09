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
from src.file_manager import file_manager

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
start.create()

processes = process_manager()
processes.register('turnover', turnover_process)
processes.register('dateblock', dateblock_process)

file = file_manager()

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    return jsonify([{"name": item.name, "value": item.value} for item in format_reporting])

@app.route("/api/reports/<category>/<format_type>", methods=["GET"])
def get_report(category, format_type):
    if category not in data_mapping:
        return jsonify({"error": "Invalid category"}), 400

    try:
        manager.settings.report_format = format_reporting[format_type.upper()]
    except KeyError:
        return jsonify({"error": "Invalid report format"}), 400

    report = report_factory().create(manager)
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
    report = report_factory().create(manager)
    report.create(prototype.create(data, filt).data)

    return Response(report.result, status=200)

@app.route("/api/transactions", methods=["POST"])
def transactions():
    data = start.data["transactions"]

    if not data:
        return jsonify({"error": "No transactions found"}), 404

    report = report_factory().create(manager)
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

    report = report_factory().create(manager)
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

@app.route("/api/get_dateblock", methods=["GET"])
def get_dateblock():
    try:
        data = file.json_read("../data/turnovers", "blocked_turnovers.json")
    except:
        return jsonify({"error": "File not found"}), 404
    return jsonify({"datablock": data['date']}), 200

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)