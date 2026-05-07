from flask import Flask, request
from google.cloud import pubsub_v1
import json, os

app = Flask(__name__)
publisher = pubsub_v1.PublisherClient()
PROJECT_ID = os.environ.get("PROJECT_ID", "your-project-id")
TOPIC_PATH = publisher.topic_path(PROJECT_ID, "vote-topic")

@app.route("/", methods=["GET"])
def index():
    return {"status": "Voting API is running!", "endpoint": "/vote"}, 200

@app.route("/vote", methods=["POST"])
def receive_vote():
    vote = request.get_json()
    if not vote or not all(k in vote for k in ["user_id", "poll_id", "choice"]):
        return {"error": "Invalid payload"}, 400
    try:
        data = json.dumps(vote).encode("utf-8")
        publisher.publish(TOPIC_PATH, data)
        return {"status": "accepted"}, 200
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)