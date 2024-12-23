import io
import json
import os
import time
from http import HTTPStatus

import numpy as np
from kui.asgi import Body, HTTPException, JSONResponse, Routes, StreamResponse, request
from decimal import Decimal
from loguru import logger
from typing_extensions import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server.models import *
from server.schema import *
from server.tools import *

MAX_NUM_SAMPLES = int(os.getenv("NUM_SAMPLES", 1))

routes = Routes()

@routes.http.post("/book/add")
async def add_book(req: Annotated[BookCreate, Body(exclusive=True)]):
    '''
        POST /book/add
        {
            "book_id": "1000000000010",
            "series_id": 1,
            "title": "The Test Book",
            "author": ["Test Author"],
            "publication_date": str(date.today()),
            "price": 29.99,
            "publisher": "Test Publisher",
            "keywords": ["test", "programming"],
            "total_stock": 100,
            "supplier": ["Test Supplier"]
        }

        success response: 201
        {
            "book_id": "1000000000010",
            "series_id": 1,
            "title": "The Test Book",
            "author": ["Test Author"],
            "publication_date": str(date.today()),
            "price": 29.99,
            "publisher": "Test Publisher",
            "keywords": ["test", "programming"],
            "total_stock": 100,
            "supplier": ["Test Supplier"]
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        new_book = Book(
            book_id=req.book_id,
            series_id=req.series_id,
            title=req.title,
            author=req.author,
            publication_date=req.publication_date,
            price=req.price,
            publisher=req.publisher,
            keywords=req.keywords,
            total_stock=req.total_stock,
            supplier=req.supplier
        )
        db.add(new_book)
        db.commit()
        db.refresh(new_book)

        response_data = BookResponse.from_orm(new_book)
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=response_data.model_dump()
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding book: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Error adding book")
    finally:
        db.close()


@routes.http.post("/book/get")
async def get_book(req: Annotated[BookGet, Body(exclusive=True)]):
    '''
        POST /book/get
        {
            "book_id": "1000000000010",
            "series_id": 1
        }

        success response: 200
        {
            "book_id": "1000000000010",
            "series_id": 1,
            "title": "The Test Book",
            "author": ["Test Author"],
            "publication_date": str(date.today()),
            "price": 29.99,
            "publisher": "Test Publisher",
            "keywords": ["test", "programming"],
            "total_stock": 100,
            "supplier": ["Test Supplier"]
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        query = db.query(Book)

        if req.book_id:
            query = query.filter(Book.book_id == req.book_id)
        if req.series_id is not None:
            query = query.filter(Book.series_id == req.series_id)
        if req.title:
            query = query.filter(Book.title.like(f"%{req.title}%"))
        if req.publisher:
            query = query.filter(Book.publisher.like(f"%{req.publisher}%"))

        books = query.all()

        if not books:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                message="No books found matching the criteria"
            )

        response_data = [
            BookResponse(
                book_id=book.book_id,
                series_id=book.series_id,
                title=book.title,
                author=json.loads(book.author) if isinstance(
                    book.author, str) else book.author,
                publication_date=book.publication_date,
                price=book.price,
                publisher=book.publisher,
                keywords=json.loads(book.keywords) if book.keywords and isinstance(
                    book.keywords, str) else book.keywords,
                total_stock=book.total_stock,
                supplier=json.loads(book.supplier) if book.supplier and isinstance(
                    book.supplier, str) else book.supplier
            ).model_dump()
            for book in books
        ]

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"books": response_data}
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error getting books: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error retrieving books"
        )
    finally:
        db.close()


@routes.http.post("/user/register")
async def register_user(req: Annotated[UserCreate, Body(exclusive=True)]):
    '''
        POST /user/register
        {
            "user_id": "john_doe",
            "password": "Password123",
            "address": "123 Main St, City"
        }

        success response: 201
        {
            "reader_id": 1,
            "user_id": "john_doe",
            "address": "123 Main St, City",
            "balance": "0.00",
            "credit_level": 1
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(
            User.user_id == req.user_id).first()
        if existing_user:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                message="User ID already exists"
            )

        new_user = User(
            user_id=req.user_id,
            password=req.password,
            address=req.address,
            balance=Decimal('0.00'),
            credit_level=1
        )
        new_user.reader_id = db.query(User).count() + 1

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        response_data = UserResponse.from_orm(new_user)
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=response_data.model_dump()
        )

    except HTTPException as he:
        raise he
    except ValueError as ve:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            message=str(ve)
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Error registering user: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error registering user"
        )
    finally:
        db.close()


@routes.http.post("/user/login")
async def login_user(req: Annotated[UserLogin, Body(exclusive=True)]):
    '''
        POST /user/login
        {
            "user_id": "john_doe",
            "password": "Password123"
        }

        success response: 200
        {
            "message": "Login successful",
            "user": {
                "reader_id": 1,
                "user_id": "john_doe",
                "address": "123 Main St, City",
                "balance": "0.00",
                "credit_level": 1
            }
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.user_id == req.user_id,
            User.password == req.password
        ).first()

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                message="Invalid user ID or password"
            )

        response_data = UserResponse(
            reader_id=user.reader_id,
            user_id=user.user_id,
            address=user.address,
            balance=user.balance,
            credit_level=user.credit_level
        )

        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": "Login successful",
                "user": response_data.model_dump()
            }
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error during login: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error processing login request"
        )
    finally:
        db.close()


@routes.http.post("/user/update_balance")
async def update_balance(
    reader_id: int,
    amount: Decimal
):
    '''
        POST /user/update_balance
        {
            "reader_id": 1,
            "amount": 2000.00
        }

        success response: 200
        {
            "message": "Balance updated successfully",
            "credit_level_updated": true,
            "user": {
                "reader_id": 1,
                "user_id": "john_doe",
                "address": "123 Main St, City",
                "balance": "2000.00",
                "credit_level": 2
            }
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.reader_id == reader_id).first()
        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                message="User not found"
            )
        
        user.balance += amount

        credit_level_updated = update_credit_level(user, db)

        response_data = UserResponse.from_orm(user)
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": "Balance updated successfully",
                "credit_level_updated": credit_level_updated,
                "user": response_data.model_dump()
            }
        )

    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating balance: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error updating balance"
        )
    finally:
        db.close()


@routes.http.post("/order/add")
async def create_order(req: Annotated[OrderCreate, Body(exclusive=True)]):
    '''
        POST /order/add
        {
            "reader_id": 1,
            "book_id": "9780123456789",
            "series_id": 1,
            "quantity": 2,
            "shipping_address": "123 Main St, City",
            "description": "Gift wrapping needed"
        }

        success response:
        {
            "message": "Order created successfully",
            "order_id": 1,
            "status": "pending"
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        book = db.query(Book).filter(
            Book.book_id == req.book_id,
            Book.series_id == req.series_id
        ).first()
        
        if not book:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                message="Book not found"
            )
        
        if book.stock < req.quantity:
            order = Order(
                reader_id=req.reader_id,
                book_id=req.book_id,
                series_id=req.series_id,
                quantity=req.quantity,
                price=book.price * req.quantity,
                order_date=datetime.now(),
                description=req.description,
                shipping_address=req.shipping_address,
                status="cancelled"
            )
            db.add(order)
            db.commit()
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "Order created but cancelled due to insufficient stock",
                    "order_id": order.order_id,
                    "status": "cancelled"
                }
            )
        
        user = db.query(User).filter(User.reader_id == req.reader_id).first()
        total_price = book.price * req.quantity
        
        if user.balance < total_price:
            order = Order(
                reader_id=req.reader_id,
                book_id=req.book_id,
                series_id=req.series_id,
                quantity=req.quantity,
                price=total_price,
                order_date=datetime.now(),
                description=req.description,
                shipping_address=req.shipping_address,
                status="cancelled"
            )
            db.add(order)
            db.commit()
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "Order created but cancelled due to insufficient balance",
                    "order_id": order.order_id,
                    "status": "cancelled"
                }
            )
        
        order = Order(
            reader_id=req.reader_id,
            book_id=req.book_id,
            series_id=req.series_id,
            quantity=req.quantity,
            price=total_price,
            order_date=datetime.now(),
            description=req.description,
            shipping_address=req.shipping_address,
            status="pending"
        )
        
        book.stock -= req.quantity
        user.balance -= total_price
        
        db.add(order)
        db.commit()
        
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": "Order created successfully",
                "order_id": order.order_id,
                "status": "pending"
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating order: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error processing order"
        )
    finally:
        db.close()


@routes.http.post("/order/ship")
async def ship_order(req: Annotated[OrderStatusUpdate, Body(exclusive=True)]):
    '''
        POST /order/ship
        {
            "order_id": 1
        }

        success response:
        {
            "message": "Order shipped successfully",
            "order_id": 1,
            "status": "shipped"
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_id == req.order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                message="Order not found"
            )
        
        if order.status != "pending":
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Cannot ship order in {order.status} status"
            )
        
        order.status = "shipped"
        db.commit()
        
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": "Order shipped successfully",
                "order_id": order.order_id,
                "status": "shipped"
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error shipping order: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error processing shipping request"
        )
    finally:
        db.close()


@routes.http.post("/order/receive")
async def receive_order(req: Annotated[OrderStatusUpdate, Body(exclusive=True)]):
    '''
        POST /order/receive
        {
            "order_id": 1
        }

        success response:
        {
            "message": "Order completed successfully",
            "order_id": 1,
            "status": "completed"
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        order = db.query(Order).filter(Order.order_id == req.order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                message="Order not found"
            )
        
        if order.status != "shipped":
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                message=f"Cannot receive order in {order.status} status"
            )
        
        order.status = "completed"
        db.commit()
        
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": "Order completed successfully",
                "order_id": order.order_id,
                "status": "completed"
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error completing order: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error processing receive request"
        )
    finally:
        db.close()

