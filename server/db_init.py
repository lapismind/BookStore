# tools/server/db_init.py
from sqlalchemy import create_engine
from models import Base

def init_database(database_url: str):
    engine = create_engine(database_url)
    
    # 创建所有表
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-user", default="root")
    parser.add_argument("--db-password", required=True)
    parser.add_argument("--db-host", default="localhost")
    parser.add_argument("--db-port", default="3306")
    parser.add_argument("--db-name", default="bookstore")
    
    args = parser.parse_args()
    
    database_url = (
        f"mysql+pymysql://{args.db_user}:{args.db_password}@"
        f"{args.db_host}:{args.db_port}/{args.db_name}?charset=utf8mb4"
    )
    
    init_database(database_url)
