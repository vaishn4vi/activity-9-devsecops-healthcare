from flask import Flask, jsonify, render_template
from datetime import datetime, timezone
import os

app = Flask(__name__)
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
ENVIRONMENT = os.getenv("APP_ENV", "development")
# Fictional aggregate demo data only. Never use real patient information.
SUMMARY = {"patients": 1284, "appointments": 46, "beds_available": 18, "alerts": 3}
ACTIVITY = [
    {"time": "09:42 AM", "title": "Lab results uploaded", "detail": "Demo patient · Record #PT-1048", "kind": "lab"},
    {"time": "09:18 AM", "title": "Appointment confirmed", "detail": "Cardiology · Demo patient", "kind": "appointment"},
    {"time": "08:56 AM", "title": "Access review completed", "detail": "Staff permissions checked", "kind": "security"},
    {"time": "08:30 AM", "title": "Backup verification passed", "detail": "Encrypted backup · 100% verified", "kind": "backup"},
]

@app.route("/")
def index():
    return render_template("index.html", summary=SUMMARY, activity=ACTIVITY,
                           app_version=APP_VERSION, environment=ENVIRONMENT)

@app.route("/health")
def health():
    return jsonify(status="healthy", service="careguard-health", version=APP_VERSION,
                   timestamp=datetime.now(timezone.utc).isoformat())

@app.route("/api/summary")
def api_summary():
    return jsonify(SUMMARY)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
