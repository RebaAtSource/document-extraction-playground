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
  unit_price: number | null;
}

export interface IInvoice {
  vendor_name: string | null;
  invoice_date: Date | null;
  due_date: Date | null;
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
  packaging_fee: number | null;
  freight: number | null;
  sales_tax: number | null;
  total: number | null;
  prepayments_deposit: number | null;
  balance_due: number | null;
} 