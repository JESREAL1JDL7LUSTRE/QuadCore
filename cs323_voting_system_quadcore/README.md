\# Distributed Voting System on GCP

## System Overview and Architecture
This project implements a distributed voting pipeline with these components:

- **Edge nodes** generate votes and send them to a Cloud Run API endpoint.
- **Cloud Run API (Flask)** validates incoming votes and publishes them to Pub/Sub topic `vote-topic`.
- **Pub/Sub** buffers votes and delivers them to a worker subscription `vote-sub`.
- **Worker service (Flask + subscriber)** consumes votes and writes them to Firestore collection `votes`.
- **Firestore** stores each vote document using a composite key `user_id_poll_id`.

High-level flow:
`Edge Node -> Cloud Run API -> Pub/Sub (vote-topic / vote-sub) -> Worker -> Firestore`

## Setup and Execution (GCP)
Use the steps below to deploy and run the system. Replace placeholders in ALL CAPS with your actual values.

1. **Create or select a GCP project**
	- Project ID: `YOUR_PROJECT_ID`

2. **Enable required APIs**
	- Cloud Run
	- Pub/Sub
	- Firestore
	- Cloud Build (if building via gcloud)

3. **Create Pub/Sub resources**
	- Topic: `vote-topic`
	- Subscription: `vote-sub` (attached to `vote-topic`)

4. **Create Firestore database**
	- Mode: Native
	- Location: choose a region close to Cloud Run

5. **Deploy the Cloud Run API service** (folder: `api/`)
	- Set environment variable `PROJECT_ID=YOUR_PROJECT_ID`
	- Expose HTTP POST endpoint `/vote`
	- Ensure the service account can publish to Pub/Sub

6. **Deploy the Cloud Run worker service** (folder: `worker/`)
	- Set environment variable `PROJECT_ID=YOUR_PROJECT_ID`
	- Ensure the service account can subscribe to Pub/Sub and write to Firestore
	- The worker listens to subscription `vote-sub` and writes to Firestore

7. **Run edge node(s) locally** (folder: `edge/`)
	- Update `API_URL` in `edge/edge_node.py` with your Cloud Run API URL
	- Run: `python edge/edge_node.py`
	- If you have multiple edge nodes, change `edge_id` in `generate_vote()`

8. **Verify data in Firestore**
	- Collection: `votes`
	- Documents should appear as the worker processes messages

## Reflection and Analysis
Bea Clarise E. Bacaling

During the implementation of the distributed voting system, I was primarily involved in setting up the GCP infrastructure and deploying the Cloud Run services. The most challenging part I personally encountered was the IAM permission errors during deployment, where the default compute service account lacked the necessary roles for Cloud Build and Storage, requiring us to manually bind each role through the terminal before the API would successfully deploy. Once the pipeline was running, I observed that the edge node consistently received HTTP 200 responses and votes appeared in Firestore within a few seconds, which made the end-to-end flow feel seamless despite the number of moving parts involved. What struck me most was how Pub/Sub acted as a safety net — even when the worker was temporarily unavailable due to the missing health check endpoint, no messages were lost and processing resumed automatically once the service was restored, which demonstrated the real value of decoupled asynchronous communication in distributed systems.

Jesreal D. Lustre

My role in the activity focused on implementing the edge node script and observing how vote data traveled through the pipeline during testing. Running the edge node locally while watching the Firestore console update in real time was the clearest moment where the distributed nature of the system became tangible — votes I generated on my machine were appearing in a cloud database within seconds without any direct connection between the two. I also noticed that when we intentionally sent duplicate votes to simulate retry behavior, Firestore never stored more than one document per user per poll because the document ID was constructed from the combination of user_id and poll_id, which enforced idempotency automatically. Compared to a simple sequential local script where everything runs in order and errors are immediately visible, the distributed setup made debugging significantly harder since a failure in one layer did not produce an obvious error in another, and tracing a single vote required checking multiple GCP dashboards simultaneously.

Gil John Rey Naldoza

Working on the worker service gave me a firsthand understanding of how asynchronous processing behaves in a cloud environment and how differently it feels from writing a simple local script. The most frustrating issue I encountered was the repeated deployment failure caused by Cloud Run's health check timing out because our worker had no HTTP endpoint — the container would start, pass the build stage, and then fail silently during revision creation until we added a Flask route running on a background thread to satisfy the health check requirement. After resolving this, I observed that the worker immediately began draining the messages that had queued in Pub/Sub during the failed deployment attempts, processing them in batches without any manual intervention, which was a clear demonstration of how message persistence enables automatic recovery in distributed systems. This experience changed how I think about fault tolerance — it is not just about preventing failures but designing systems that recover gracefully when failures inevitably occur.

Angel Janette Taglucop

My contribution involved testing the fault injection scenarios and documenting the system behavior under failure conditions, particularly observing what happened when the worker service was scaled down to zero instances while the edge nodes continued sending votes. During this period, the Cloud Run API kept accepting requests and returning success responses, Pub/Sub continued buffering the incoming messages, and Firestore simply stopped updating — but critically, no data was lost and no part of the system crashed entirely, which illustrated how distributed architectures isolate failures to individual components rather than bringing everything down at once. When the worker was restored by redeploying with minimum instances set back to one, it automatically reconnected to the subscription and processed all queued messages without any manual replay logic required. The entire experience highlighted a key trade-off I had not fully appreciated before: distribution significantly improves reliability and scalability but introduces communication overhead, configuration complexity, and debugging difficulty that would simply not exist in a straightforward monolithic application.