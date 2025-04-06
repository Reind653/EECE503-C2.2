from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

qa = pipeline(
    task="question-answering",
    model="deepset/roberta-base-squad2",
    tokenizer="deepset/roberta-base-squad2",
)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)
    context = data.get("context", "")
    question = data.get("question", "")
    if not context or not question:
        return jsonify({"error": "Both 'context' and 'question' are required."}), 400

    result = qa(question=question, context=context)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
