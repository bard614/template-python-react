from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """使用者基本資料"""
    username: str = Field(..., min_length=3, max_length=50, description="使用者名稱")
    email: EmailStr = Field(..., description="電子郵件")
    is_active: bool = Field(True, description="是否啟用")
    is_admin: bool = Field(False, description="是否為管理員")

class UserCreate(UserBase):
    """建立使用者時的資料格式"""
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="密碼",
        examples=["password123"]
    )

class UserUpdate(BaseModel):
    """更新使用者時的資料格式"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="使用者名稱")
    email: Optional[EmailStr] = Field(None, description="電子郵件")
    password: Optional[str] = Field(None, min_length=8, max_length=100, description="密碼")
    is_active: Optional[bool] = Field(None, description="是否啟用")
    is_admin: Optional[bool] = Field(None, description="是否為管理員")

class UserInDB(UserBase):
    """資料庫中的使用者資料格式"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserOut(UserBase):
    """回傳給前端的使用者資料格式"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None 