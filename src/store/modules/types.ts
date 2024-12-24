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
  series_id: number;
  title: string;
  author: string[];
  publication_date: string;
  price: number;
  publisher: string;
  keywords: string[];
  total_stock: number;
  supplier: string[];
}

export type BookList = Book[];

export interface BookShortage {
  shortage_id: number;
  book_id: string;
  series_id: number;
  publisher: string;
  supplier: string;
  quantity: number;
  record_date: string;
  processed: boolean;
}

export interface Order {
  order_id: number;
  reader_id: number;
  book_id: string;
  series_id: number;
  quantity: number;
  price: number;
  order_date: string;
  shipping_address: string;
  if_paid: boolean;
  status: 'pending' | 'shipped' | 'cancelled';
}

export interface ProcurementOrder {
  procurement_order_id: number;
  book_id: string;
  series_id: number;
  quantity: number;
  status: 'pending' | 'completed';
}

export interface Supplier {
  supplier_id: number;
  name: string;
  book_list: { book_id: string; series_id: number }[];
}