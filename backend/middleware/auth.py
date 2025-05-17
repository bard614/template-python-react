from typing import Optional, Callable
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class JWTAuthMiddleware(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request):
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(request)
        
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="無效的認證方案"
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="無效的認證資訊"
            )

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict) -> bool:
        if "admin" in self.allowed_roles and user.is_admin:
            return True
        if "active" in self.allowed_roles and user.is_active:
            return True
        return False 