from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from models import Base

def create_database_if_not_exists(user, password, host, port, db_name):
    engine_url = f"mysql+pymysql://{user}:{password}@{host}:{port}"
    engine = create_engine(engine_url)
    
    try:
        with engine.connect() as conn:
            conn.execute(text(
                f"CREATE DATABASE IF NOT EXISTS {db_name} "
                "CHARACTER SET utf8mb4 "
                "COLLATE utf8mb4_unicode_ci"
            ))
            print(f"Database '{db_name}' created successfully or already exists.")
            
            conn.execute(text(f"ALTER DATABASE {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            print(f"Database character set updated to utf8mb4")
    except Exception as e:
        print(f"Error creating/updating database: {e}")
        raise
    finally:
        engine.dispose()

def init_database(database_url: str):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)
    print("Tables created successfully.")
    engine.dispose()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-user", default="bookstore")
    parser.add_argument("--db-password", default='123456')
    parser.add_argument("--db-host", default="localhost")
    parser.add_argument("--db-port", default="3306")
    parser.add_argument("--db-name", default="bookstore")
    
    args = parser.parse_args()
    
    create_database_if_not_exists(
        args.db_user, 
        args.db_password, 
        args.db_host, 
        args.db_port, 
        args.db_name
    )
    
    database_url = (
        f"mysql+pymysql://{args.db_user}:{args.db_password}@"
        f"{args.db_host}:{args.db_port}/{args.db_name}"
    )
    
    init_database(database_url)
