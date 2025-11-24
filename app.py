import os
from flask import Flask
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.devices import devices_bp
import logging

load_dotenv()

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
handler.setFormatter(formatter)

app.logger.addHandler(handler)

app.logger.info("Logging is enabled!")

PORT = os.getenv("PORT", 5000)


# Register blueprints with /api prefix
app.register_blueprint(auth_bp, url_prefix="/api")
app.register_blueprint(devices_bp, url_prefix="/go")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
