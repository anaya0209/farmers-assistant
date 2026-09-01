# Module 2: ASR & Translation (Bhashini Pipeline)

This branch (`module-2-asr`) contains the implementation for the Speech-to-Text (ASR) and Translation pipeline of the Multi-Agent Farmers Assistant.

## Overview
This module is responsible for taking a recorded voice query (e.g., from a farmer speaking in a regional language like Hindi) and processing it through the **Bhashini (ULCA) Dhruva Inference API**.

The pipeline executes two sequential tasks:
1. **ASR (Automatic Speech Recognition):** Converts the spoken regional language audio (e.g., `.wav`) into text.
2. **Translation:** Translates the recognized regional text into English, which is required for the downstream LangGraph orchestrator (Module 3) to process the farmer's intent accurately.

## File Structure
- `modules/m2_asr_bhashini.py`: The core production script containing the API integration and Base64 encoding logic.

## Setup Instructions

1. **Environment Variables**
   You must configure your Bhashini API credentials. Create a `.env` file in the root directory (`agri-assistant-backend/`) and add the following keys:
   ```env
   BHASHINI_USER_ID="your_user_id"
   BHASHINI_API_KEY="your_api_key"
   BHASHINI_AUTH_TOKEN="your_auth_token"
   BHASHINI_INFERENCE_URL="https://dhruva-api.bhashini.gov.in/services/inference/pipeline"
   
   # Optional depending on your specific Bhashini config:
   BHASHINI_ASR_SERVICE_ID="your_asr_service_id"
   BHASHINI_TRANSLATION_SERVICE_ID="your_translation_service_id"
   ```

2. **Virtual Environment & Dependencies**
   It is highly recommended to use a virtual environment to isolate the project dependencies.
   
   **Create and activate the virtual environment (Windows PowerShell):**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **Install the required python packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Local Testing

To start the FastAPI server locally:
1. Make sure your virtual environment is activated and you have copied `.env.example` to `.env`.
2. Run the server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
3. Open your browser and navigate to the Swagger UI: `http://localhost:8000/docs`
4. Use the `POST /api/v1/asr/transcribe` endpoint to upload any `.wav` or `.mp3` audio file directly through your browser and see the translated text in the response!
