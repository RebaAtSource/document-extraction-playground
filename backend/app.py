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

@app.route('/api/process-pdf', methods=['POST', 'OPTIONS'])
def process_pdf():
    logger.debug('Received request to /api/process-pdf')
    logger.debug(f'Request method: {request.method}')
    logger.debug(f'Request headers: {dict(request.headers)}')
    
    # Handle preflight request
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', '*')
        response.headers.add('Access-Control-Allow-Methods', '*')
        return response

    try:
        logger.debug(f'Files in request: {request.files}')
        if 'file' not in request.files:
            logger.error('No file in request')
            return jsonify({'error': 'No file provided'}), 400

        pdf_file = request.files['file']
        if pdf_file.filename == '':
            logger.error('Empty filename')
            return jsonify({'error': 'No file selected'}), 400

        logger.debug(f'Processing file: {pdf_file.filename}')
        
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_file)
        logger.debug('Successfully extracted text from PDF')

        # Prepare the prompt for GPT-4
        prompt = f"""You are an expert at extracting information from invoices. Analyze the following invoice text and extract the requested information.

Text to analyze:
{pdf_text}

Instructions:
1. Extract all the fields listed below
2. Return the data in JSON format
3. Use null for any fields not found in the text
4. For addresses, maintain the original formatting including line breaks
5. For monetary values, include only the numerical amount (no currency symbols)
6. Look for variations in field names (e.g., "Shipping" vs "Freight" vs "Freight Charges")
7. For Terms, capture any payment terms format (e.g., "Net 30", "2/10 Net 30", "Due on Receipt")

Fields to extract:
- Invoice Date: Look for any date format associated with invoice date/issue date
- Invoice Number: Look for invoice #, reference number, or similar identifiers
- Vendor Name: Company or business name issuing the invoice
- Vendor Order Number/Sales Order Number: Look for SO#, Order #, or similar references
- Account Number: Any customer or account reference number
- Bill To Address: Complete billing address including company name if present
- Ship To Address: Complete shipping address including company name if present
- Source PO Number: Purchase order number reference
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
    "Invoice Date": null,
    "Invoice Number": null,
    "Vendor Name": null,
    "Vendor Order Number/Sales Order Number": null,
    "Account Number": null,
    "Bill To Address": null,
    "Ship To Address": null,
    "Source PO Number": null,
    "Packaging Fee": null,
    "Total": null,
    "Sales Tax": null,
    "Freight/Shipping": null,
    "Terms": null,
    "Banking Info": null,
    "Due Date": null,
    "Currency": null,
    "Prepayments/Deposit": null,
    "Balance Due": null
}}

Replace each null with the found value, or leave as null if not found. Ensure the JSON structure remains exactly as shown."""

        # Call GPT-4 with new client format
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts information from invoices and returns it in JSON format."},
                {"role": "user", "content": prompt}
            ]
        )

        # Extract the JSON response (new format)
        extracted_data = response.choices[0].message.content
        logger.debug('Successfully processed with GPT-4')

        return jsonify({
            'success': True,
            'data': extracted_data
        })

    except Exception as e:
        logger.error(f'Error processing request: {str(e)}', exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0') 