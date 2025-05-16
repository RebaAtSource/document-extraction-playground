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


# def generate_prompt(pdf_text, prompt_type):
#     prompt_invoice_items = f"""You are an expert at extracting line item information from invoices. Analyze the following invoice text and extract the requested information.

# Text to analyze:
# {pdf_text}

# Instructions:
# 1. Look for a table of line items in the invoice
# 2. There may be one, or many line items, but they will have the same format
# 3. Return the data in valid JSON format
# 4. Use null for any fields not found in the text
# 5. For monetary values, include only the numerical amount (no currency symbols)
# 6. Look for variations in field names ("Total Price" or "Amount" or "Extended Price")
# 7. Do not include other texts or comments outside of the JSON format

# Fields to extract:
# - Item Number/ Spec Tag: Look for text that contains "Item" or "Spec" or "Tag", typically XX-### format, or similar
# - Description/ Spec Description: will typically describe a product or service
# - Quantity: Look for numbers that represent a quantity, typically a whole number
# - Units: Look for text that represents a unit of measure, typically 2 or 3 letter codes
# - Unit Price: Look for numbers that represent a price per unit, typically a float with 2 decimal places
# - Extended Price: Look for numbers that represent a total price, typically a float with 2 decimal places
# - Overage: Look for numbers that represent a quantity overage, typically a whole number
# - FOB: Look for text that represents a shipping term, typically a city, state, or country

# Return the data in this exact JSON format:
# {
#     "spec_tag": null,
#     "description": null,
#     "quantity": null,
#     "units": null,
#     "unit_price": null,
#     "extended_price": null,
#     "overage": null,
#     "fob": null
# }"""

    

    # if prompt_type == "invoice_items":
    #     return prompt_invoice_items
    # elif prompt_type == "invoice_data":
    #     return prompt_invoice_data


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
4. For addresses, maintain the original formatting including line breaks
5. For monetary values, include only the numerical amount (no currency symbols)
6. Look for variations in field names (e.g., "Shipping" vs "Freight" vs "Freight Charges")
7. For Terms, capture any payment terms format (e.g., "Net 30", "2/10 Net 30", "Due on Receipt")
8. Do not include other texts or comments outside of the JSON format

Fields to extract:
- Invoice Date: Look for any date format associated with invoice date/issue date
- Invoice Number: Look for invoice #, reference number, or similar identifiers
- Vendor Name: Company or business name issuing the invoice
- Vendor Order Number/Sales Order Number: Look for SO#, Order #, or similar references
- Account Number: Any customer or account reference number
- Bill To Address: Complete billing address including company name if present
- Ship To Address: Complete shipping address including company name if present
- Source PO Number: Purchase order number reference
- Invoice Items:
-- Item Number/ Spec Tag: Look for text that contains "Item" or "Spec" or "Tag", typically XX-### format, or similar
-- Description/ Spec Description: will typically describe a product or service
-- Quantity: Look for numbers that represent a quantity, typically a whole number
-- Units: Look for text that represents a unit of measure, typically 2 or 3 letter codes
-- Unit Price: Look for numbers that represent a price per unit, typically a float with 2 decimal places
-- Extended Price: Look for numbers that represent a total price, typically a float with 2 decimal places
-- Overage: Look for numbers that represent a quantity overage, typically a whole number
-- FOB: Look for text that represents a shipping term, typically a city, state, or country
- Packaging Fee: Any packaging or handling charges
- Total: Final total amount of the invoice
- Sales Tax: Tax amount or rate applied
- Freight/Shipping: Any shipping, freight, or delivery charges
- Terms: Payment terms in any format found
- Banking Info: Any bank account, routing numbers, or payment instructions
- Due Date: Payment due date in any format
- Currency: Type of currency used (USD, EUR, etc.)
- Prepayments/Deposit: Any advance payments or deposits applied
- Balance Due: Remaining amount to be paid

Return the data in this exact JSON format:
{{
    "vendor_name": null,
    "invoice_date": null,
    "due_date": null,
    "invoice_number": null,
    "vendor_order_number": null,
    "account_number": null,
    "source_po_number": null,
    "terms": null,
    "banking_info": null,
    "currency": null,
    "bill_to_address": {{
        "company_name": null,
        "address_line_1": null,
        "address_line_2": null,
        "city": null,
        "state": null,
        "zip": null
    }},
    "ship_to_address": {{
        "company_name": null,
        "address_line_1": null,
        "address_line_2": null,
        "city": null,
        "state": null,
        "zip": null
    }},
    "invoice_items": [{{
        "spec_tag": null,
        "description": null,
        "quantity": null,
        "units": null,
        "unit_price": null,
        "extended_price": null,
        "overage": null,
        "fob": null
     }}]
    "packaging_fee": null,
    "freight_shipping": null,
    "sales_tax": null,
    "total": null,
    "prepayments_deposit": null,
    "balance_due": null
}}"""

#         prompt_invoice_data = f"""You are an expert at extracting information from invoices. Analyze the following invoice text and extract the requested information.

# Text to analyze:
# {pdf_text}

# Instructions:
# 1. Extract all the fields listed below
# 2. Return the data in valid JSON format
# 3. Use null for any fields not found in the text
# 4. For addresses, maintain the original formatting including line breaks
# 5. For monetary values, include only the numerical amount (no currency symbols)
# 6. Look for variations in field names (e.g., "Shipping" vs "Freight" vs "Freight Charges")
# 7. For Terms, capture any payment terms format (e.g., "Net 30", "2/10 Net 30", "Due on Receipt")
# 8. Do not include other texts or comments outside of the JSON format

# Fields to extract:
# - Invoice Date: Look for any date format associated with invoice date/issue date
# - Invoice Number: Look for invoice #, reference number, or similar identifiers
# - Vendor Name: Company or business name issuing the invoice
# - Vendor Order Number/Sales Order Number: Look for SO#, Order #, or similar references
# - Account Number: Any customer or account reference number
# - Bill To Address: Complete billing address including company name if present
# - Ship To Address: Complete shipping address including company name if present
# - Source PO Number: Purchase order number reference
# - Packaging Fee: Any packaging or handling charges
# - Total: Final total amount of the invoice
# - Sales Tax: Tax amount or rate applied
# - Freight/Shipping: Any shipping, freight, or delivery charges
# - Terms: Payment terms in any format found
# - Banking Info: Any bank account, routing numbers, or payment instructions
# - Due Date: Payment due date in any format
# - Currency: Type of currency used (USD, EUR, etc.)
# - Prepayments/Deposit: Any advance payments or deposits applied
# - Balance Due: Remaining amount to be paid

# Return the data in this exact JSON format:
# {{
#     "vendor_name": null,
#     "invoice_date": null,
#     "due_date": null,
#     "invoice_number": null,
#     "vendor_order_number": null,
#     "account_number": null,
#     "source_po_number": null,
#     "terms": null,
#     "banking_info": null,
#     "currency": null,
#     "bill_to_address": {{
#         "company_name": null,
#         "address_line_1": null,
#         "address_line_2": null,
#         "city": null,
#         "state": null,
#         "zip": null
#     }},
#     "ship_to_address": {{
#         "company_name": null,
#         "address_line_1": null,
#         "address_line_2": null,
#         "city": null,
#         "state": null,
#         "zip": null
#     }},
#     "packaging_fee": null,
#     "freight_shipping": null,
#     "sales_tax": null,
#     "total": null,
#     "prepayments_deposit": null,
#     "balance_due": null
# }}"""

        
#         prompt_invoice_items = f"""You are an expert at extracting line item information from invoices. Analyze the following invoice text and extract the requested information.

# Text to analyze:
# {pdf_text}

# Instructions:
# 1. Look for a table of line items in the invoice
# 2. There may be one, or many line items, but they will have the same format
# 3. Return the data in valid JSON format
# 4. Use null for any fields not found in the text
# 5. For monetary values, include only the numerical amount (no currency symbols)
# 6. Look for variations in field names ("Total Price" or "Amount" or "Extended Price")
# 7. Do not include other texts or comments outside of the JSON format
# 8. ONLY return valid JSON, nothing else

# Fields to extract:
# - Item Number/ Spec Tag: Look for text that contains "Item" or "Spec" or "Tag", typically XX-### format, or similar
# - Description/ Spec Description: will typically describe a product or service
# - Quantity: Look for numbers that represent a quantity, typically a whole number
# - Units: Look for text that represents a unit of measure, typically 2 or 3 letter codes
# - Unit Price: Look for numbers that represent a price per unit, typically a float with 2 decimal places
# - Extended Price: Look for numbers that represent a total price, typically a float with 2 decimal places
# - Overage: Look for numbers that represent a quantity overage, typically a whole number
# - FOB: Look for text that represents a shipping term, typically a city, state, or country

# Return the data in this exact JSON format:
# {{
#     "spec_tag": null,
#     "description": null,
#     "quantity": null,
#     "units": null,
#     "unit_price": null,
#     "extended_price": null,
#     "overage": null,
#     "fob": null
# }}"""

        # Call GPT-4 with new client format
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=0.1,
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
    app.run(debug=True, port=3000, host="0.0.0.0")
