export interface IAddress {
  company_name: string | null;
  address_line_1: string | null;
  address_line_2: string | null;
  city: string | null;
  state: string | null;
  zip: string | null;
}

export interface IItem {
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
  invoice_items: IItem[];
  subtotal: number | null;
  packaging_fee: number | null;
  freight: number | null;
  sales_tax: number | null;
  sales_tax_rate: number | null;
  total: number | null;
  prepayments_deposit: number | null;
  balance_due: number | null;
} 