# Prompts for different document types
def get_prompts(document_type: str, pdf_text: str) -> tuple[str, str]:
    """
    Retrieve and format the system and user prompts based on the document type.

    Parameters:
    document_type (str): The type of document (e.g., 'invoice', 'spec', etc.).
    pdf_text (str): The extracted text from the PDF.

    Returns:
    tuple: A tuple containing the system prompt and the formatted user prompt.
    """
    system_prompt = system_prompts.get(document_type, system_prompts['invoice'])
    user_prompt = user_prompts.get(document_type, user_prompts['invoice'])
    formatted_user_prompt = user_prompt.format(pdf_text=pdf_text)
    return system_prompt, formatted_user_prompt 

# System prompts
system_prompts = {
    "invoice": "You are an invoice data extraction assistant. IMPORTANT: Return ONLY valid JSON with no preamble, no explanations, and no additional text. The response must start with '{' and end with '}'.",
    "spec": "You are a specification data extraction assistant. IMPORTANT: Return ONLY valid JSON with no preamble, no explanations, and no additional text. The response must start with '{' and end with '}'.",
    "quote": "You are a quote data extraction assistant. IMPORTANT: Return ONLY valid JSON with no preamble, no explanations, and no additional text. The response must start with '{' and end with '}'.",
    "submittal": "You are a submittal data extraction assistant. IMPORTANT: Return ONLY valid JSON with no preamble, no explanations, and no additional text. The response must start with '{' and end with '}'."
}

# User prompts
user_prompts = {
    "invoice": """You are an expert at extracting information from invoices. Analyze the following invoice text and extract the requested information.

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
}}""",
    "spec": "You are an expert at extracting information from specifications. Analyze the following specification text and extract the requested information.",
    "quote": "You are an expert at extracting information from quotes. Analyze the following quote text and extract the requested information.",
    "submittal": "You are an expert at extracting information from submittals. Analyze the following submittal text and extract the requested information."
}