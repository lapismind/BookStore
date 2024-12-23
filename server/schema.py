from datetime import datetime, date
from dataclasses import dataclass
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from typing import Optional, List

class BookSchema(BaseModel):
    book_id: int
    series_id: int
    title: str
    author: list[str]
    publication_date: datetime
    price: float
    publisher: str
    keywords: str
    total_stock: int
    supplier: list[str]

    class Config:
        orm_mode = True

class BookCreate(BaseModel):
    book_id: str = Field(..., description="ISBN")
    series_id: int = Field(..., description="Series Number")
    title: str = Field(..., description="Book Title")
    author: list[str] = Field(..., description="Authors List")
    publication_date: Optional[datetime] = Field(None, description="Publication Date")
    price: Optional[float] = Field(None, ge=0, description="Price")
    publisher: Optional[str] = Field(None, description="Publisher")
    keywords: Optional[list[str]] = Field(None, description="Keywords")
    total_stock: Optional[int] = Field(None, ge=0, description="Total Stock")
    supplier: Optional[list[str]] = Field(None, description="Supplier")

    @validator('price')
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Price cannot be negative")
        return v

    @validator('total_stock')
    def validate_total_stock(cls, v):
        if v is not None and v < 0:
            raise ValueError("Total stock cannot be negative")
        return v
    

class BookResponse(BaseModel):
    book_id: str = Field(..., description="ISBN")
    series_id: int = Field(..., description="Series Number")
    title: str = Field(..., description="Book Title")
    author: List[str] = Field(..., description="Authors List")
    publication_date: Optional[datetime] = Field(
        None, description="Publication Date")
    price: Optional[float] = Field(None, description="Price")
    publisher: Optional[str] = Field(None, description="Publisher")
    keywords: Optional[List[str]] = Field(None, description="Keywords")
    total_stock: Optional[int] = Field(None, description="Total Stock")
    supplier: Optional[List[str]] = Field(None, description="Supplier")

    class Config:
        from_attributes = True  # 允许从 ORM 模型创建
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class BookGet(BaseModel):
    book_id: Optional[str] = Field(None, description="ISBN")
    series_id: Optional[int] = Field(None, description="Series Number")
    title: Optional[str] = Field(None, description="Book Title")
    publisher: Optional[str] = Field(None, description="Publisher")

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=20,
                         description="User ID")
    password: str = Field(..., min_length=6, max_length=20,
                          description="Password")
    address: str = Field(..., max_length=200, description="Address")

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v.strip():
            raise ValueError("User ID cannot be empty")
        return v.strip()

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError(
                "Password must contain at least one uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError(
                "Password must contain at least one lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    user_id: str = Field(..., min_length=1, max_length=20,
                         description="User ID")
    password: str = Field(..., min_length=1, max_length=20,
                          description="Password")

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    reader_id: int = Field(..., description="Reader ID")
    user_id: str = Field(..., description="User ID")
    address: str = Field(..., description="Address")
    balance: Decimal = Field(..., description="Balance")
    credit_level: int = Field(..., description="Credit Level")

    class Config:
        from_attributes = True
