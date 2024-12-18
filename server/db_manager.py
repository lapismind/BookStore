# tools/server/db_manager.py
from typing import Generator
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger

class DatabaseManager:
    def __init__(self, session_maker: sessionmaker, debug: bool = False):
        """
        初始化数据库管理器
        Args:
            session_maker: SQLAlchemy的会话制造器
            debug: 是否开启调试模式
        """
        self.session_maker = session_maker
        self.debug = debug
        logger.info("Database manager initialized")

    def get_db(self) -> Generator[Session, None, None]:
        """
        获取数据库会话的上下文管理器
        使用方法:
        with db_manager.get_db() as db:
            db.query(Model).all()
        """
        db = self.session_maker()
        try:
            yield db
        finally:
            db.close()

    async def execute_transaction(self, operation):
        """
        执行数据库事务
        Args:
            operation: 需要在事务中执行的操作函数
        """
        db = self.session_maker()
        try:
            result = await operation(db)
            await db.commit()
            return result
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Database transaction error: {str(e)}")
            raise
        finally:
            db.close()

    def get_session(self) -> Session:
        """
        获取一个新的数据库会话
        Returns:
            Session: SQLAlchemy会话对象
        """
        return self.session_maker()

    async def close(self):
        """
        关闭所有数据库连接
        """
        self.session_maker.close_all()
        logger.info("All database connections closed")

    async def health_check(self) -> bool:
        """
        数据库健康检查
        Returns:
            bool: 数据库是否正常
        """
        try:
            db = self.get_session()
            db.execute("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return False
        finally:
            db.close()
