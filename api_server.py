from threading import Lock
import re

import pyrootutils
import uvicorn
from kui.asgi import FactoryClass, HTTPException, HttpRoute, Kui, OpenAPI, Routes
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

pyrootutils.setup_root(__file__, indicator=".project-root", pythonpath=True)

from server.api_utils import parse_args
from server.exception_handler import ExceptionHandler
from server.db_manager import DatabaseManager
from server.views import routes

class API(ExceptionHandler):
    def __init__(self):
        self.args = parse_args()
        self.routes = routes

        self.openapi = OpenAPI(
            {
                "title": "Bookstore Management API",
                "version": "1.0.0",
                "description": "API for online bookstore management system",
            },
        ).routes

        self.app = Kui(
            routes=self.routes + self.openapi[1:],
            exception_handlers={
                HTTPException: self.http_exception_handler,
                Exception: self.other_exception_handler,
            },
            factory_class=FactoryClass(),
            cors_config={
                "allow_origins": [re.compile(re.escape("*"))],
                "allow_methods": ["*"],
                "allow_headers": ["*"],
            },
        )

        self.app.state.lock = Lock()
        self.app.state.max_connections = self.args.max_connections

        self.app.on_startup(self.initialize_app)
        self.app.on_shutdown(self.cleanup_app)

    async def initialize_app(self, app: Kui):
        database_url = (
            f"mysql+pymysql://{self.args.db_user}:{self.args.db_password}@"
            f"{self.args.db_host}:{self.args.db_port}/{self.args.db_name}?charset=utf8mb4"
        )
        
        app.state.engine = create_engine(
            database_url,
            pool_size=self.args.max_connections,
            max_overflow=10,
            echo=self.args.debug,
            pool_pre_ping=True,
            pool_recycle=3600
        )

        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=app.state.engine)
        app.state.SessionLocal = SessionLocal
        
        app.state.db_manager = DatabaseManager(
            session_maker=SessionLocal,
            debug=self.args.debug
        )

        logger.info(f"Database connection established")
        logger.info(f"Server listening at http://{self.args.listen}")


    async def cleanup_app(self, app: Kui):
        await app.state.db_manager.close()
        logger.info("Database connections closed")

def parse_args():
    """命令行参数解析"""
    import argparse
    parser = argparse.ArgumentParser(description="Bookstore API Server")
    
    parser.add_argument("--listen", default="0.0.0.0:8000", help="Host and port to listen on")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    parser.add_argument("--db-host", default="localhost", help="Database host")
    parser.add_argument("--db-port", type=int, default=3306, help="Database port")
    parser.add_argument("--db-name", default="bookstore", help="Database name")
    parser.add_argument("--db-user", default="bookstore", help="Database user")
    parser.add_argument("--db-password", default="123456", help="Database password")
    parser.add_argument("--max-connections", type=int, default=10, help="Maximum database connections")
    
    return parser.parse_args()

if __name__ == "__main__":
    logger.add(
        "logs/api_{time}.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )

    api = API()
    host, port = api.args.listen.split(":")

    uvicorn.run(
        api.app,
        host=host,
        port=int(port),
        workers=api.args.workers,
        log_level="info" if not api.args.debug else "debug",
    )
