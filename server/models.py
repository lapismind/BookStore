from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = "book_store_book"

    book_id = Column(Integer, primary_key=True, comment='书ID')
    title = Column(String(100, charset='utf8mb4'), nullable=False, comment='书名')
    author = Column(String(200, charset='utf8mb4'), nullable=False, comment='作者')
    publication_date = Column(DateTime, nullable=False, comment='出版时间')
    price = Column(DECIMAL(10, 2), nullable=False, comment='价格')
    publisher = Column(String(100, charset='utf8mb4'), nullable=False, comment='出版社')
    keywords = Column(String(500, charset='utf8mb4'), nullable=False, comment='关键字')
    total_stock = Column(Integer, nullable=False, default=0, comment='存货总量')
    supplier = Column(String(100, charset='utf8mb4'), nullable=False, comment='供书商')
    series_id = Column(Integer, nullable=False, comment='丛书号')

class Reader(Base):
    __tablename__ = "book_store_reader"

    reader_id = Column(Integer, primary_key=True, comment='读者ID')
    user_id = Column(String(20), nullable=False, comment='用户ID')
    address = Column(String(200, charset='utf8mb4'), nullable=False, comment='地址')
    balance = Column(DECIMAL(10, 2), nullable=False, default=0, comment='余额')
    credit_level = Column(Integer, nullable=False, default=1, comment='信用等级')

class Order(Base):
    __tablename__ = "book_store_order"

    order_id = Column(Integer, primary_key=True, comment='订单 ID')
    reader_id = Column(Integer, ForeignKey('book_store_reader.reader_id'), nullable=False, comment='读者 ID')
    book_id = Column(Integer, ForeignKey('book_store_book.book_id'), nullable=False, comment='书 ID')
    quantity = Column(Integer, nullable=False, comment='订购数量')
    price = Column(DECIMAL(10, 2), nullable=False, comment='价格')
    order_date = Column(DateTime, nullable=False, comment='时间')
    description = Column(String(500, charset='utf8mb4'), nullable=True, comment='描述')
    shipping_address = Column(String(200, charset='utf8mb4'), nullable=False, comment='发货地址')
    status = Column(String(20, charset='utf8mb4'), nullable=False, comment='订单状态(pending,received,shipped,canceled)')

class Supplier(Base):
    __tablename__ = "book_store_supplier"

    supplier_id = Column(Integer, primary_key=True, comment='供应商 ID')
    name = Column(String(100, charset='utf8mb4'), nullable=False, comment='供应商名称')
    phone = Column(String(20), nullable=False, comment='电话号码')
    supply_info = Column(String(1000, charset='utf8mb4'), nullable=False, comment='供货信息')

class Inventory(Base):
    __tablename__ = "book_store_inventory"

    inventory_id = Column(Integer, primary_key=True, comment='库存 ID')
    book_id = Column(Integer, ForeignKey('book_store_book.book_id'), nullable=False, comment='书 ID')
    location = Column(String(100, charset='utf8mb4'), nullable=False, comment='存放位置')
    status = Column(String(20, charset='utf8mb4'), nullable=False, comment='状态(available,reserved,sold)')

