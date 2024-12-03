import logging
from fastapi import FastAPI
from .database import engine, Base
from .routers import users, articles, comments, auth, admin, complaints, reviews
from .utils import send_telegram_message
from fastapi import Request
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(articles.router)
app.include_router(comments.router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(complaints.router)
app.include_router(reviews.router)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")

@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    logger.error(f"Internal Server Error: {exc}")
    send_telegram_message(f"Internal Server Error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )
