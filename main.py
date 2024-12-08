import connexion
from flask import jsonify, Response, request
import psycopg2
import os
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

DB_CONN = os.getenv("DB_CONNECTION", f"dbname={start.settings.db_name} user={start.settings.db_user} password={start.settings.db_password} host=localhost port=5432")

def connect_db():
    return psycopg2.connect(DB_CONN)

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    try:
        result = [{"name": item.name, "value": item.value} for item in format_reporting]
        observe_service.raise_event(event_type.FORMATS, logs, {"status": "GET formats successfully completed"})
    except:
        observe_service.raise_event(event_type.FORMATS, logs, {"error": "GET formats can not completed"})
    return jsonify(result)

@app.route("/api/reports/<category>/<format_type>", methods=["GET"])
def get_report(category, format_type):
    if category not in data_mapping:
        observe_service.raise_event(event_type.GET_REPORT, logs, {"error": "Invalid category"})
        return jsonify({"error": "Invalid category"}), 400

    try:
        manager.settings.report_format = format_reporting[format_type.upper()]
    except KeyError:
        observe_service.raise_event(event_type.GET_REPORT, logs, {"error": "Invalid report format"})
        return jsonify({"error": "Invalid report format"}), 400

    report.create(reposity.data[data_mapping[category]])
    observe_service.raise_event(event_type.GET_REPORT, logs, {"status": "GET get_report successfully completed"})
    return Response(report.result, status=200)

@app.route("/api/crud/filter/<category>", methods=["POST"])
def filter_data(category):
    if request.content_type != 'application/json':
        observe_service.raise_event(event_type.FILTER_DATA, logs, {"error": "Content-Type must be application/json"})
        return jsonify({"error": "Content-Type must be application/json"}), 415

    if category not in data_mapping:
        observe_service.raise_event(event_type.FILTER_DATA, logs, {"error": "Invalid category"})
        return jsonify({"error": "Invalid category"}), 400
    
    data = reposity.data[data_mapping[category]]
    filt = filter.from_dict(request.get_json())
    prototype = prototype_manager(data)
    report.create(prototype.create(data, filt).data)

    observe_service.raise_event(event_type.FILTER_DATA, logs, {"status": "POST filter_data successfully completed"})
    return Response(report.result, status=200)

@app.route("/api/crud/transactions", methods=["POST"])
def transactions():
    data = start.data["transactions"]

    if not data:
        observe_service.raise_event(event_type.TRANSACTIONS, logs, {"error": "No transactions found"})
        return jsonify({"error": "No transactions found"}), 404

    report.create(data)
    observe_service.raise_event(event_type.TRANSACTIONS, logs, {"status": "POST transactions successfully completed"})
    return report.result

@app.route("/api/crud/turnover", methods=["POST"])
def turnover():
    data = start.data["transactions"]

    if not data:
        observe_service.raise_event(event_type.TURNOVER, logs, {"error": "No transactions found"})
        return jsonify({"error": "No transactions found"}), 404

    turnover = processes.get('turnover')
    turnover_data = turnover.process(data)

    if not turnover_data:
        observe_service.raise_event(event_type.TURNOVER, logs, {"error": "No turnovers found"})
        return jsonify({"error": "No turnovers found"}), 404

    report.create(turnover_data)
    observe_service.raise_event(event_type.TURNOVER, logs, {"status": "POST turnover successfully completed"})
    return report.result

@app.route("/api/crud/dateblock", methods=["POST"])
def dateblock():
    data = start.data["transactions"]

    if not data:
        observe_service.raise_event(event_type.DATEBLOCK, logs, {"error": "No transactions found"})
        return jsonify({"error": "No transactions found"}), 404

    dateblock = processes.get('dateblock')
    state = dateblock.process(data)

    if not state:
        observe_service.raise_event(event_type.DATEBLOCK, logs, {"error": "Dateblock error"})
        return jsonify({"error": "Dateblock error"}), 404
    observe_service.raise_event(event_type.DATEBLOCK, logs, {"status": "POST dateblock successfully completed"})
    return jsonify({"datablock_state": state}), 200

@app.route("/api/reports/dateblock", methods=["GET"])
def get_dateblock():
    try:
        data = file.json_read("../data/turnovers", "blocked_turnovers.json")
    except:
        observe_service.raise_event(event_type.GET_DATEBLOCK, logs, {"error": "Dateblock file not found"})
        return jsonify({"error": "Dateblock file not found"}), 404
    observe_service.raise_event(event_type.GET_DATEBLOCK, logs, {"status": "GET get_dateblock successfully completed"})
    return jsonify({"datablock": data['date']}), 200

@app.route('/api/reports/nomenclature', methods=['GET'])
def get_nomenclature():
    result = nmcl_service.get_nomenclature(request.args)
    if "error" in result:
        observe_service.raise_event(event_type.GET_NOMENCLATURE, logs, result)
        return jsonify(result), 404
    report.create(list(result))
    observe_service.raise_event(event_type.GET_NOMENCLATURE, logs, {"status": "GET get_nomenclature successfully completed"})
    return Response(report.result, status=200)

@app.route('/api/crud/nomenclature', methods=['PUT'])
def add_nomenclature():
    result = nmcl_service.add_nomenclature(request.args)
    observe_service.raise_event(event_type.ADD_NOMENCLATURE, logs, result)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/crud/nomenclature', methods=['PATCH'])
def update_nomenclature():
    result = observe_service.raise_event(event_type.UPDATE_NOMENCLATURE, request.json)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/crud/nomenclature', methods=['DELETE'])
def delete_nomenclature():
    result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, request.json)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/api/reports/balance_list', methods=['GET'])
def get_balance_list():
    data = start.data["transactions"]
    if not data:
        observe_service.raise_event(event_type.GET_BALANCE_LIST, logs, {"error": "No transactions found"})
        return jsonify({"error": "No transactions found"}), 404
    balance = processes.get('balance')
    balance_list = balance.process(data, request.args)
    if not balance_list:
        observe_service.raise_event(event_type.GET_BALANCE_LIST, logs, {"error": "No balance list found"})
        return jsonify({"error": "No balance list found"}), 404
    observe_service.raise_event(event_type.GET_BALANCE_LIST, logs, {"status": "GET get_balance_list successfully completed"})
    return jsonify(balance_list), 200

@app.route('/api/crud/save_data', methods=['POST'])
def save_data():
    result = start.save()
    if not result:
        observe_service.raise_event(event_type.SAVE_DATA, logs, {"error": "Data not save"})
        return jsonify({"error": "Data not save"}), 500
    observe_service.raise_event(event_type.SAVE_DATA, logs, {"status": "POST save_data successfully completed"})
    return jsonify({"status": "Data successfully saved"}), 200

@app.route('/api/crud/load_data', methods=['POST'])
def load_data():
    result = start.load()
    if not result:
        observe_service.raise_event(event_type.LOAD_DATA, logs, {"error": "Data not load"})
        return jsonify({"error": "Data not load"}), 500
    observe_service.raise_event(event_type.LOAD_DATA, logs, {"status": "POST load_data successfully completed"})
    return jsonify({"status": "Data successfully loaded"}), 200

@app.route('/api/crud/db_save', methods=['POST'])
def db_save():
    result = start.save()
    if not result:
        observe_service.raise_event(event_type.SAVE_DATA, logs, {"error": "Data not getting"})
        return jsonify({"error": "Data not save"}), 500
    try:
        with connect_db() as conn:
            pass
        observe_service.raise_event(event_type.SAVE_DATA, logs, {"status": "POST save_data successfully completed"})
    except:
        observe_service.raise_event(event_type.SAVE_DATA, logs, {"error": "Data not save in database"})
    return jsonify({"status": "Data successfully saved"}), 200

@app.route('/api/crud/db_load', methods=['POST'])
def db_load():
    try:
        with connect_db() as conn:
            data = []
        start.data = data
        observe_service.raise_event(event_type.LOAD_DATA, logs, {"status": "POST load_data successfully completed"})
    except:
        observe_service.raise_event(event_type.LOAD_DATA, logs, {"error": "Data not load in database"})
    return jsonify({"status": "Data successfully loaded"}), 200

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(host="0.0.0.0", port=8080)