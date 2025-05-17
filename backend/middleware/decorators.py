from functools import wraps
from typing import List, Callable
from fastapi import HTTPException, status, Depends
from utils.auth import get_current_user, get_current_active_user, get_current_admin_user

def require_roles(roles: List[str]) -> Callable:
    """檢查使用者是否具有指定角色的裝飾器"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 根據角色要求選擇適當的驗證函數
            if "admin" in roles:
                user = await get_current_admin_user()
            elif "active" in roles:
                user = await get_current_active_user()
            else:
                user = await get_current_user()
            
            # 將使用者資訊加入到 kwargs
            kwargs["current_user"] = user
            return await func(*args, **kwargs)
        return wrapper
    return decorator 