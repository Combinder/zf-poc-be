import os
import requests

from flask import Blueprint, request, current_app
from services.auth_service import get_access_token

BASE_URL = os.getenv("BASE_URL")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")


def fetch_spaces(page=0, page_size=100):
    """Handles external API call to fetch user spaces."""
    url = f"{BASE_URL}/spaces"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/json",
    }
    params = {
        "page": page,
        "pageSize": page_size,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        current_app.logger.info(f"fetched spaces {response.status_code}")
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def fetch_device_readings_v1(device_id, start_time, end_time, resolution, measurement):
    """Handles external API call to fetch device readings."""
    current_app.logger.info(f"about to fetch readings for device with id: {device_id}")
    current_app.logger.info(f"startTime: {start_time}")
    current_app.logger.info(f"endTime: {end_time}")
    current_app.logger.info(f"resolution: {resolution}")
    current_app.logger.info(f"measurement: {measurement}")
    url = f"{BASE_URL}/devices/{device_id}/readings"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/json",
    }
    params = {
        "startTime": start_time,
        "endTime": end_time,
        "resolution": resolution,
        "measurement": measurement,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def fetch_device_readings(device_id, start_time, end_time, resolution, measurement):
    """Handles external API call to fetch device readings."""

    current_app.logger.info(f"[readings] device_id={device_id}")
    current_app.logger.info(f"[readings] start={start_time}, end={end_time}, res={resolution}, m={measurement}")

    url = f"{BASE_URL}/devices/{device_id}/readings"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/json",
    }
    params = {
        "startTime": start_time,
        "endTime": end_time,
        "resolution": resolution,
        "measurement": measurement,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        current_app.logger.error("[readings] REQUEST FAILED", exc_info=True)

        try:
            current_app.logger.error(f"[readings] access_token startswith={headers['Authorization'][:15]}")
        except:
            pass

        return None, str(e)


def fetch_space_devices(space_id, page=0, page_size=100):
    """Fetch devices for a given space from the partner API."""
    url = f"{BASE_URL}/spaces/{space_id}/devices"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Accept": "application/json",
    }
    params = {
        "page": page,
        "pageSize": page_size,
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)


def fetch_spaces_with_devices(page=0, page_size=100):
    """Fetch spaces and include devices for each space."""
    spaces_data, error = fetch_spaces(page=page, page_size=page_size)
    if error:
        return None, error

    spaces = spaces_data.get("spaces", [])
    enriched_spaces = []

    for space in spaces:
        space_id = space.get("id")
        if not space_id:
            continue

        devices_data, device_error = fetch_space_devices(space_id)
        if device_error:
            # Add the error info but continue gracefully
            space["devices"] = []
            space["device_error"] = device_error
        else:
            space["devices"] = devices_data.get("devices", [])

        enriched_spaces.append(space)

    return {
        "spaces": enriched_spaces,
        "totalNumPages": spaces_data.get("totalNumPages"),
    }, None
