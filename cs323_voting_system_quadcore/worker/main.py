from google.cloud import pubsub_v1, firestore
import json, os, time, threading
from flask import Flask

app = Flask(__name__)
PROJECT_ID = os.environ.get("PROJECT_ID", "cs323-voting-system-lustre")
SUBSCRIPTION_PATH = f"projects/{PROJECT_ID}/subscriptions/vote-sub"

db = firestore.Client()
subscriber = pubsub_v1.SubscriberClient()

def process_vote(message):
    try:
        vote = json.loads(message.data.decode("utf-8"))
        doc_id = f"{vote['user_id']}_{vote['poll_id']}"
        db.collection("votes").document(doc_id).set(vote)
        print(f"Processed: {vote['user_id']} | Choice: {vote['choice']} | Time: {time.time()}")
        message.ack()
    except Exception as e:
        print(f"Error: {e}")

def run_subscriber():
    streaming_pull = subscriber.subscribe(SUBSCRIPTION_PATH, callback=process_vote)
    print("Worker listening for votes...")
    with subscriber:
        try:
            streaming_pull.result()
        except Exception as e:
            streaming_pull.cancel()
            print(f"Worker stopped: {e}")

# Health check endpoint for Cloud Run
@app.route("/", methods=["GET"])
def health():
    return {"status": "ok"}, 200

if __name__ == "__main__":
    # Run subscriber in background thread
    thread = threading.Thread(target=run_subscriber, daemon=True)
    thread.start()
    # Run Flask for health checks
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)