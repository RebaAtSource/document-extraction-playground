import tempfile
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from openai import OpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
import logging
import anthropic
from utils.extract_json import extract_json_from_response
from utils.token_utils import estimate_token_count
from utils.pdf_extraction import extract_text_from_pdf
from utils.prompts import system_prompts, user_prompts, get_prompts
from collections import OrderedDict

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI()  # It will automatically use OPENAI_API_KEY from environment

# Initialize Clients
openai_client = OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
openai_model = "gpt-4o"

deepseek_client = ChatCompletionsClient(endpoint="https://models.github.ai/inference", credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]))
deepseek_model = "deepseek/DeepSeek-V3-0324"

anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
anthropic_model = "claude-3-5-sonnet-20240620"

@app.route("/api/process-pdf", methods=["POST", "OPTIONS"])
def process_pdf():
    # logger.debug("Received request to /api/process-pdf")
    # logger.debug(f"Request method: {request.method}")
    # logger.debug(f"Request headers: {dict(request.headers)}")

    # Handle preflight request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    try:
        # logger.debug(f"Files in request: {request.files}")
        if "file" not in request.files:
            # logger.error("No file in request")
            return jsonify({"error": "No file provided"}), 400

        pdf_file = request.files["file"]
        if not pdf_file.filename:
            # logger.error("File has no filename")
            return jsonify({"error": "File has no filename"}), 400
        temp_file_path = os.path.join(tempfile.gettempdir(), pdf_file.filename)
        

        # Temporary file storage & extraction
        pdf_file.save(temp_file_path)
        pdf_text = extract_text_from_pdf(temp_file_path)
        os.remove(temp_file_path)

        # logger.debug("Successfully extracted text from PDF")

        # Set prompts based on selected document type
        document_type = request.form.get('type', 'invoice')  # Default to 'invoice' if not specified
        system_prompt, prompt = get_prompts(document_type, pdf_text)

        # ------------- CLIENT CALLS -------------
        # Call OpenAI client
        openai_response = client.chat.completions.create(
            model=openai_model,
            temperature=0.1,
            timeout=90,  # 90 second timeout for OpenAI API call
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {"role": "user", "content": prompt}
            ]
        )
        openai_response_content = str(openai_response.choices[0].message.content)

        # Call DeepSeek client
        deepseek_response = deepseek_client.complete(
            model=deepseek_model,
            temperature=0.1,
            timeout=90,  # 90 second timeout for OpenAI API call
            messages=[
                {
                    "role": "system",
                    "content": "You are an invoice data extraction assistant. IMPORTANT: Return ONLY valid JSON with no preamble, no explanations, and no additional text. The response must start with '{' and end with '}'."
                },
                {"role": "user", "content": prompt}
            ]
        )
        deepseek_response_content = str(deepseek_response.choices[0].message.content)

        # Call Anthropic client
        response = anthropic_client.messages.create(
            model=anthropic_model,
            max_tokens=4000,
            temperature=0.1,
            system="You are an invoice data extraction assistant. IMPORTANT: Return ONLY valid JSON with no preamble, no explanations, and no additional text. The response must start with '{' and end with '}'",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        # Anthropic returns a list of textblocks, so we need to convert the first one to a string
        anthropic_response_content = str(response.content[0].text)  # Convert to string if it's a textblock

        # Extract the JSON response
        # extracted_data = extract_json_from_response(response_content)
        # To Do : update token counts for different models
        # token_counts = estimate_token_count(prompt, extracted_data)

        logger.debug(f"DeepSeek response: {extract_json_from_response(deepseek_response_content)}")

        # List of model names and their corresponding response contents
        model_responses = {
            "deepseek": extract_json_from_response(deepseek_response_content),
            "openai": extract_json_from_response(openai_response_content),
            "anthropic": extract_json_from_response(anthropic_response_content)
        }


        # Construct the final response object
        response_data = {
            "success": True,
            "data": model_responses,
            "tokens": 1
        }

        return response_data

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# ------------- DOCUMENT TYPE SELECTION -------------
@app.route("/api/document-types", methods=["GET"])
def get_document_types():
    try:
        document_types = list(system_prompts.keys())
        return jsonify({"success": True, "document_types": document_types})
    except Exception as e:
        # logger.error(f"Error retrieving document types: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0", threaded=True)
