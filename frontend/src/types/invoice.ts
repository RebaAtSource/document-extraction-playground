export interface IAddress {
  company_name: string | null;
  address_line_1: string | null;
  address_line_2: string | null;
  city: string | null;
  state: string | null;
  zip: string | null;
}

export interface IInvoice {
  vendor_name: string | null;
  invoice_date: string | null;
  invoice_number: string | null;
  vendor_order_number: string | null;
  account_number: string | null;
  bill_to_address: IAddress;
  ship_to_address: IAddress;
  source_po_number: string | null;
  packaging_fee: string | null;
  total: string | null;
  sales_tax: string | null;
  freight_shipping: string | null;
  terms: string | null;
  banking_info: string | null;
  due_date: string | null;
  currency: string | null;
  prepayments_deposit: string | null;
  balance_due: string | null;
} 