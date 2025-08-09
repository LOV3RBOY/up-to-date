"""API routes for the EBC Intel Radar backend."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .db import get_db
from . import models

router = APIRouter()


@router.get("/intel")
async def get_intel(db: Session = Depends(get_db)) -> dict[str, list]:
    """Return the most recently ingested intelligence items.

    Currently this returns a simple list of all Article records in the
    database.  You can extend this endpoint to perform filtering,
    aggregation, or scoring.  The front‑end consumes this endpoint to
    display a feed.

    Parameters
    ----------
    db : Session
        A SQLAlchemy session injected via dependency.

    Returns
    -------
    dict[str, list]
        A dictionary containing the list of articles under the `intel` key.
    """
    articles = db.query(models.Article).order_by(models.Article.published.desc()).limit(50).all()
    return {"intel": [article.to_dict() for article in articles]}
