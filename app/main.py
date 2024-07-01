import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis
from sqladmin import Admin
import sentry_sdk

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.database import engine
from app.hotels.room.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.pages.router import router as router_pages
from app.static.images.router import router as router_images
from app.users.router import router as router_users
from app.logger import logger
from fastapi_versioning import VersionedFastAPI
from fastapi_cache.backends.inmemory import InMemoryBackend


app = FastAPI()


sentry_sdk.init(
    dsn="https://fa2d7b3dda356d2272fb3d7f07513bfe@o4506709859434496.ingest.sentry.io/4506709861793792",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0



app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_images)

app.include_router(router_pages)

origins = [
    "http://localhost:3000",
]

FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Acces-Control-Allow-Headers",
                    "Acces-Control-Allow-Origin",
                "Authorization"])


async def startup():
    redis = await aioredis.from_url("redis://localhost:6379",
                                    encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

app.add_event_handler("startup", startup)

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
#     description='Greet users with a nice message',
#     middleware=[
#         Middleware(SessionMiddleware, secret_key='mysecretkey')
#     ]
)

admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request handing time", extra={
        "process_time": round(process_time, 4)})
    return response

app.mount("/static", StaticFiles(directory="app/static"), "static")