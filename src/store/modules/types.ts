// store/modules/types.ts
export interface Reader {
  reader_id: number;
  user_id: string;
  address: string;
  balance: number;
  credit_level: number;
}
export type ReaderList = Reader[];

export interface Book {
  book_id: string;
  title: string;
  author: string;
  publication_date: Date;
  price: number;
  publisher: string;
  keywords: string;
  total_stock: number;
  supplier: string;
  series_id: number;
}

export type BookList = Book[];

export interface BookShortage {
  shortage_id: number;
  book_id: string;
  supplier: string;
  quantity: number;
  record_date: Date;
  processed: boolean;
}

export interface Order {
  order_id: number;
  reader_id: number;
  book_id: string;
  quantity: number;
  price: number;
  order_date: Date;
  shipping_address: string;
  status: 'pending' | 'shipped'  | 'cancelled';
}

export interface ProcurementOrder {
  procurement_order_id: number;
  book_id: string;
  quantity: number;
  status: 'processing' | 'completed';
}

export interface Supplier {
  supplier_id: number;
  name: string;
  supply_info: string;
}
