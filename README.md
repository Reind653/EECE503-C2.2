# QA‑Flask‑API

A lightweight Question‑Answering micro‑service built with **Flask**, **Transformers**, and **Prometheus** metrics.
---

## Features

| Endpoint   | Method | Purpose                                                                            |
| ---------- | ------ | ---------------------------------------------------------------------------------- |
| `/predict` | POST   | Extractive QA – returns an answer span, confidence score, start & end offsets.     |
| `/metrics` | GET    | Prometheus‑compatible metrics (`qa_requests_total`, `qa_request_latency_seconds`).


## Architecture

```
┌──────────────┐    POST /predict    ┌────────────────────────────┐
│  Client (UI) │ ────────────────▶ │  Flask App (app.py)        │
└──────────────┘                    │  • Hugging Face pipeline   │
                                    │    – deepset/roberta‑squad │
┌──────────────┐    GET /metrics    │  • Prometheus metrics      │
│ Prometheus   │ ◀───────────────┤ │                          │
└──────────────┘                    └────────────────────────────┘
```



## Prerequisites

- **Python 3.9 +**  (3.10/3.11 work too)
- **pip** & **git**

## How to Start

### 1. Clone the repository

```bash
git clone https://github.com/Reind653/EECE503-C2.2
cd EECE503-C2.2
```

### 2. Create & activate a virtual environment

```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If you see *running scripts is disabled*, run PowerShell **as Administrator** once:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
```

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
# Windows cmd
set FLASK_APP=app.py
flask run

# PowerShell
$env:FLASK_APP="app.py"
flask run

# macOS / Linux
export FLASK_APP=app.py
flask run
```

Server listens on [**http://127.0.0.1:5000**](http://127.0.0.1:5000) by default.


## Testing

### POST `/predict`

```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{
           "context": "Marie Curie discovered radium in 1898.",
           "question": "Who discovered radium?"
         }'
```

Response:

```json
{
  "answer": "Marie Curie",
  "score": 0.95,
  "start": 0,
  "end": 11
}
```

### GET `/metrics`

Navigate to [**http://127.0.0.1:5000/metrics**](http://127.0.0.1:5000/metrics) and you’ll see Prometheus text exposition:

```
# HELP qa_requests_total Total number of /predict requests
# TYPE qa_requests_total counter
qa_requests_total 3.0
...
```

---

## Versioning & Tags
```bash
# tag current commit
git tag -a v2 -m "Add metrics endpoint"
# push to GitHub
git push origin v2
```



## License

This project is released for our EECE503N assignment.

