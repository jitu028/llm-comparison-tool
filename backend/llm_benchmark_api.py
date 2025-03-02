import time
import openai
import anthropic
import cohere
from google.cloud import storage
from flask import Flask, request, jsonify
import os
import vertexai
from vertexai.generative_models import GenerativeModel
import json
from datetime import datetime
from google.cloud import secretmanager
import os

# **Set up Flask**
app = Flask(__name__)

# **Set up Cloud Storage**
GCS_BUCKET = "gcp-demo-028-benchmark-data"  # Replace with your bucket name
GCS_FOLDER = "benchmark_results"
storage_client = storage.Client()

# Load API keys from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
cohere_client = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

def get_secret(secret_name):
    """Retrieve secret from Google Cloud Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    project_id = "gcp-demo-028"
    secret_path = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")

# Load API keys from Secret Manager
openai.api_key = get_secret("OPENAI_API_KEY")
anthropic_client = anthropic.Anthropic(api_key=get_secret("ANTHROPIC_API_KEY"))
cohere_client = cohere.Client(api_key=get_secret("COHERE_API_KEY"))


def query_gemini(prompt, model_name):
    """Query Gemini AI model using Vertex AI Generative AI SDK."""
    try:
        vertexai.init(project="gcp-demo-028", location="us-central1")
        model = GenerativeModel(model_name)
        response = model.generate_content(
            [prompt],
            generation_config={"temperature": 0.7, "max_output_tokens": 512},
            stream=False
        )
        return response.text if response else "No response"
    except Exception as e:
        return str(e)

def query_model(model_name, prompt):
    """Query the selected model and return response and latency."""
    start_time = time.time()
    response_text = ""

    try:
        if model_name.startswith("gpt-"):
            response = openai.ChatCompletion.create(
                model=model_name, messages=[{"role": "user", "content": prompt}]
            )
            response_text = response["choices"][0]["message"]["content"]

        elif model_name.startswith("claude"):
            response = anthropic_client.messages.create(
                model=model_name, max_tokens=512, messages=[{"role": "user", "content": prompt}]
            )
            response_text = response.content[0].text

        elif model_name.startswith("command-"):
            response = cohere_client.generate(model=model_name, prompt=prompt, max_tokens=512)
            response_text = response.generations[0].text
        
        elif model_name.startswith("gemini"):
            response_text = query_gemini(prompt, model_name)
        
        else:
            return None, "Unsupported model"
    
    except Exception as e:
        return None, str(e)
    
    latency = (time.time() - start_time) * 1000
    return response_text, latency

def get_gcs_file_path(prompt):
    """Generate a Cloud Storage file path based on the prompt."""
    filename = prompt.replace(" ", "_").replace("?", "").replace(".", "").lower()
    return f"{GCS_FOLDER}/{filename}.json"

def log_to_gcs(model_name, latency, prompt, response):
    """Logs benchmark data to Google Cloud Storage as JSON."""
    bucket = storage_client.bucket(GCS_BUCKET)
    file_path = get_gcs_file_path(prompt)
    blob = bucket.blob(file_path)

    existing_data = []
    if blob.exists():
        existing_data = json.loads(blob.download_as_text())

    new_entry = {
        "model_name": model_name,
        "latency_ms": latency,
        "accuracy_score": 0.0,
        "cost_per_1k_tokens": 0.0,
        "user_feedback": 0,
        "prompt": prompt,
        "response": response,
        "created_at": datetime.utcnow().isoformat()
    }
    existing_data.append(new_entry)
    blob.upload_from_string(json.dumps(existing_data, indent=2), content_type="application/json")

@app.route("/benchmark", methods=["POST"])
def benchmark():
    """Handles model inference and logs results to Cloud Storage"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON format"}), 400

    model_name = data.get("model_name")
    prompt = data.get("prompt")

    if not model_name or not prompt:
        return jsonify({"error": "Missing model_name or prompt"}), 400
    
    response_text, latency = query_model(model_name, prompt)
    if response_text is None:
        return jsonify({"error": latency}), 500
    
    log_to_gcs(model_name, latency, prompt, response_text)
    
    return jsonify({"model": model_name, "response": response_text, "latency_ms": latency})

@app.route("/update-feedback", methods=["POST"])
def batch_update_feedback():
    """Batch update user feedback in Cloud Storage JSON files"""
    try:
        data = request.get_json()

        if not isinstance(data, list) or len(data) == 0:
            return jsonify({"error": "Invalid input format. Expected a list of feedback entries."}), 400

        bucket = storage_client.bucket(GCS_BUCKET)

        for entry in data:
            model_name = entry.get("model_name")
            prompt = entry.get("prompt")
            feedback = entry.get("user_feedback")

            if not model_name or not prompt or feedback is None:
                return jsonify({"error": "Invalid entry in batch request"}), 400

            file_path = get_gcs_file_path(prompt)
            blob = bucket.blob(file_path)

            if not blob.exists():
                return jsonify({"error": f"No data found for prompt: {prompt}"}), 404

            existing_data = json.loads(blob.download_as_text())

            updated = False
            for record in existing_data:
                if record.get("model_name") == model_name:
                    record["user_feedback"] = feedback
                    updated = True

            if not updated:
                return jsonify({"error": f"No matching record found for model {model_name}"}), 404

            blob.upload_from_string(json.dumps(existing_data, indent=2), content_type="application/json")

        return jsonify({"message": "User feedback updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/past-results", methods=["GET"])
def get_past_results():
    """Retrieve past results from Cloud Storage JSON files"""
    bucket = storage_client.bucket(GCS_BUCKET)
    blobs = bucket.list_blobs(prefix=GCS_FOLDER)

    results = []
    for blob in blobs:
        try:
            json_data = json.loads(blob.download_as_text())
            results.extend(json_data)
        except Exception as e:
            print(f"⚠️ Error reading {blob.name}: {e}")

    if not results:
        return jsonify({"message": "No past results found"}), 404

    results = sorted(results, key=lambda x: x.get("created_at", ""), reverse=True)
    return jsonify(results[:100]), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
