import connexion
from flask import jsonify, Response, request
from src.core.format_reporting import format_reporting
from src.storage_reposity import storage_reposity
from src.reports.report_factory import report_factory
from src.settings_manager import settings_manager
from src.start_service import start_service
from src.logics.prototype_manager import prototype_manager
from src.dto.filter import filter

app = connexion.FlaskApp(__name__, specification_dir='./')

data_mapping = {
    'ranges': storage_reposity.ranges_key(),
    'groups': storage_reposity.groups_key(),
    'nomenclature': storage_reposity.nomenclature_key(),
    'receipts': storage_reposity.receipts_key()
}

@app.route("/api/reports/formats", methods=["GET"])
def formats():
    return jsonify([{"name": item.name, "value": item.value} for item in format_reporting])

@app.route("/api/reports/<category>/<format_type>", methods=["GET"])
def get_report(category, format_type):
    manager = settings_manager()
    manager.open("settings2.json", "../")
    reposity = storage_reposity()

    if category not in data_mapping:
        return jsonify({"error": "Invalid category"}), 400

    try:
        report_format = format_reporting[format_type.upper()]
    except KeyError:
        return jsonify({"error": "Invalid report format"}), 400
    
    manager.settings.report_format = report_format
    start = start_service(reposity, manager)
    start.create()

    report = report_factory().create(manager)
    report.create(reposity.data[data_mapping[category]])

    return Response(report.result, status=200)

@app.route("/api/filter/<category>", methods=["POST"])
def filter_data(category):
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415
    
    manager = settings_manager()
    manager.open("settings2.json", "../")
    reposity = storage_reposity()

    if category not in data_mapping:
        return jsonify({"error": "Invalid category"}), 400
    
    manager.settings.report_format = format_reporting.JSON
    start = start_service(reposity, manager)
    start.create()
    data = reposity.data[data_mapping[category]]
    filt = filter.from_dict(request.get_json())
    prototype = prototype_manager(data)
    report = report_factory().create(manager)
    report.create(prototype.create(data, filt).data)

    return Response(report.result, status=200)

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)