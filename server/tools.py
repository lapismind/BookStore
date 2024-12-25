from decimal import Decimal
from typing import Dict

from server.models import *

CREDIT_LEVEL_THRESHOLDS: Dict[int, Decimal] = {
    1: Decimal('0'),
    2: Decimal('1000'),
    3: Decimal('5000'),
    4: Decimal('10000'),
    5: Decimal('50000')
}


def update_credit_level(user: User, db) -> bool:
    """
    检查并更新用户的信用等级
    返回是否发生了更新
    """
    current_balance = user.balance
    current_level = user.credit_level
    new_level = current_level

    # 检查是否需要升级
    for level, threshold in CREDIT_LEVEL_THRESHOLDS.items():
        if current_balance >= threshold:
            new_level = max(new_level, level)

    # 如果需要更新信用等级
    if new_level != current_level:
        user.credit_level = new_level
        db.commit()
        return True

    return False

async def batch_update_credit_levels():
    SessionLocal = request.app.state.SessionLocal
    db = SessionLocal()
    try:
        users = db.query(User).all()
        updated_count = 0

        for user in users:
            if update_credit_level(user, db):
                updated_count += 1

        return {
            "message": f"Updated {updated_count} users' credit levels",
            "updated_count": updated_count
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error in batch update: {e}")
        raise
    finally:
        db.close()
