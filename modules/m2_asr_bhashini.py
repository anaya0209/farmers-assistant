import os
import base64
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bhashini API Credentials
USER_ID = os.getenv("BHASHINI_USER_ID")
API_KEY = os.getenv("BHASHINI_API_KEY")
AUTH_TOKEN = os.getenv("BHASHINI_AUTH_TOKEN") # e.g. from the 'Authorization' header requirement

# Bhashini Inference Pipeline Endpoint
INFERENCE_URL = os.getenv("BHASHINI_INFERENCE_URL", "https://dhruva-api.bhashini.gov.in/services/inference/pipeline")

def encode_audio(file_path: str) -> str:
    """Reads a local audio file and encodes it to Base64."""
    try:
        with open(file_path, "rb") as audio_file:
            encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"Error reading audio file: {e}")
        return ""

def process_audio(file_path: str, source_language: str = "hi", target_language: str = "en") -> str:
    """
    Sends the audio file to Bhashini API for ASR and Translation.
    Pipeline: ASR (Hindi/Regional) -> Translation (English).
    """
    base64_audio = encode_audio(file_path)
    if not base64_audio:
        return "Failed to encode audio."

    headers = {
        "Content-Type": "application/json",
        "Authorization": AUTH_TOKEN,
    }

    # Pipeline configuration based on Bhashini documentation
    payload = {
        "pipelineTasks": [
            {
                "taskType": "asr",
                "config": {
                    "language": {
                        "sourceLanguage": source_language
                    },
                    "serviceId": os.getenv("BHASHINI_ASR_SERVICE_ID", ""),
                    "audioFormat": "wav",
                    "samplingRate": 16000
                }
            },
            {
                "taskType": "translation",
                "config": {
                    "language": {
                        "sourceLanguage": source_language,
                        "targetLanguage": target_language
                    },
                    "serviceId": os.getenv("BHASHINI_TRANSLATION_SERVICE_ID", "")
                }
            }
        ],
        "inputData": {
            "audio": [
                {
                    "audioContent": base64_audio
                }
            ]
        }
    }

    try:
        response = requests.post(INFERENCE_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Extract the final translated text from the pipeline response
        if "pipelineResponse" in data:
            for task_response in data["pipelineResponse"]:
                if task_response.get("taskType") == "translation":
                    if "output" in task_response and len(task_response["output"]) > 0:
                        return task_response["output"][0].get("target", "")
        
        print(f"Could not extract translation from response: {data}")
        return ""

    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        if e.response is not None:
             print(f"Response body: {e.response.text}")
        return ""
    except (KeyError, IndexError, ValueError) as e:
        print(f"Error parsing response: {e}")
        return ""

if __name__ == "__main__":
    # Example usage for testing
    sample_audio = "sample_farmer_query.wav"
    
    if not os.path.exists(sample_audio):
        print(f"Please provide a valid audio file at: {sample_audio}")
    else:
        print(f"Processing audio: {sample_audio}")
        english_translation = process_audio(sample_audio, source_language="hi", target_language="en")
        print(f"Final Translated Text (English): {english_translation}")
