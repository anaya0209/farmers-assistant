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

2. **Install Dependencies**
   Ensure you have installed the required python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Local Testing

To test the module locally:
1. Place a sample audio file named `sample_farmer_query.wav` in the root directory.
2. Run the script directly:
   ```bash
   python modules/m2_asr_bhashini.py
   ```
3. The script will encode the audio, send the payload to the Bhashini API, and print the final English translated text to the console.
