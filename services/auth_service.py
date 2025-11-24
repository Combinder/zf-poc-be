import os
import time

import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

from flask import Blueprint, request, current_app

load_dotenv()

AUTH_DOMAIN = os.getenv("AUTH_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Temporary token store (in-memory, for demo)
_tokens = {}


def build_authorization_url():
    """Generate the URL to redirect the user to Auth0 for login."""
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email offline_access",
        "audience": "https://api.prod.zaehlerfreunde.com",
    }
    return f"{AUTH_DOMAIN}/authorize?{urlencode(params)}"


def exchange_code_for_token(code):
    current_app.logger.info(f"exchanging code for access_token: {code}")

    """Exchange authorization code for access + refresh tokens."""
    token_url = f"{AUTH_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    tokens = response.json()

    _tokens["access_token"] = tokens.get("access_token")
    _tokens["refresh_token"] = tokens.get("refresh_token")

    return tokens


# def get_access_token():
#     """Return a valid access token (refresh if needed)."""
#     token = _tokens.get("access_token")
#     if token:
#         return token
#
#     raise RuntimeError("No access token found — user must authenticate first.")
#
# import time

def get_access_token():
    """Return a valid access token (refresh if needed)."""
    access_token = _tokens.get("access_token")
    expires_in = _tokens.get("expires_in")
    issued_at = time.time()

    # If no token exists, user must authenticate first
    if not access_token:
        raise RuntimeError("No access token found — user must authenticate first.")

    # Check expiration (allow a small buffer, e.g., 60 seconds)
    if issued_at and expires_in:
        now = time.time()
        if now - issued_at >= expires_in - 60:
            # Token is expired or about to expire, refresh it
            print("Access token expired — refreshing...")
            new_token = refresh_access_token()
            _tokens["issued_at"] = time.time()
            return new_token

    # Token is still valid
    return access_token


def refresh_access_token():
    """Use refresh_token to get a new access_token."""
    if "refresh_token" not in _tokens:
        raise RuntimeError("No refresh token available to renew access.")

    token_url = f"{AUTH_DOMAIN}/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "refresh_token": _tokens["refresh_token"],
    }

    response = requests.post(token_url, json=payload)
    response.raise_for_status()
    new_data = response.json()

    _tokens["access_token"] = new_data.get("access_token")
    return _tokens["access_token"]