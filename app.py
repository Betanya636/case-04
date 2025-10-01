from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from pydantic import ValidationError
from models import SurveySubmission, StoredSurveyRecord
from storage import append_json_line
import hashlib

def hash_value(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()

def generate_submission_id(email_hash: str) -> str:
    now = datetime.now().strftime("%Y%m%d%H")
    return hash_value(email_hash + now)

app = Flask(__name__)
# Allow cross-origin requests so the static HTML can POST from localhost or file://
CORS(app, resources={r"/v1/*": {"origins": "*"}})

@app.route("/ping", methods=["GET"])
def ping():
    """Simple health check endpoint."""
    return jsonify({
        "status": "ok",
        "message": "API is alive",
        "utc_time": datetime.now(timezone.utc).isoformat()
    })

@app.post("/v1/survey")
def submit_survey():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "invalid_json", "detail": "Body must be application/json"}), 400

    try:
        submission = SurveySubmission(**payload)
    except ValidationError as ve:
        return jsonify({"error": "validation_error", "detail": ve.errors()}), 422

    submission_dict = submission.dict()

    submission_dict["email"] = hash_value(submission_dict["email"])
    submission_dict["age"] = hash_value(str(submission_dict["age"]))

    if submission_dict.get("submission_id"):
        submission_id = submission_dict["submission_id"]  
    else:
        submission_id = generate_submission_id(submission_dict["email"])  
    submission_dict["submission_id"] = submission_id

    record = StoredSurveyRecord(
        **submission.dict(),
        received_at=datetime.now(timezone.utc),
        ip=request.headers.get("X-Forwarded-For", request.remote_addr or "")
    )
    append_json_line(record.dict())
    return jsonify({"status": "ok"}), 201

if __name__ == "__main__":
    app.run(port=5000, debug=True)
