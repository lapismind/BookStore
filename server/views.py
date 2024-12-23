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

        # 创建新用户
        new_user = User(
            user_id=req.user_id,
            password=req.password,
            address=req.address,
            balance=Decimal('0.00'),
            credit_level=1
        )

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

        # 构建响应
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
