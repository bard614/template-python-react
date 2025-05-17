from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from database import get_db
from crud.user import get_user_by_email
from schemas.token import TokenData

# 載入環境變數
load_dotenv()

# 密碼加密設定
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT 設定
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# OAuth2 設定
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """生成密碼雜湊值"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """建立 JWT Token"""
    to_encode = data.copy()
    
    # 設定過期時間
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 加入過期時間到 token 資料中
    to_encode.update({"exp": expire})
    
    # 產生 JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """從 JWT Token 取得當前使用者"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認證失敗",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # 解碼 JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        # 建立 token 資料模型
        token_data = TokenData(
            username=username,
            email=payload.get("email"),
            is_admin=payload.get("is_admin", False)
        )
    except JWTError:
        raise credentials_exception
    
    # 從資料庫取得使用者
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    """檢查使用者是否啟用"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="使用者未啟用"
        )
    return current_user

async def get_current_admin_user(current_user = Depends(get_current_active_user)):
    """檢查使用者是否為管理員"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理員權限"
        )
    return current_user 