---

```markdown
# 📘 Web 使用者管理系統開發計畫書

## 🧾 專案目標
開發一個簡單的使用者管理系統，具備帳號登入登出與使用者 CRUD 功能，採用前後端分離架構。

---

## 🧰 技術選型

| 類別       | 技術                                          |
|------------|-----------------------------------------------|
| 前端       | React + Vite + React Router + Axios + Tailwind CSS |
| 後端       | Python + FastAPI                              |
| 資料庫     | MySQL                                         |
| ORM 工具   | SQLAlchemy                                    |
| 身份驗證   | JWT (PyJWT)                                   |
| 表單處理   | react-hook-form                               |
| API 格式   | RESTful API                                   |
| 開發工具   | Cursor (VS Code Plugin)                       |

---

## 📁 建議資料夾結構

```

project-root/
├── backend/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── database.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   └── App.jsx
│   ├── .env
│   └── package.json
└── README.md

```

---

## ✅ 開發步驟清單

### 初始化階段
- [x] 1. 建立前端專案：`npm create vite@latest frontend --template react`
- [x] 2. 建立後端專案資料夾與基本結構（使用 FastAPI + SQLAlchemy）
- [x] 3. 設定 `.env` 檔案與資料庫連線
---

### 後端開發：帳號與使用者功能
- [x] 4. 建立 `User` 資料表與 SQLAlchemy 模型
- [x] 5. 建立 CRUD 操作函式
- [x] 6. 使用 Pydantic 建立 `UserCreate` / `UserOut` 等 schema
- [x] 7. 實作 JWT 登入 API（`POST /login`）
- [x] 8. 建立 JWT 驗證中介層
- [x] 9. 建立 `GET /users` 取得使用者清單
- [x] 10. 建立 `POST /users` 新增使用者
- [x] 11. 建立 `PUT /users/{id}` 編輯使用者
- [x] 12. 建立 `DELETE /users/{id}` 刪除使用者
- [x] 13. 加上 CORS 設定以支援前端請求

---

### 前端開發：登入與使用者管理介面
- [x] 14. 建立登入頁面與登入表單，連接 `POST /login`
- [x] 15. 登入成功後儲存 JWT 並導向主畫面
- [x] 16. 建立使用者列表頁，顯示所有使用者（呼叫 `GET /users`）
- [x] 17. 建立新增使用者頁面（呼叫 `POST /users`）
- [x] 18. 建立編輯使用者頁面（呼叫 `PUT /users/{id}`）
- [x] 19. 實作刪除使用者功能（呼叫 `DELETE /users/{id}`）
- [x] 20. 使用 react-router-dom 建立路由切換與保護機制
- [x] 21. 建立登出按鈕與清除 token 功能

---

### 測試與優化
- [x] 22. 測試整體流程：註冊、登入、編輯、刪除等功能
- [ ] 23. 處理 API 錯誤訊息並顯示於前端
- [x] 24. 前端介面簡單美化（使用 Tailwind CSS）
- [ ] 25. 撰寫 README 使用說明與啟動指南
```