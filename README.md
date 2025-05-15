# PDF Invoice Data Extraction

This application extracts data from PDF invoices using GPT-4. It features a modern React frontend for PDF upload and preview, and a Flask backend for processing and data extraction.

## Features

- 📄 Drag & drop PDF upload
- 👁️ PDF preview with pagination
- 🤖 GPT-4 powered data extraction
- 📋 Structured data display
- ⚡ Real-time processing
- 🎨 Modern Material-UI interface

## Extracted Data Fields

The application extracts the following information from invoices:
- Invoice Date
- Invoice Number
- Vendor Name
- Vendor Order Number/Sales Order Number
- Account Number
- Bill To Address
- Ship To Address
- Source PO Number
- Packaging Fee
- Total
- Sales Tax
- Freight/Shipping
- Terms
- Banking Info
- Due Date
- Currency
- Prepayments/Deposit
- Balance Due

## Prerequisites

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- OpenAI API key

## Project Structure

```
document-extraction-playground/
├── frontend/           # React frontend application
├── backend/           # Flask backend application
│   ├── venv/         # Python virtual environment
│   ├── app.py        # Flask application
│   ├── start.sh      # Backend startup script
│   ├── requirements.txt
│   └── .env          # Environment variables
└── README.md
```

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the backend directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Make the startup script executable:
   ```bash
   chmod +x start.sh
   ```

5. Start the backend server:
   ```bash
   ./start.sh
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies and start the development server:
   ```bash
   npm install
   npm run dev
   ```

The application will be available at:
- Frontend: http://localhost:5173
- Backend: http://localhost:5000

## Usage

1. Open the application in your browser
2. Drag and drop a PDF invoice into the upload area (or click to select one)
3. Wait for the processing to complete
4. View the extracted data in the form on the right
5. Use the PDF preview controls to navigate through the document

## Tech Stack

### Frontend
- React with TypeScript
- Vite
- Material-UI
- react-dropzone
- react-pdf

### Backend
- Flask
- PyPDF2
- OpenAI API
- python-dotenv

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.