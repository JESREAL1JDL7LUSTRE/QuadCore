import requests, uuid, random, time

API_URL = "https://voting-api-607060113730.asia-southeast1.run.app/vote"

def generate_vote():
    return {
        "user_id": str(uuid.uuid4()),
        "poll_id": "poll_1",
        "choice": random.choice(["A", "B", "C"]),
        "timestamp": time.time(),
        "edge_id": "node_1"   # change per member: node_1, node_2, etc.
    }

def send_vote(vote, retries=3):
    for attempt in range(retries):
        try:
            r = requests.post(API_URL, json=vote, timeout=5)
            print(f"Vote sent: {vote['user_id']} | Choice: {vote['choice']} | Status: {r.status_code}")
            return
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(1)

def run_edge_node():
    while True:
        vote = generate_vote()
        send_vote(vote)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_edge_node()