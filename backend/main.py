from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, test, users

# 建立 FastAPI 應用程式
app = FastAPI(
    title="使用者管理系統",
    description="使用 FastAPI 建立的使用者管理系統 API",
    version="1.0.0"
)

# 設定 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在實際環境中應該限制允許的來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router)
app.include_router(test.router)
app.include_router(users.router)

# 根路由
@app.get("/")
async def root():
    return {"message": "歡迎使用使用者管理系統 API"} 