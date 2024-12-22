from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Book(Base):
    __tablename__ = "book"

    book_id = Column(Integer, primary_key=True, comment="Book ID")
    title = Column(String(100), nullable=False, comment="Book Title")
    publication_date = Column(DateTime, nullable=False, comment="Publication Date")
    price = Column(DECIMAL(10, 2), nullable=False, comment="Price")
    publisher = Column(String(100), nullable=False, comment="Publisher")
    keywords = Column(String(500), nullable=False, comment="Keywords")
    total_stock = Column(Integer, nullable=False, default=0, comment="Total Stock")
    supplier = Column(String(100), nullable=False, comment="Supplier")
    series_id = Column(Integer, nullable=False, comment="Series ID")

class User(Base):
    __tablename__ = "user"

    reader_id = Column(Integer, primary_key=True, comment="Reader ID")
    user_id = Column(String(20), nullable=False, comment="User ID")
    password = Column(String(20), nullable=False, comment="Password")
    address = Column(String(200), nullable=False, comment="Address")
    balance = Column(DECIMAL(10, 2), nullable=False, default=0, comment="Balance")
    credit_level = Column(Integer, nullable=False, default=1, comment="Credit Level")

class Order(Base):
    __tablename__ = "order"

    order_id = Column(Integer, primary_key=True, comment="Order ID")
    reader_id = Column(Integer, ForeignKey('user.reader_id'), nullable=False, comment="Reader ID")
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False, comment="Book ID")
    quantity = Column(Integer, nullable=False, comment="Quantity")
    price = Column(DECIMAL(10, 2), nullable=False, comment="Price")
    order_date = Column(DateTime, nullable=False, comment="Order Date")
    description = Column(String(500), nullable=True, comment="Description")
    shipping_address = Column(String(200), nullable=False, comment="Shipping Address")
    status = Column(String(20), nullable=False, comment="Order Status (pending, shipped, cancelled)")

class Shortage(Base):
    __tablename__ = "shortage"

    shortage_id = Column(Integer, primary_key=True, comment="Shortage ID")
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False, comment="Book ID")
    publisher = Column(String(100), nullable=False, comment="Publisher")
    supplier = Column(String(100), nullable=False, comment="Supplier")
    quantity = Column(Integer, nullable=False, comment="Quantity")
    record_date = Column(DateTime, nullable=False, default=lambda: datetime.now(datetime.timezone.utc), comment="Record Date")
    processed = Column(Boolean, nullable=False, default=False, comment="Processed")

class Procure(Base):
    __tablename__ = "procure"

    procurement_order_id = Column(Integer, primary_key=True, comment="Procurement Order ID")
    book_id = Column(Integer, ForeignKey('book.book_id'), nullable=False, comment="Book ID")
    quantity = Column(Integer, nullable=False, comment="Quantity")
    status = Column(String(20), nullable=False, comment="Procurement Status")

class Supplier(Base):
    __tablename__ = "supplier"

    supplier_id = Column(Integer, primary_key=True, comment="Supplier ID")
    name = Column(String(100), nullable=False, comment="Supplier Name")
    supply_info = Column(String(1000), nullable=False, comment="Supply Information")
