// src/store/modules/record.ts

export interface BookShortage {
  shortage_id: number;
  book_id: number;
  supplier: string;
  quantity: number;
  record_date: Date;
}

// 其他可能相关的类型定义
export interface ShortageRecordForm {
  book_id: number;
  supplier: string;
  quantity: number;
}
