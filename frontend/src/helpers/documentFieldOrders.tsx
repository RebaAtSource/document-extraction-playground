import { IInvoice, ISpec, IQuote, ISubmittal } from "../types/interfaces";

// Define field orders for different document types
const InvoiceFieldOrder: (keyof IInvoice)[] = [
  "vendor_name",
  "invoice_date",
  "due_date",
  "ship_date",
  "invoice_number",
  "vendor_order_number",
  "account_number",
  "po_number",
  "terms",
  "banking_info",
  "currency",
  "bill_to_address",
  "ship_to_address",
  "invoice_items",
  "subtotal",
  "packaging_fee",
  "freight",
  "sales_tax",
  "sales_tax_rate",
  "total",
  "prepayments_deposit",
  "balance_due"
];

const SpecFieldOrder: (keyof ISpec)[] = [
  "tag",
  "description",
  "quantity"
];

const QuoteFieldOrder: (keyof IQuote)[] = [
  "quote_number",
  "quote_date",
  "expiration_date",
  "customer_name",
  "customer_address",
  "line_items"
];

const SubmittalFieldOrder: (keyof ISubmittal)[] = [
  "submittal_number",
  "submittal_date",
  "spec_tag"
];

// Mapping of types to their field orders
const typeToFieldOrderMap = {
  "invoice": InvoiceFieldOrder,
  "spec": SpecFieldOrder,
  "quote": QuoteFieldOrder,
  "submittal": SubmittalFieldOrder,
};

function transformDocumentData(data: Record<string, any>, documentType: keyof typeof typeToFieldOrderMap) {
  const fieldOrder = typeToFieldOrderMap[documentType];

  if (!fieldOrder) {
    throw new Error('No field order found for the provided data type.');
  }

  const transformedData: Record<string, any> = {};

  Object.entries(data).forEach(([key, value]) => {
    const transformedEntry: Record<string, any> = {};

    fieldOrder.forEach((field) => {
      if (field.includes('address')) {
        transformedEntry[field] = {
          company_name: ((value as Record<string, any>)[field])?.company_name || null,
          address_line_1: ((value as Record<string, any>)[field])?.address_line_1 || null,
          address_line_2: ((value as Record<string, any>)[field])?.address_line_2 || null,
          city: ((value as Record<string, any>)[field])?.city || null,
          state: ((value as Record<string, any>)[field])?.state || null,
          zip: ((value as Record<string, any>)[field])?.zip || null,
        };
      } else {
        transformedEntry[field] = (value as Record<string, any>)[field] || null;
      }
    });

    transformedData[key] = transformedEntry;
  });

  return transformedData;
}

// Define an enum for document types
enum DocumentType {
  Invoice = 'invoice',
  Spec = 'spec',
  Quote = 'quote',
  Submittal = 'submittal',
}

export { transformDocumentData, DocumentType };