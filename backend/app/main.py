"""FastAPI entry point for the EBC Intel Radar backend.

This module defines a factory function to create an application instance.  By
encapsulating the setup in a function we make it easier to override
configuration in tests or when running background workers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .db import engine
from .api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(title="EBC Intel Radar API")

    # Auto-create DB tables
    models.Base.metadata.create_all(bind=engine)

    # CORS for Netlify (and your custom domain if you add one later)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://*.netlify.app",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    # APIs
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()
