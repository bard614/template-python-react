from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserOut
from middleware.decorators import require_roles
from crud.user import (
    get_users,
    get_user_by_id,
    create_user,
    update_user,
    delete_user
)

router = APIRouter(
    prefix="/users",
    tags=["使用者管理"]
)

@router.get("/", response_model=List[UserOut])
@require_roles(["admin"])
async def list_users(
    skip: int = Query(default=0, ge=0, description="跳過的記錄數"),
    limit: int = Query(default=10, ge=1, le=100, description="每頁記錄數"),
    search: Optional[str] = Query(default=None, description="搜尋使用者名稱或電子郵件"),
    sort_by: Optional[str] = Query(
        default="id",
        enum=["id", "username", "email", "created_at"],
        description="排序欄位"
    ),
    order: Optional[str] = Query(
        default="asc",
        enum=["asc", "desc"],
        description="排序方向"
    ),
    db: Session = Depends(get_db),
    current_user: User = None
):
    """
    取得使用者清單
    
    - **skip**: 跳過的記錄數（分頁用）
    - **limit**: 每頁記錄數
    - **search**: 搜尋使用者名稱或電子郵件
    - **sort_by**: 排序欄位（id、username、email、created_at）
    - **order**: 排序方向（asc、desc）
    """
    users = get_users(
        db,
        skip=skip,
        limit=limit,
        search=search,
        sort_by=sort_by,
        order=order
    )
    return users

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@require_roles(["admin"])
async def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = None
):
    """建立新使用者"""
    return create_user(db=db, user=user)

@router.put("/{user_id}", response_model=UserOut)
@require_roles(["admin"])
async def update_user_info(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = None
):
    """更新使用者資訊"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該使用者"
        )
    return update_user(db=db, user_id=user_id, user=user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@require_roles(["admin"])
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = None
):
    """刪除使用者"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="找不到該使用者"
        )
    delete_user(db=db, user_id=user_id)
    return None 