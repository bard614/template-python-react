from pydantic import BaseModel, Field

class Token(BaseModel):
    """JWT Token 回傳格式"""
    access_token: str = Field(..., description="JWT 存取令牌")
    token_type: str = Field("bearer", description="令牌類型")

class TokenData(BaseModel):
    """JWT Token 內容格式"""
    username: str = Field(..., description="使用者名稱")
    email: str = Field(..., description="電子郵件")
    is_admin: bool = Field(False, description="是否為管理員") 