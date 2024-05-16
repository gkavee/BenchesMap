from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from benches.router import router as benches_router
from config import REDIS_HOST, REDIS_PORT
from users.router import router as users_router
from auth.router import router as auth_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

app = FastAPI(
    title='Bench app'
)

origins = [
    "https://localhost:8000",
    "https://localhost:5173",
    "https://localhost:5001",
    "https://localhost:5002",
    "https://f4c676c6e47e.vps.myjino.ru:49379",
    "https://f4c676c6e47e.vps.myjino.ru",
    "https://api.fitji.ru",
    "https://fitji.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Cookie", "Set-Cookie", "Access-Control-Allow-Credential", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin", "Access-Control-Allow-Methods", "Authorization"],
)


app.include_router(benches_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
