from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from PyPDF2 import PdfReader
from openai import OpenAI
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os
import logging
import tiktoken
import json
import extract_with_ocr
import anthropic
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

extractor = extract_with_ocr.InvoiceExtractor()

# Initialize OpenAI client
client = OpenAI()  # It will automatically use OPENAI_API_KEY from environment

# Initialize Clients
openai_client = OpenAI(base_url="https://models.inference.ai.azure.com", api_key=os.environ["GITHUB_TOKEN"])
openai_model = "gpt-4o"

deepseek_client = ChatCompletionsClient(endpoint="https://models.github.ai/inference", credential=AzureKeyCredential(os.environ["GITHUB_TOKEN"]))
deepseek_model = "deepseek/DeepSeek-V3-0324"

anthropic_client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
anthropic_model = "claude-3-5-sonnet-20240620"



def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Estimate the token count of a prompt
def estimate_token_count(prompt: str, response: str | None) -> dict[str, int]:
    tokenizer = tiktoken.encoding_for_model("gpt-4")
    input_tokens = len(tokenizer.encode(prompt))
    output_tokens = 0 if response is None else len(tokenizer.encode(response))
    return {"input_tokens": input_tokens, "output_tokens": output_tokens}

# Extracts a JSON object from a string response.
def extract_json_from_response(response_content):
    """
    Extracts a JSON object from a string response.

    Parameters:
    response_content (str): The response string from which to extract the JSON object.

    Returns:
    dict: The extracted JSON object as a Python dictionary, or None if parsing fails.
    """
    logger.debug("Raw response content: %s", response_content)
    try:
        # Directly parse the JSON string into a Python dictionary
        parsed_json = json.loads(response_content)
        logger.debug("Parsed JSON object: %s", parsed_json)
        return parsed_json
    except json.JSONDecodeError as e:
        logger.error("Error decoding JSON: %s", e)
        logger.error("Problematic JSON string: %s", response_content)
        # Attempt to trim the string to extract JSON
        start_index = response_content.find('{')
        end_index = response_content.rfind('}') + 1
        if start_index != -1 and end_index != -1:
            trimmed_content = response_content[start_index:end_index]
            try:
                parsed_json = json.loads(trimmed_content)
                logger.debug("Parsed JSON object after trimming: %s", parsed_json)
                return parsed_json
            except json.JSONDecodeError as e:
                logger.error("Error decoding JSON after trimming: %s", e)
                return None
        return None

@app.route("/api/process-pdf", methods=["POST", "OPTIONS"])
def process_pdf():
    logger.debug("Received request to /api/process-pdf")
    logger.debug(f"Request method: {request.method}")
    logger.debug(f"Request headers: {dict(request.headers)}")

    # Handle preflight request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    try:
        logger.debug(f"Files in request: {request.files}")
        if "file" not in request.files:
            logger.error("No file in request")
            return jsonify({"error": "No file provided"}), 400

        pdf_file = request.files["file"]
        if pdf_file.filename == "":
            logger.error("Empty filename")
            return jsonify({"error": "No file selected"}), 400

        logger.debug(f"Processing file: {pdf_file.filename}")

        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_file)
        logger.debug("Successfully extracted text from PDF")

        # Prepare the prompt for GPT-4

        prompt = f"""You are an expert at extracting information from invoices. Analyze the following invoice text and extract the requested information.

Text to analyze:
{pdf_text}

Instructions:
1. Extract all the fields listed below
2. Return the data in valid JSON format
3. Use null for any fields not found in the text
4. For addresses, include an object with the following fields:
    - company_name: the company name (or null if not found)
    - address_line_1: the first line of the address (or null if not found)
    - address_line_2: the second line of the address (or null if not found)
    - city: the city of the address (or null if not found)
    - state: the state of the address (or null if not found)
    - zip: the zip code of the address (or null if not found)
5. For monetary values, include only the numerical amount, to two decimal places (no currency symbols)
6. Look for variations in field names (e.g., "Shipping" vs "Freight" vs "Freight Charges")
7. For Terms, capture any payment terms format (e.g., "Net 30", "2/10 Net 30", "Due on Receipt")
8. Do not include other texts or comments outside of the JSON format

Fields to extract:
- vendor_name: Company or business name issuing the invoice
- invoice_date: Look for any date format associated with invoice date/issue date
- due_date: Payment due date in any format
- ship_date: Look for any date format associated with shipping date
- invoice_number: Look for invoice #, reference number, or similar identifiers
- vendor_order_number: Look for SO#, Order #, or similar references
- account_number: Any customer or account reference number
- po_number: Purchase order number reference
- terms: Payment terms in any format found
- banking_info: Any bank account, routing numbers, or payment instructions
- currency: Type of currency used (USD, EUR, etc.)
- bill_to_address: Complete billing address including company name if present
- ship_to_address: Complete shipping address including company name if present. If the ship to address includes Source Logistics, this is NOT the shipping address - leave null
- invoice_items:
-- spec_tag: Look for text that contains "Item" or "Spec" or "Tag", typically XX-### format, or similar
-- description: will typically describe a product or service, like 'decorative bed scarf @ King Guest Room'
-- quantity: Look for numbers that represent a quantity, typically a whole number
-- units: Look for text that represents a unit of measure, typically 2 or 3 letter codes. If not found, use "EA" as the default unit.
-- overage: Look for numbers that represent a quantity overage, typically a whole number
-- unit_price: Look for numbers that represent a price per unit, typically a float with 2 decimal places
-- discount: Look for numbers that represent a discount, typically a %
-- extended_price: Look for numbers that represent a total price, typically a float with 2 decimal places
-- fob: Look for text that represents a shipping term, typically a city, state, or country
- subtotal: Look for numbers that represent a subtotal, typically a float with 2 decimal places
- packing_fee Any packaging or handling charges
- freight: Any shipping, freight, or delivery charges
- sales_tax: Tax amount or rate applied
- sales_tax_rate: Tax rate applied, typically a %
- total: Final total amount of the invoice
- prepayment: Any advance payments or deposits applied
- balance_due: Remaining amount to be paid

Return the data in a similar JSON format:
{{
    "field_example": null,
    "example_address": {{
        "company_name": value,
        "address_line_1": value,
        "address_line_2": value,
        "city": value,
        "state": value,
        "zip": value,
    }},
    "invoice_items": [{{
        "spec_tag": FCH-002A.F3,
        "description": Fabric for chair CH-002A,
        "quantity": 32,
        "units": YD,
        "unit_price": 9.12,
        "extended_price": 291.84,
        "overage": 1.4,
        "fob": North Carolina,
    }}]
}}"""
        # Call GPT-4 client
        openai_response = client.chat.completions.create(
            model=openai_model,
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

        # set this to the model response you want to pass
        response_content = deepseek_response_content

        logger.debug("Response content before JSON extraction: %s", response_content)

        # Trim leading characters before the first '{' and trailing characters after the last '}'


        

        # Extract the JSON response
        # extracted_data = extract_json_from_response(response_content)
        # To Do : update token counts for different models
        # token_counts = estimate_token_count(prompt, extracted_data)

        return jsonify({"success": True, "data": {"deepseek": extract_json_from_response(deepseek_response_content), "openai": extract_json_from_response(openai_response_content), "anthropic": extract_json_from_response(anthropic_response_content)}, "tokens": 1})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0", threaded=True)
