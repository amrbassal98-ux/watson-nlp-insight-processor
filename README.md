# Watson NLP Emotion Detection Service with Flask Microservice Architecture

A Python Flask web application that performs real-time emotion classification on user-submitted text using the IBM Watson NLP Emotion Predict API. Implements a token-driven NLP classification pipeline with structured error handling for blank inputs and upstream API failures.

---

## Architecture Overview

### NLP Classification Pipeline

```
User Input (text)
  |
  v
[Flask Route Handler]         -- /emotionDetector, query param extraction
  |
  v
[EmotionDetection Package]    -- emotion_detector() function
  |
  v
[Watson NLP REST API]         -- POST to sn-watson-emotion.labs.skills.network
  |
  v
[Response Parser]             -- JSON extraction, score aggregation
  |
  v
[Dominant Emotion Selector]   -- max() over anger/disgust/fear/joy/sadness
  |
  v
[Formatted String Response]   -- Structured output for frontend consumption
```

### Package Decomposition

```
EmotionDetection/
  __init__.py                 # Package marker
  emotion_detection.py        # Core NLP function: Watson API integration
server.py                     # Flask application, route definitions
test_emotion_detection.py     # Unit test suite (5 emotion scenarios)
templates/
  index.html                  # Web interface for text input
static/
  mywebscript.js              # Client-side AJAX call handler
```

### Watson NLP Integration Details

- **Endpoint**: `https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict`
- **Model Header**: `grpc-metadata-mm-model-id: emotion_aggregated-workflow_lang_en_stock`
- **Input Format**: `{ "raw_document": { "text": "..." } }`
- **Error Handling**: HTTP 400 returns all-null scores (blank input); non-200 responses propagate null `dominant_emotion`

---

## Technical Stack Matrix

| Component | Technology | Role |
|:---|:---|:---|
| Runtime | Python 3.9+ | Application execution |
| Web Framework | Flask | HTTP routing, template rendering |
| NLP Backend | Watson NLP Emotion Predict | Cloud-hosted emotion classification |
| HTTP Client | requests | Watson API communication |
| Testing | unittest | Automated emotion scenario validation |
| Frontend | HTML + JavaScript | Text input form, AJAX submission |

---

## Operational Blueprint

### Prerequisites

- Python 3.9+
- Watson NLP API access (IBM Cloud credentials or Skills Network Lab)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/amrbassal98-ux/oaqjp-final-project-emb-ai.git
cd oaqjp-final-project-emb-ai

# Create isolated virtual environment (user-space, no sudo)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install flask requests

# Run the application
python server.py
```

The server boots on `http://localhost:5000`.

### API Endpoints

| Method | Path | Parameters | Description |
|:---|:---|:---|:---|
| `GET` | `/` | - | Render main application page |
| `GET` | `/emotionDetector` | `?textToAnalyze=...` | Analyze text, return emotion scores |

### Running Tests

```bash
python -m unittest test_emotion_detection -v
```

### Example Response

```
Input: "I am glad this happened"
Output: For the given statement, the system response is 'anger': 0.03,
'disgust': 0.01, 'fear': 0.02, 'joy': 0.92 and 'sadness': 0.01.
The dominant emotion is joy.
```

---

## Architectural Modernization Roadmap

### 1. Structured Python Logging Matrix

Replace `print()` statements with Python's `logging` module configured at three levels: `DEBUG` for Watson API request/response payloads, `INFO` for route invocations, and `ERROR` for upstream API failures. Implement a `RotatingFileHandler` for persistent log files and a `StreamHandler` for console output. This provides production-grade observability without external dependencies.

### 2. Containerized Runtime for Cloud-Native Deployment

Create a multi-stage `Dockerfile`: Stage 1 uses `python:3.11-slim` to install dependencies into a virtualenv; Stage 2 copies only the virtualenv and application code. Expose port 5000 via `EXPOSE` and set `CMD ["python", "server.py"]`. This produces a sub-100MB container image suitable for Kubernetes deployment or Cloud Foundry push.

### 3. Environment-Driven Configuration System

Extract the Watson API URL, model ID header, and Flask debug flag into a `.env` file loaded via `python-dotenv`. Replace hardcoded values in `emotion_detection.py` with `os.environ.get()` calls. This enables environment-specific configuration (dev/staging/prod) without code changes and prevents credential leakage in version control.

---

*Part of the IBM Full-Stack Cloud Developer Professional Certificate portfolio.*
