from flask import Flask, request, jsonify
from transformers import pipeline
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time


app = Flask(__name__)

qa = pipeline(
    task="question-answering",
    model="deepset/roberta-base-squad2",
    tokenizer="deepset/roberta-base-squad2",
)
# Prometheus metrics
REQUEST_COUNT = Counter(
    "qa_requests_total", "Total number of /predict requests"
)
REQUEST_LATENCY = Histogram(
    "qa_request_latency_seconds", "Latency of /predict requests"
)

@app.route("/predict", methods=["POST"])
def predict():
    start = time.time()

    data = request.get_json(force=True)
    context = data.get("context", "")
    question = data.get("question", "")
    if not context or not question:
        return jsonify({"error": "Both 'context' and 'question' are required."}), 400

    result = qa(question=question, context=context)

    # update metrics
    REQUEST_COUNT.inc()
    REQUEST_LATENCY.observe(time.time() - start)

    return jsonify(result)

@app.route("/metrics")
def metrics():
    """Prometheus scrape endpoint."""
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(debug=True)
