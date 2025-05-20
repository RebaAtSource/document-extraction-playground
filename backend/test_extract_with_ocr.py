from extract_with_ocr import InvoiceExtractor
import os
import json
import argparse

extracted_data = InvoiceExtractor().extract_invoice_data('inputs/invoices/2Modern.pdf')

def save_to_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

save_to_json(extracted_data, 'outputs/json/2Modern_invoice_data.json')