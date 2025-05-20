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

    

    # if prompt_type == "invoice_items":
    #     return prompt_invoice_items
    # elif prompt_type == "invoice_data":
    #     return prompt_invoice_data

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
