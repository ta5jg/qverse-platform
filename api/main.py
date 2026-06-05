from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse
from api.routes import enabled_routers, route_manifest


STARTED_AT = datetime.now(timezone.utc)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.started_at = STARTED_AT
    app.state.status = "running"
    yield
    app.state.status = "stopped"

app = FastAPI(
    title="Q-Verse API",
    version="4.0.0",
    lifespan=lifespan,
)

for router in enabled_routers():
    app.include_router(router)


@app.middleware("http")
async def request_context(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-QVerse-Version"] = "4.0.0"
    response.headers["X-QVerse-Platform"] = "Q-Verse"
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": type(exc).__name__,
            "message": str(exc),
        },
    )

@app.get("/version")
def version():
    return {
        "platform": "Q-Verse",
        "version": "4.0.0",
        "api": "V9",
    }


@app.get("/routes")
def routes():
    return route_manifest()


@app.get("/metrics")
def metrics():
    return {
        "metrics": "enabled",
        "uptime_seconds": int((datetime.now(timezone.utc) - STARTED_AT).total_seconds()),
    }


@app.get("/")
def root():
    return {
        "name": "Q-Verse API",
        "status": "running",
        "version": "4.0.0",
    }
