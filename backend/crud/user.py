from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, or_, desc
from typing import List, Optional
from models.user import User
from schemas.user import UserCreate, UserUpdate
from utils.auth import get_password_hash

def get_user(db: Session, user_id: int) -> Optional[User]:
    """根據 ID 取得使用者"""
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """根據 email 取得使用者"""
    return db.query(User).filter(User.email == email).first()

def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    search: Optional[str] = None,
    sort_by: str = "id",
    order: str = "asc"
) -> List[User]:
    """取得使用者列表"""
    # 建立基本查詢
    query = select(User)
    
    # 加入搜尋條件
    if search:
        search = f"%{search}%"
        query = query.where(
            or_(
                User.username.ilike(search),
                User.email.ilike(search)
            )
        )
    
    # 加入排序
    if order == "desc":
        query = query.order_by(desc(getattr(User, sort_by)))
    else:
        query = query.order_by(getattr(User, sort_by))
    
    # 加入分頁
    query = query.offset(skip).limit(limit)
    
    # 執行查詢
    result = db.execute(query)
    return list(result.scalars().all())

def create_user(db: Session, user: UserCreate) -> User:
    """建立新使用者"""
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        is_admin=user.is_admin if hasattr(user, 'is_admin') else False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate) -> Optional[User]:
    """更新使用者資料"""
    # 建立更新資料字典
    update_data = user.dict(exclude_unset=True)
    
    # 如果有密碼更新，進行雜湊處理
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    if not update_data:
        return None
    
    # 執行更新
    stmt = (
        update(User)
        .where(User.id == user_id)
        .values(**update_data)
        .returning(User)
    )
    result = db.execute(stmt)
    db.commit()
    
    return result.scalar_one_or_none()

def delete_user(db: Session, user_id: int) -> bool:
    """刪除使用者"""
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()
    return result.rowcount > 0 