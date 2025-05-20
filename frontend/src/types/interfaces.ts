export interface IDocumentTypes {
  invoice: IInvoice;
  spec: ISpec;
  quote: IQuote;
  submittal: ISubmittal;
}

export interface IAddress {
  company_name: string | null;
  address_line_1: string | null;
  address_line_2: string | null;
  city: string | null;
  state: string | null;
  zip: string | null;
}

export interface ILineItem {
  spec_tag: string | null;
  description: string | null;
  quantity: number | null;
  units: string | null;
  overage: number | null;
  discount: number | null;
  unit_price: number | null;
  extended_price: number | null;
  fob: string | null;
}

export interface IInvoice {
  vendor_name: string | null;
  invoice_date: Date | null;
  due_date: Date | null;
  ship_date: Date | null;
  invoice_number: string | null;
  vendor_order_number: string | null;
  account_number: string | null;
  po_number: string | null;
  terms: string | null;
  banking_info: string | null;
  currency: string | null;
  bill_to_address: IAddress;
  ship_to_address: IAddress;
  invoice_items: ILineItem[];
  subtotal: number | null;
  packaging_fee: number | null;
  freight: number | null;
  sales_tax: number | null;
  sales_tax_rate: number | null;
  total: number | null;
  prepayments_deposit: number | null;
  balance_due: number | null;
}

export interface ISpec {
  tag: string | null;
  description: string | null;
  quantity: number | null;
}

export interface IQuote {
  quote_number: string | null;
  quote_date: Date | null;
  expiration_date: Date | null;
  customer_name: string | null;
  customer_address: IAddress;
  line_items: ILineItem[];
}

export interface ISubmittal {
  submittal_number: string | null;
  submittal_date: Date | null;
  spec_tag: ISpec;
}

