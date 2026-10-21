from contextlib import asynccontextmanager
from pathlib import Path
from secrets import compare_digest

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from src.api import router
from src.config import settings
from src.database import init_db

ASSET_ROOT = Path(__file__).resolve().parents[1] / "assets" / "pictograms"


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Easy Read Adapter",
    description="Adapt Spanish texts for easier reading and add pictograms.",
    version="0.1.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def protect_api(request: Request, call_next):
    configured_key = settings.api_key.strip()
    if (
        configured_key
        and request.url.path.startswith("/api/")
        and request.url.path != "/api/health"
        and not compare_digest(request.headers.get("X-API-Key", ""), configured_key)
    ):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)


app.mount(
    "/pictograms/own",
    StaticFiles(directory=ASSET_ROOT / "own"),
    name="pictograms-own",
)
app.mount(
    "/pictograms/mulberry",
    StaticFiles(directory=ASSET_ROOT / "mulberry"),
    name="pictograms-mulberry",
)
app.include_router(router)
