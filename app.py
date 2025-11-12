import os
from flask import Flask
from dotenv import load_dotenv
from routes.auth import auth_bp
from routes.devices import devices_bp

load_dotenv()

app = Flask(__name__)
PORT = os.getenv("PORT", 5000)


app.register_blueprint(auth_bp)
app.register_blueprint(devices_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
