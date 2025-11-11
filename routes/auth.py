import os

from flask import Blueprint, redirect, request, jsonify
from services.auth_service import build_authorization_url, exchange_code_for_token

auth_bp = Blueprint("auth", __name__)
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")


@auth_bp.route("/auth/login", methods=["GET"])
def login():
    """Return the Auth0 authorization URL so the frontend can redirect."""
    url = build_authorization_url()
    return jsonify({"authorization_url": url})


@auth_bp.route("/auth/callback")
def callback():
    """Handle redirect from Auth0 after user login."""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Missing authorization code"}), 400

    try:
        _ = exchange_code_for_token(code)
        # return jsonify({
        #     "message": "Authentication successful",
        #     "tokens": tokens
        # })
        return redirect(f"{frontend_url}/zf?auth=success")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
