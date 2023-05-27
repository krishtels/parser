import aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_pagination import add_pagination

from routers import lamoda_router, twitch_router

app = FastAPI()
app.include_router(lamoda_router.router)
app.include_router(twitch_router.router)

add_pagination(app)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://redis", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="parser-cache")
