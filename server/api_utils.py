import argparse
from typing import NamedTuple

def parse_args():
    """解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数对象
    """
    parser = argparse.ArgumentParser(description="BookStore API Server")
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="服务器监听地址 (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="服务器端口 (default: 8000)"
    )
    
    parser.add_argument(
        "--db-host",
        default="localhost",
        help="数据库主机地址 (default: localhost)"
    )
    parser.add_argument(
        "--db-port",
        type=int,
        default=3306,
        help="数据库端口 (default: 3306)"
    )
    parser.add_argument(
        "--db-user",
        default="bookstore",
        help="数据库用户名 (default: bookstore)"
    )
    parser.add_argument(
        "--db-password",
        default="123456",
        help="数据库密码"
    )
    parser.add_argument(
        "--db-name",
        default="bookstore",
        help="数据库名称 (default: bookstore)"
    )
    
    # 调试模式
    parser.add_argument(
        "--debug",
        action="store_true",
        help="是否开启调试模式"
    )
    
    return parser.parse_args()
