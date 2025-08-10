"""FastAPI entry point for the EBC Intel Radar backend.

This module defines a factory function to create an application instance.  By
encapsulating the setup in a function we make it easier to override
configuration in tests or when running background workers.
"""

from fastapi import FastAPI

from . import models
from .db import engine
from .api import router as api_router


def create_app() -> FastAPI:
    """Construct and configure the FastAPI application.

    Returns
    -------
    FastAPI
        The configured FastAPI application.
    """
    app = FastAPI(title="EBC Intel Radar API")
        # Create database tables if they do not exist
    models.Base.metadata.create_all(bind=engine)


    @app.get("/ping")
    async def ping() -> dict[str, str]:
        """Simple liveness probe."""
        return {"message": "pong"}

    # Include additional API routes under the `/api` prefix
    app.include_router(api_router, prefix="/api")

    return app


# When the module is run directly by an ASGI server such as Uvicorn, create
# the application instance at import time.
app = create_app()
