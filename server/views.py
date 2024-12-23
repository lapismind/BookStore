import json
import os
import time
from http import HTTPStatus

from kui.asgi import Body, HTTPException, JSONResponse, Routes, StreamResponse, request
from decimal import Decimal
from loguru import logger
from typing_extensions import Annotated
from sqlalchemy import func, tuple_
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


@routes.http.get("/user/query")
async def query_user(
    user_id: Optional[str] = None,
    reader_id: Optional[int] = None
):
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        query = db.query(User)
        if user_id:
            query = query.filter(User.user_id == user_id)
        if reader_id:
            query = query.filter(User.reader_id == reader_id)

        records = query.all()
        if not records:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="No matching users found"
            )

        data = [UserResponse.from_orm(u).model_dump() for u in records]
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={"users": data}
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error querying user: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error querying user"
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
                if_paid=req.if_paid,
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
        
        # Determine discount and overdraft allowance based on user's credit level
        discount_map = {
            1: 0.10,
            2: 0.15,
            3: 0.15,
            4: 0.20,
            5: 0.25
        }

        overdraft_map = {
            1: 0,
            2: 0,
            3: 1000,
            4: 2000,
            5: float('inf')
        }
        overdraft_allowed_levels = {3, 4, 5}
        
        discount_rate = discount_map.get(user.credit_level, 0.0)
        discounted_price = book.price * req.quantity * (1 - discount_rate)
        dilivery_balance = user.balance + overdraft_map.get(user.credit_level, 0.0)

        if book.price > dilivery_balance or (req.if_paid & user.credit_level not in overdraft_allowed_levels):
            order = Order(
            reader_id=req.reader_id,
            book_id=req.book_id,
            series_id=req.series_id,
            quantity=req.quantity,
            price=discounted_price,
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
        
        total_price = discounted_price

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
        if req.if_paid:
            user.balance -= total_price
        
        _ = update_credit_level(user, db)
        
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
        
        if not order.if_paid:
            user = db.query(User).filter(User.reader_id == order.reader_id).first()
            user.update(
                {"balance": User.balance - order.price},
                synchronize_session=False
            )
            _ = update_credit_level(user, db)
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


@routes.http.post("/shortage/add")
async def create_shortage(req: Annotated[ShortageCreate, Body(exclusive=True)]):
    '''
        POST /shortage/add
        {
            "book_id": "9780123456789",
            "series_id": 1,
            "publisher": "Sample Publisher",
            "supplier": "Sample Supplier",
            "quantity": 50
        }

        success response: 201
        {
            "message": "Shortage record created successfully",
            "shortage": {
                "shortage_id": 1,
                "book_id": "9780123456789",
                "series_id": 1,
                "publisher": "Sample Publisher",
                "supplier": "Sample Supplier",
                "quantity": 50,
                "record_date": "2024-12-23T18:06:00+00:00",
                "processed": false
            }
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
        
        existing_shortage = db.query(Shortage).filter(
            Shortage.book_id == req.book_id,
            Shortage.series_id == req.series_id,
            Shortage.processed == False
        ).first()
        
        if existing_shortage:
            existing_shortage.quantity += req.quantity
            existing_shortage.record_date = datetime.now(datetime.timezone.utc)
            db.commit()
            
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "Existing shortage record updated",
                    "shortage_id": existing_shortage.shortage_id,
                    "total_quantity": existing_shortage.quantity
                }
            )
        
        shortage = Shortage(
            book_id=req.book_id,
            series_id=req.series_id,
            publisher=req.publisher,
            supplier=req.supplier,
            quantity=req.quantity,
            record_date=datetime.now(datetime.timezone.utc),
            processed=False
        )
        
        db.add(shortage)
        db.commit()
        
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content={
                "message": "Shortage record created successfully",
                "shortage": {
                    "shortage_id": shortage.shortage_id,
                    "book_id": shortage.book_id,
                    "series_id": shortage.series_id,
                    "publisher": shortage.publisher,
                    "supplier": shortage.supplier,
                    "quantity": shortage.quantity,
                    "record_date": shortage.record_date.isoformat(),
                    "processed": shortage.processed
                }
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating shortage record: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error creating shortage record"
        )
    finally:
        db.close()


@routes.http.get("/shortage/list")
async def list_shortages(
    processed: Optional[bool] = None,
    book_id: Optional[str] = None,
    series_id: Optional[int] = None
):
    '''
        GET /shortage/list?processed=false

        success response: 200
        {
            "shortages": [
                {
                    "shortage_id": 1,
                    "book_id": "9780123456789",
                    "series_id": 1,
                    "publisher": "Sample Publisher",
                    "supplier": "Sample Supplier",
                    "quantity": 50,
                    "record_date": "2024-12-23T18:06:00+00:00",
                    "processed": false
                }
                // ... extra records
            ]
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        query = db.query(Shortage)
        
        if processed is not None:
            query = query.filter(Shortage.processed == processed)
        if book_id:
            query = query.filter(Shortage.book_id == book_id)
        if series_id:
            query = query.filter(Shortage.series_id == series_id)
            
        shortages = query.order_by(Shortage.record_date.desc()).all()
        
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "shortages": [
                    {
                        "shortage_id": s.shortage_id,
                        "book_id": s.book_id,
                        "series_id": s.series_id,
                        "publisher": s.publisher,
                        "supplier": s.supplier,
                        "quantity": s.quantity,
                        "record_date": s.record_date.isoformat(),
                        "processed": s.processed
                    }
                    for s in shortages
                ]
            }
        )
        
    except Exception as e:
        logger.error(f"Error listing shortage records: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error retrieving shortage records"
        )
    finally:
        db.close()


@routes.http.post("/procure/create")
async def create_procurement_orders():
    '''
        POST /procure/create

        success response: 201
        {
            "message": "Procurement orders created successfully",
            "orders": [
                {
                    "book_id": "9780123456789",
                    "series_id": 1,
                    "quantity": 50,
                    "publisher": "Sample Publisher",
                    "supplier": "Sample Supplier"
                }
                // ... extra records
            ]
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        shortages = db.query(
            Shortage.book_id,
            Shortage.series_id,
            Shortage.publisher,
            Shortage.supplier,
            func.sum(Shortage.quantity).label('total_quantity')
        ).filter(
            Shortage.processed == False
        ).group_by(
            Shortage.book_id,
            Shortage.series_id,
            Shortage.publisher,
            Shortage.supplier
        ).all()
        
        if not shortages:
            return JSONResponse(
                status_code=HTTPStatus.OK,
                content={
                    "message": "No pending shortages found"
                }
            )
        
        created_orders = []
        for shortage in shortages:
            procure = Procure(
                book_id=shortage.book_id,
                series_id=shortage.series_id,
                quantity=shortage.total_quantity,
                status="pending"
            )
            db.add(procure)
            created_orders.append({
                "book_id": shortage.book_id,
                "series_id": shortage.series_id,
                "quantity": shortage.total_quantity,
                "publisher": shortage.publisher,
                "supplier": shortage.supplier
            })
        
        db.query(Shortage).filter(
            Shortage.processed == False
        ).update(
            {"processed": True},
            synchronize_session=False
        )
        
        db.commit()
        
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content={
                "message": "Procurement orders created successfully",
                "orders": created_orders
            }
        )
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating procurement orders: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error creating procurement orders"
        )
    finally:
        db.close()


@routes.http.post("/procure/complete")
async def complete_procurement(req: Annotated[ProcureComplete, Body(exclusive=True)]):
    '''
        POST /procure/complete
        {
            "procurement_order_id": 1
        }

        success response: 200
        {
            "message": "Procurement completed successfully",
            "procurement_order_id": 1,
            "book_id": "9780123456789",
            "series_id": 1,
            "quantity": 50,
            "new_stock": 150
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        procure = db.query(Procure).filter(
            Procure.procurement_order_id == req.procurement_order_id
        ).first()
        
        if not procure:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                message="Procurement order not found"
            )
        
        if procure.status == "completed":
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                message="Procurement order already completed"
            )
        
        book = db.query(Book).filter(
            Book.book_id == procure.book_id,
            Book.series_id == procure.series_id
        ).first()
        
        if not book:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                message="Book not found"
            )
        
        book.stock += procure.quantity
        
        procure.status = "completed"
        
        db.query(Shortage).filter(
            Shortage.book_id == procure.book_id,
            Shortage.series_id == procure.series_id,
            Shortage.processed == True
        ).delete(synchronize_session=False)
        
        db.commit()
        
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "message": "Procurement completed successfully",
                "procurement_order_id": procure.procurement_order_id,
                "book_id": procure.book_id,
                "series_id": procure.series_id,
                "quantity": procure.quantity,
                "new_stock": book.stock
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error completing procurement: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error completing procurement"
        )
    finally:
        db.close()


@routes.http.get("/procure/list")
async def list_procurements(
    status: Optional[str] = None,
    book_id: Optional[str] = None,
    series_id: Optional[int] = None
):
    '''
        GET /procure/list?status=pending

        success response: 200
        {
            "procurements": [
                {
                    "procurement_order_id": 2,
                    "book_id": "9780123456789",
                    "series_id": 1,
                    "quantity": 30,
                    "status": "pending"
                }
                // ... extra records
            ]
        }
    '''
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        query = db.query(Procure)
        
        if status:
            query = query.filter(Procure.status == status)
        if book_id:
            query = query.filter(Procure.book_id == book_id)
        if series_id:
            query = query.filter(Procure.series_id == series_id)
            
        procurements = query.all()
        
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "procurements": [
                    {
                        "procurement_order_id": p.procurement_order_id,
                        "book_id": p.book_id,
                        "series_id": p.series_id,
                        "quantity": p.quantity,
                        "status": p.status
                    }
                    for p in procurements
                ]
            }
        )
        
    except Exception as e:
        logger.error(f"Error listing procurements: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error retrieving procurement list"
        )
    finally:
        db.close()


@routes.http.post("/supplier/add")
async def create_supplier(req: Annotated[SupplierCreate, Body(exclusive=True)]):
    """
        POST /supplier/add
        {
            "name": "Sample Supplier",
            "book_list": [
                {
                    "book_id": "9780123456789",
                    "series_id": 1
                },
                {
                    "book_id": "9780123456790",
                    "series_id": 2
                }
            ]
        }

        success response: 201

        {
            "message": "Supplier created successfully",
            "supplier": {
                "supplier_id": 1,
                "name": "Sample Supplier",
                "book_list": [
                    {
                        "book_id": "9780123456789",
                        "series_id": 1
                    },
                    {
                        "book_id": "9780123456790",
                        "series_id": 2
                    }
                ]
            }
        }
    """
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        book_ids = [(book['book_id'], book['series_id']) for book in req.book_list]
        existing_books = db.query(Book).filter(
            tuple_(Book.book_id, Book.series_id).in_(book_ids)
        ).all()
        
        if len(existing_books) != len(book_ids):
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                message="Some books in the list do not exist"
            )
        
        existing_supplier = db.query(Supplier).filter(
            Supplier.name == req.name
        ).first()
        
        if existing_supplier:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                message="Supplier name already exists"
            )
        
        supplier = Supplier(
            name=req.name,
            book_list=req.book_list
        )
        db.add(supplier)
        
        for book in existing_books:
            if not book.suppliers:
                book.suppliers = []
            
            if supplier.supplier_id not in book.suppliers:
                book.suppliers.append(supplier.supplier_id)
        
        db.commit()
        
        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content={
                "message": "Supplier created successfully",
                "supplier": {
                    "supplier_id": supplier.supplier_id,
                    "name": supplier.name,
                    "book_list": supplier.book_list
                }
            }
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating supplier: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error creating supplier"
        )
    finally:
        db.close()


@routes.http.get("/supplier/query")
async def query_suppliers(
    supplier_id: Optional[int] = None,
    name: Optional[str] = None,
    book_id: Optional[str] = None,
    series_id: Optional[int] = None
):
    """
        query all suppliers
        GET /supplier/query

        query by supplier id
        GET /supplier/query?supplier_id=1

        query by name (case-insensitive)
        GET /supplier/query?name=Sample

        query by book_id
        GET /supplier/query?book_id=9780123456789&series_id=1

        success response: 200
        {
            "suppliers": [
                {
                    "supplier_id": 1,
                    "name": "Sample Supplier",
                    "books": [
                        {
                            "book_id": "9780123456789",
                            "series_id": 1,
                            "title": "Sample Book",
                            "author": "Sample Author",
                            "price": 29.99
                        },
                        {
                            "book_id": "9780123456790",
                            "series_id": 2,
                            "title": "Another Book",
                            "author": "Another Author",
                            "price": 19.99
                        }
                    ]
                }
            ]
        }
    """
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        query = db.query(Supplier)
        
        if supplier_id:
            query = query.filter(Supplier.supplier_id == supplier_id)
        if name:
            query = query.filter(Supplier.name.ilike(f"%{name}%"))
        if book_id or series_id:
            if book_id and series_id:
                query = query.filter(
                    Supplier.book_list.contains([
                        {"book_id": book_id, "series_id": series_id}
                    ])
                )
            elif book_id:
                query = query.filter(
                    Supplier.book_list.contains([
                        {"book_id": book_id}
                    ])
                )
            elif series_id:
                query = query.filter(
                    Supplier.book_list.contains([
                        {"series_id": series_id}
                    ])
                )
        
        suppliers = query.all()
        
        book_details = {}
        book_ids = set()
        for supplier in suppliers:
            for book in supplier.book_list:
                book_ids.add((book['book_id'], book['series_id']))
        
        if book_ids:
            books = db.query(Book).filter(
                tuple_(Book.book_id, Book.series_id).in_(book_ids)
            ).all()
            book_details = {
                (book.book_id, book.series_id): {
                    "title": book.title,
                    "author": book.author,
                    "price": float(book.price)
                }
                for book in books
            }
        
        return JSONResponse(
            status_code=HTTPStatus.OK,
            content={
                "suppliers": [
                    {
                        "supplier_id": s.supplier_id,
                        "name": s.name,
                        "books": [
                            {
                                "book_id": book['book_id'],
                                "series_id": book['series_id'],
                                **book_details.get((book['book_id'], book['series_id']), {})
                            }
                            for book in s.book_list
                        ]
                    }
                    for s in suppliers
                ]
            }
        )
        
    except Exception as e:
        logger.error(f"Error querying suppliers: {e}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            message="Error querying suppliers"
        )
    finally:
        db.close()
