from database import engine, SessionLocal, Base
from models.user import User
from utils.password import get_password_hash

def init_db():
    # 建立所有資料表
    Base.metadata.create_all(bind=engine)
    
    # 建立資料庫連線
    db = SessionLocal()
    
    try:
        # 檢查是否已存在管理員帳號
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        
        if not admin:
            # 建立管理員帳號
            admin = User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_admin=True
            )
            db.add(admin)
            db.commit()
            print("管理員帳號建立成功")
        else:
            print("管理員帳號已存在")
            
    except Exception as e:
        print(f"初始化資料庫時發生錯誤: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("開始初始化資料庫...")
    init_db()
    print("資料庫初始化完成") 