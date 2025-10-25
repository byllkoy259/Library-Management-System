from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination
from starlette.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from app.auth.jwt_handler import verify_token
from app.routes.admin import author_a, book_a, category_a, user_manage_a
from app.routes.user import user_u, book_u, category_u, borrow_u
from app.routes import auth
from app.seed import seed_data
from app.config import settings
from app import database

def init_db():
    database.Base.metadata.create_all(bind=database.engine)
    db = database.SessionLocal()
    seed_data(db)
    db.close()

init_db()

app = FastAPI(
    title="Library Management System",
    description="A simple library management system API built with FastAPI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    user_u.router,
    prefix="",
    tags=["user - user"],
)
app.include_router(
    book_u.router,
    prefix="/user/books",
    tags=["user - books"],
)
app.include_router(
    category_u.router,
    prefix="/user/categories",
    tags=["user - categories"],
)
app.include_router(
    borrow_u.router,
    prefix="/user/borrows",
    tags=["user - borrows"],
)
app.include_router(
    user_manage_a.router,
    prefix="/admin/users",
    tags=["admin - users"],
)
app.include_router(
    book_a.router,
    prefix="/admin/books",
    tags=["admin - books"],
)
app.include_router(
    category_a.router,
    prefix="/admin/categories",
    tags=["admin - categories"],
)
app.include_router(
    author_a.router,
    prefix="/admin/authors",
    tags=["admin - authors"]
)
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["user - auth"]
)

add_pagination(app)


@app.get("/")
def root():
    return {"message": "Welcome to the Library Management System."}

@app.get("/protected")
async def protected_route(user=Depends(verify_token)):
    return {"message": f"Hello, {user.username}. This is a protected route."}