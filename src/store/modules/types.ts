// store/modules/types.ts
export interface Reader {
  reader_id: number;
  user_id: string;
  address: string;
  balance: number;
  credit_level: number;
}

export interface Book {
  book_id: number;
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

export interface Inventory {
  inventory_id: number;
  book_id: number;
  location: string;
  status: 'available' | 'reserved' | 'sold';
}

export interface Author {
  author_id: number;
  book_id: number;
  name: string;
}

export interface BookShortage {
  shortage_id: number;
  book_id: number;
  supplier: string;
  quantity: number;
  record_date: Date;
}

export interface Order {
  order_id: number;
  reader_id: number;
  book_id: number;
  quantity: number;
  price: number;
  order_date: string;
  description: string;
  shipping_address: string;
  status: 'pending' | 'received' | 'shipped' | 'canceled';
}

export interface Supplier {
  supplier_id: number;
  name: string;
  phone: string;
  supply_info: string;
}

export interface ProcurementOrder {
  procurement_order_id: number;
  book_id: number;
  quantity: number;
  status: 'pending' | 'processed' | 'completed';
}