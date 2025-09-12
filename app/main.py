from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth, OAuthError

from app.routes.admin import author_a, book_a, category_a, user_manage_a
from app.routes.user import user_u, book_u, category_u
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

app.add_middleware(SessionMiddleware, secret_key="add any string here")
app.mount("/static", StaticFiles(directory="static"), name="static")

oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_id=settings.CLIENT_ID,
    client_secret=settings.CLIENT_SECRET,
    client_kwargs={
        "scope": "openid email profile",
        "redirect_url": "http://127.0.0.1:8000/auth"
    }
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
def read_root(request: Request):
    user = request.session.get("user")
    if user:
        return RedirectResponse("/welcome")
    return templates.TemplateResponse(
        name = "index.html", 
        context = {"request": request}
    )

@app.get("/welcome")
def welcome(request: Request):
    user = request.session.get("user")
    if user:
        return templates.TemplateResponse(
            name = "welcome.html", 
            context = {"request": request, "user": user}
        )
    return RedirectResponse("/")

@app.get("/login")
async def login(request: Request):
    url = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, url)

@app.get("/auth")
async def auth(request:Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as e:
        return templates.TemplateResponse(
            name = "error.html", 
            context = {"request": request, "error": e.error}
        )
    user = token.get("userinfo")
    if user:
        request.session["user"] = dict(user)
    return RedirectResponse("/welcome")

@app.get("/logout")
def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse("/")

# app.include_router(auth.router)

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

add_pagination(app)