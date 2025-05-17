from fastapi import APIRouter
from middleware.decorators import require_roles
from models.user import User

router = APIRouter(
    prefix="/test",
    tags=["測試"]
)

@router.get("/public")
async def public_route():
    """公開路由"""
    return {"message": "這是公開的路由"}

@router.get("/user")
@require_roles(["active"])
async def user_route(current_user: User):
    """需要一般使用者權限的路由"""
    return {
        "message": "這是需要使用者權限的路由",
        "user": {
            "username": current_user.username,
            "email": current_user.email
        }
    }

@router.get("/admin")
@require_roles(["admin"])
async def admin_route(current_user: User):
    """需要管理員權限的路由"""
    return {
        "message": "這是需要管理員權限的路由",
        "user": {
            "username": current_user.username,
            "email": current_user.email,
            "is_admin": current_user.is_admin
        }
    } 