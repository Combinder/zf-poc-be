from flask import Blueprint, jsonify, request
from services.device_service import fetch_device_readings, fetch_spaces, fetch_space_devices, fetch_spaces_with_devices

devices_bp = Blueprint("devices", __name__)


@devices_bp.route("/devices/<device_id>/readings", methods=["GET"])
def get_device_readings(device_id):
    """Proxy endpoint to fetch readings for a given device."""
    start_time = request.args.get("startTime")
    end_time = request.args.get("endTime")
    resolution = request.args.get("resolution")
    measurement = request.args.get("measurement")

    missing = [p for p, v in {
        "startTime": start_time,
        "endTime": end_time,
        "resolution": resolution,
        "measurement": measurement,
    }.items() if not v]

    if missing:
        return jsonify({"error": f"Missing required query params: {', '.join(missing)}"}), 400

    data, error = fetch_device_readings(device_id, start_time, end_time, resolution, measurement)
    if error:
        return jsonify({"error": error}), 502

    return jsonify(data)

@devices_bp.route("/spaces", methods=["GET"])
def get_spaces():
    """Proxy endpoint to fetch user spaces, enriched with devices."""
    page = request.args.get("page", default=0, type=int)
    page_size = request.args.get("pageSize", default=100, type=int)

    data, error = fetch_spaces_with_devices(page=page, page_size=page_size)
    if error:
        return jsonify({"error": error}), 502

    return jsonify(data)


@devices_bp.route("/spaces/<space_id>/devices", methods=["GET"])
def get_space_devices(space_id):
    """Proxy endpoint to fetch devices within a space."""
    page = request.args.get("page", default=0, type=int)
    page_size = request.args.get("pageSize", default=100, type=int)

    data, error = fetch_space_devices(space_id, page=page, page_size=page_size)
    if error:
        return jsonify({"error": error}), 502

    return jsonify(data)

