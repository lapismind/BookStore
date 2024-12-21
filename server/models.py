from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True, comment='书 ID')
    title = Column(String(100, charset='utf8mb4'), nullable=False, comment='书名')
    publication_date = Column(DateTime, nullable=False, comment='出版时间')
    price = Column(DECIMAL(10, 2), nullable=False, comment='价格')
    publisher = Column(String(100, charset='utf8mb4'), nullable=False, comment='出版社')
    keywords = Column(String(500, charset='utf8mb4'), nullable=False, comment='关键字')
    total_stock = Column(Integer, nullable=False, default=0, comment='存货总量')
    supplier = Column(String(100, charset='utf8mb4'), nullable=False, comment='供书商')
    series_id = Column(Integer, nullable=False, comment='丛书号')

class User(Base):
    __tablename__ = "user"

    reader_id = Column(Integer, primary_key=True, comment='读者 ID')
    user_id = Column(String(20), nullable=False, comment='用户 ID')
    password = Column(String(20), nullable=False, comment='密码')
    address = Column(String(200, charset='utf8mb4'), nullable=False, comment='地址')
    balance = Column(DECIMAL(10, 2), nullable=False, default=0, comment='余额')
    credit_level = Column(Integer, nullable=False, default=1, comment='信用等级')

class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True, comment='订单 ID')
    reader_id = Column(Integer, ForeignKey('user.reader_id'), nullable=False, comment='读者 ID')
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False, comment='书 ID')
    quantity = Column(Integer, nullable=False, comment='订购数量')
    price = Column(DECIMAL(10, 2), nullable=False, comment='价格')
    order_date = Column(DateTime, nullable=False, comment='时间')
    description = Column(String(500, charset='utf8mb4'), nullable=True, comment='描述')
    shipping_address = Column(String(200, charset='utf8mb4'), nullable=False, comment='发货地址')
    status = Column(String(20, charset='utf8mb4'), nullable=False, comment='订单状态(pending,shipped,canceled)')

class Shortage(Base):
    __tablename__ = "shortage"

    shortage_id = Column(Integer, primary_key=True, comment='缺书登记 ID')
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False, comment='书 ID')
    publisher = Column(String(100, charset='utf8mb4'), nullable=False, comment='出版社')
    supplier = Column(String(100, charset='utf8mb4'), nullable=False, comment='供书商')
    quantity = Column(Integer, nullable=False, comment='数量')
    record_date = Column(DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc), comment='登记日期')
    processed = Column(Boolean, nullable=False, default=False, comment='是否已被处理')

class Procure(Base):
    __tablename__ = "procure"

    procurement_order_id = Column(Integer, primary_key=True, comment='采购单 ID')
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False, comment='书 ID')
    quantity = Column(Integer, nullable=False, comment='采购数量')
    status = Column(String(20, charset='utf8mb4'), nullable=False, comment='采购单状态')

class Supplier(Base):
    __tablename__ = "supplier"

    supplier_id = Column(Integer, primary_key=True, comment='供应商 ID')
    name = Column(String(100, charset='utf8mb4'), nullable=False, comment='供应商名称')
    supply_info = Column(String(1000, charset='utf8mb4'), nullable=False, comment='供货信息')
