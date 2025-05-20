# this code was created by Claude 3.7 Sonnet for extracting pdf invoice data
import os
import re
import json
import argparse
import tempfile
from PyPDF2 import PdfReader
try:
    from pdf2image import convert_from_path
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

class InvoiceExtractor:
    """A class to extract data from 2Modern invoices using multiple methods."""
    
    def __init__(self, use_ocr=False, poppler_path=None):
        """
        Initialize the extractor
        
        Args:
            use_ocr (bool): Whether to use OCR for text extraction
            poppler_path (str): Path to poppler binaries (required for pdf2image on Windows)
        """
        self.use_ocr = use_ocr
        self.poppler_path = poppler_path
        
        if use_ocr and not OCR_AVAILABLE:
            print("Warning: OCR requested but pdf2image or pytesseract is not installed.")
            print("Please install with: pip install pdf2image pytesseract")
            print("Falling back to PyPDF2 extraction.")
            self.use_ocr = False
    
    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file using PyPDF2 or OCR
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text
        """
        # First try with PyPDF2
        reader = PdfReader(pdf_path)
        text = reader.pages[0].extract_text()
        
        # If text extraction failed or OCR is forced, use OCR
        if not text or self.use_ocr:
            if OCR_AVAILABLE:
                text = self._extract_text_with_ocr(pdf_path)
            else:
                print("Warning: PDF text extraction failed and OCR is not available.")
        
        return text
    
    def _extract_text_with_ocr(self, pdf_path):
        """
        Extract text from a PDF file using OCR
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text
        """
        # Convert PDF to images
        images = convert_from_path(pdf_path, poppler_path=self.poppler_path)
        
        # Extract text from images using OCR
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        
        return text
    
    def extract_invoice_data(self, pdf_path):
        """
        Extract structured data from a 2Modern invoice PDF
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            dict: Structured invoice data
        """
        # Extract text from the PDF
        text = self.extract_text_from_pdf(pdf_path)
        
        # Initialize the invoice data structure
        invoice_data = {
            "invoice_details": {},
            "company_information": {
                "vendor": "2Modern",
                "company_address": {},
                "payment_address": {}
            },
            "billing_information": {
                "address": {}
            },
            "shipping_information": {
                "address": {}
            },
            "prepared_by": {},
            "line_items": [],
            "financial_summary": {},
            "notes": []
        }
        
        # Extract invoice details using various regex patterns to handle potential variations
        self._extract_invoice_details(text, invoice_data)
        
        # Extract billing and shipping information
        self._extract_address_information(text, invoice_data)
        
        # Extract company information
        self._extract_company_information(text, invoice_data)
        
        # Extract line items
        self._extract_line_items(text, invoice_data)
        
        # Extract financial summary
        self._extract_financial_summary(text, invoice_data)
        # Extract notes
        self._extract_notes(text, invoice_data)
        
        return invoice_data
    
    def _extract_invoice_details(self, text, invoice_data):
        """Extract invoice number, date, PO number etc."""
        # Invoice number patterns
        invoice_patterns = [
            r'(\d+)Invoice',
            r'Invoice[:\s]+(\d+)',
            r'INVOICE\s+#?\s*(\d+)'
        ]
        
        for pattern in invoice_patterns:
            match = re.search(pattern, text)
            if match:
                invoice_data["invoice_details"]["invoice_number"] = match.group(1)
                break
        
        # Created date patterns
        date_patterns = [
            r'(\d+/\d+/\d+)Created Date',
            r'Created Date[:\s]+(\d+/\d+/\d+)',
            r'Date[:\s]+(\d+/\d+/\d+)'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                invoice_data["invoice_details"]["created_date"] = match.group(1)
                break
        
        # PO number patterns
        po_patterns = [
            r'(PO#[\w-]+)Quote Name',
            r'Customer PO #[:\s]+([\w-]+)',
            r'PO[:\s]+([\w-]+)'
        ]
        
        for pattern in po_patterns:
            match = re.search(pattern, text)
            if match:
                invoice_data["invoice_details"]["customer_po"] = match.group(1)
                break
                
        # Quote name patterns
        quote_patterns = [
            r'(PO#[\w-]+)Quote Name',
            r'Quote Name[:\s]+([\w-]+)'
        ]
        
        for pattern in quote_patterns:
            match = re.search(pattern, text)
            if match:
                invoice_data["invoice_details"]["quote_name"] = match.group(1)
                break
    
    def _extract_address_information(self, text, invoice_data):
        """Extract billing and shipping address information"""
        # Billing information
        bill_to_patterns = [
            r'(.*?)Bill To Name\n(.*?)\n(.*?)\n(.*?), (.*?) (\d+)\n(.*?)\n',
            r'Bill To[:\s]+(.*?)\n(.*?)\n(.*?), (.*?) (\d+)\n(.*?)\n'
        ]
        
        for pattern in bill_to_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match and len(match.groups()) >= 6:  # Ensure we have enough groups
                if len(match.groups()) == 7:  # First pattern
                    invoice_data["billing_information"]["name"] = match.group(2).strip()
                    street_idx, city_idx, state_idx, zip_idx, country_idx = 3, 4, 5, 6, 7
                else:  # Second pattern
                    invoice_data["billing_information"]["name"] = match.group(1).strip()
                    street_idx, city_idx, state_idx, zip_idx, country_idx = 2, 3, 4, 5, 6
                
                invoice_data["billing_information"]["address"]["street"] = match.group(street_idx).strip()
                invoice_data["billing_information"]["address"]["city"] = match.group(city_idx).strip()
                invoice_data["billing_information"]["address"]["state"] = match.group(state_idx).strip()
                invoice_data["billing_information"]["address"]["zip"] = match.group(zip_idx).strip()
                invoice_data["billing_information"]["address"]["country"] = match.group(country_idx).strip()
                break
        
        # Shipping information
        ship_to_patterns = [
            r'(.*?)Ship To Name\n(.*?)\n(.*?)\n(.*?), (.*?) (\d+)\n(.*?)\n',
            r'Ship To[:\s]+(.*?)\n(.*?)\n(.*?), (.*?) (\d+)\n(.*?)\n'
        ]
        
        for pattern in ship_to_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match and len(match.groups()) >= 6:
                if len(match.groups()) == 7:  # First pattern
                    invoice_data["shipping_information"]["name"] = match.group(2).strip()
                    street_idx, city_idx, state_idx, zip_idx, country_idx = 3, 4, 5, 6, 7
                else:  # Second pattern
                    invoice_data["shipping_information"]["name"] = match.group(1).strip()
                    street_idx, city_idx, state_idx, zip_idx, country_idx = 2, 3, 4, 5, 6
                
                invoice_data["shipping_information"]["address"]["street"] = match.group(street_idx).strip()
                invoice_data["shipping_information"]["address"]["city"] = match.group(city_idx).strip()
                invoice_data["shipping_information"]["address"]["state"] = match.group(state_idx).strip()
                invoice_data["shipping_information"]["address"]["zip"] = match.group(zip_idx).strip()
                invoice_data["shipping_information"]["address"]["country"] = match.group(country_idx).strip()
                break
        
        # Extract sidemark
        sidemark_patterns = [
            r'(SM:.*?)sidemark',
            r'Sidemark[:\s]+(.*?)\n'
        ]
        
        for pattern in sidemark_patterns:
            match = re.search(pattern, text)
            if match:
                invoice_data["shipping_information"]["sidemark"] = match.group(1).strip()
                break
        
        # Extract prepared by information
        preparer_patterns = [
            r'(.*?)Prepared By\n(Direct: [\d\.]+)Phone\n(.*?)Email',
            r'Prepared By[:\s]+(.*?)\nPhone[:\s]+(.*?)\nEmail[:\s]+(.*?)\n'
        ]
        
        for pattern in preparer_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                invoice_data["prepared_by"]["name"] = match.group(1).strip()
                invoice_data["prepared_by"]["phone"] = match.group(2).strip()
                invoice_data["prepared_by"]["email"] = match.group(3).strip()
                break
    
    def _extract_company_information(self, text, invoice_data):
        """Extract company address and payment information"""
        # Company address
        company_addr_patterns = [
            r'Company Address\n(.*?)\n(.*?), (.*?) (\d+)\n(.*?)\n',
            r'Company Address[:\s]+(.*?)\n(.*?), (.*?) (\d+)\n(.*?)\n'
        ]
        
        for pattern in company_addr_patterns:
            match = re.search(pattern, text, re.DOTALL)
            if match:
                invoice_data["company_information"]["company_address"]["street"] = match.group(1).strip()
                invoice_data["company_information"]["company_address"]["city"] = match.group(2).strip()
                invoice_data["company_information"]["company_address"]["state"] = match.group(3).strip()
                invoice_data["company_information"]["company_address"]["zip"] = match.group(4).strip()
                invoice_data["company_information"]["company_address"]["country"] = match.group(5).strip()
                break
        
        # Payment address
        payment_addr_patterns = [
            r'Submit Payment To:\n2Modern\n(PO Box \d+)\n(.*?), (.*?) ([\d-]+)',
            r'Submit Payment To[:\s]+2Modern\n(PO Box \d+)\n(.*?), (.*?) ([\d-]+)'
        ]
        
        for pattern in payment_addr_patterns:
            match = re.search(pattern, text)
            if match:
                invoice_data["company_information"]["payment_address"]["po_box"] = match.group(1).strip()
                invoice_data["company_information"]["payment_address"]["city"] = match.group(2).strip()
                invoice_data["company_information"]["payment_address"]["state"] = match.group(3).strip()
                invoice_data["company_information"]["payment_address"]["zip"] = match.group(4).strip()
                break

    def _extract_line_items(self, text, invoice_data):
        """
        Extract line items from the invoice text.

        Args:
            text (str): The text extracted from the PDF.
            invoice_data (dict): The dictionary to store extracted data.
        """
        # Example pattern to match line items
        line_item_pattern = r'Item\s+(\d+)\s+Description\s+([\w\s]+)\s+Quantity\s+(\d+)\s+Price\s+(\d+\.\d{2})'
        
        matches = re.findall(line_item_pattern, text)
        for match in matches:
            item = {
                "item_number": match[0],
                "description": match[1].strip(),
                "quantity": int(match[2]),
                "price": float(match[3])
            }
            invoice_data["line_items"].append(item)

        # Add more logic as needed to handle different formats or additional fields

    def _extract_financial_summary(self, text, invoice_data):
        """
        Extract financial summary from the invoice text.

        Args:
            text (str): The text extracted from the PDF.
            invoice_data (dict): The dictionary to store extracted data.
        """
        # Example patterns to match financial summary fields
        subtotal_pattern = r'Subtotal[:\s]+\$?(\d+\.\d{2})'
        tax_pattern = r'Tax[:\s]+\$?(\d+\.\d{2})'
        total_pattern = r'Total[:\s]+\$?(\d+\.\d{2})'

        # Extract subtotal
        match = re.search(subtotal_pattern, text)
        if match:
            invoice_data["financial_summary"]["subtotal"] = float(match.group(1))

        # Extract tax
        match = re.search(tax_pattern, text)
        if match:
            invoice_data["financial_summary"]["tax"] = float(match.group(1))

        # Extract total
        match = re.search(total_pattern, text)
        if match:
            invoice_data["financial_summary"]["total"] = float(match.group(1))

        # Add more logic as needed to handle different formats or additional fields

    def _extract_notes(self, text, invoice_data):
        """
        Extract notes from the invoice text.

        Args:
            text (str): The text extracted from the PDF.
            invoice_data (dict): The dictionary to store extracted data.
        """
        # Example pattern to match notes
        notes_pattern = r'Notes[:\s]+([\w\s,.-]+)'

        # Extract notes
        match = re.search(notes_pattern, text, re.DOTALL)
        if match:
            notes = match.group(1).strip()
            invoice_data["notes"].append(notes)

        # Add more logic as needed to handle different formats or additional fields

def main():
    parser = argparse.ArgumentParser(description='Extract data from 2Modern invoice PDFs')
    parser.add_argument('pdf_path', help='Path to the invoice PDF file')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Check if the PDF file exists
    if not os.path.isfile(args.pdf_path):
        print(f"Error: PDF file '{args.pdf_path}' not found")
        return
    
    # Extract data from the PDF
    invoice_data = extract_invoice_data(args.pdf_path)
    
    # Determine output path
    output_path = args.output
    if not output_path:
        base_name = os.path.splitext(os.path.basename(args.pdf_path))[0]
        output_path = f"{base_name}_invoice_data.json"
    
    # Write the data to a JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(invoice_data, f, indent=2)
    
    print(f"Invoice data extracted and saved to {output_path}")

if __name__ == "__main__":
    main()