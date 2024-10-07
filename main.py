import connexion
from flask import jsonify
from flask import Response
from src.core.format_reporting import format_reporting
from src.storage_reposity import storage_reposity
from src.reports.report_factory import report_factory
from src.settings_manager import settings_manager
from src.start_service import start_service

app = connexion.FlaskApp(__name__, specification_dir='./')

def formats():
    return jsonify([{"name": item.name, "value": item.value} for item in format_reporting])

@app.route("/api/reports/<category>/<format_type>", methods=["GET"])
def get_report(category, format_type):
    manager = settings_manager()
    manager.open("settings2.json", "../")
    reposity = storage_reposity()

    data_mapping = {
        'range': storage_reposity.ranges_key(),
        'group': storage_reposity.groups_key(),
        'nomenclature': storage_reposity.nomenclature_key(),
        'receipts': storage_reposity.receipts_key()
    }

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

    content_type = "application/json"
    if report_format == format_reporting.CSV:
        content_type = "text/csv"
    elif report_format == format_reporting.MD:
        content_type = "text/markdown"
    elif report_format == format_reporting.XML:
        content_type = "application/xml"
    elif report_format == format_reporting.DOCX:
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif report_format == format_reporting.XLSX:
        content_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    return Response(report.result, content_type=content_type, status=200)

if __name__ == '__main__':
    app.add_api("swagger.yaml")
    app.run(port=8080)