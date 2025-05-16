from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from PyPDF2 import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import io
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize OpenAI client
client = OpenAI()  # It will automatically use OPENAI_API_KEY from environment


def extract_text_from_pdf(pdf_file):
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


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
- invoice_number: Look for invoice #, reference number, or similar identifiers
- vendor_order_number: Look for SO#, Order #, or similar references
- account_number: Any customer or account reference number
- po_number: Purchase order number reference
- terms: Payment terms in any format found
- banking_info: Any bank account, routing numbers, or payment instructions
- currency: Type of currency used (USD, EUR, etc.)
- bill_to_address: Complete billing address including company name if present
- ship_to_address: Complete shipping address including company name if present
- invoice_items:
-- spec_tag: Look for text that contains "Item" or "Spec" or "Tag", typically XX-### format, or similar
-- description: will typically describe a product or service
-- quantity: Look for numbers that represent a quantity, typically a whole number
-- units: Look for text that represents a unit of measure, typically 2 or 3 letter codes. If not found, use "EA" as the default unit.
-- overage: Look for numbers that represent a quantity overage, typically a whole number
-- unit_price: Look for numbers that represent a price per unit, typically a float with 2 decimal places
-- extended_price: Look for numbers that represent a total price, typically a float with 2 decimal places
-- fob: Look for text that represents a shipping term, typically a city, state, or country
- packing_fee Any packaging or handling charges
- freight: Any shipping, freight, or delivery charges
- sales_tax: Tax amount or rate applied
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

        # Call GPT-4 with new client format
        response = client.chat.completions.create(
            model="gpt-4",
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

        # Extract the JSON response (new format)
        extracted_data = response.choices[0].message.content
        logger.debug("Successfully processed with GPT-4")

        return jsonify({"success": True, "data": extracted_data})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0", threaded=True)
