"""Background tasks for ingesting and processing data.

These Celery tasks serve as examples of how you might pull data from
external APIs, perform AI enrichment, and persist results into the
database.  At present they implement placeholders so the worker can be
started successfully.  Replace the implementations with your own logic
to call services like the Perigon News API, GDELT, or Ticketmaster, and
to run summarization/classification via OpenAI.
"""

import logging
import os
from datetime import datetime

import requests

from ..app import models, db
from ..app.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task
def fetch_perigon_news() -> str:
    """Fetch recent news articles from the Perigon API and store them.

    You must set `PERIGON_API_KEY` in your environment for this task to run.

    Returns
    -------
    str
        A summary message indicating how many articles were ingested.
    """
    api_key = os.getenv("PERIGON_API_KEY")
    if not api_key:
        logger.warning("PERIGON_API_KEY is not configured; skipping fetch.")
        return "Perigon fetch skipped"

    endpoint = "https://api.goperigon.com/v1/all"
    params = {
        "apiKey": api_key,
        "q": "Las Vegas nightlife OR Encore Beach Club OR Zouk Nightclub OR LIV Nightclub OR Marquee Nightclub OR Omnia Nightclub",
        "from": (datetime.utcnow().date()).isoformat(),
        "sources": "",
        "pageSize": 25,
    }
    resp = requests.get(endpoint, params=params, timeout=10)
    if resp.status_code != 200:
        logger.error("Perigon request failed: %s", resp.text)
        return f"Perigon fetch failed with status {resp.status_code}"
    data = resp.json()
    articles = data.get("articles", [])

    session = db.SessionLocal()
    count = 0
    try:
        for item in articles:
            # Avoid duplicates by URL
            existing = session.query(models.Article).filter_by(url=item["url"]).first()
            if existing:
                continue
            article = models.Article(
                source=item.get("source", "perigon"),
                title=item.get("title"),
                url=item.get("url"),
                summary=item.get("summary"),
                published=datetime.fromisoformat(item.get("publishedAt", datetime.utcnow().isoformat())),
            )
            session.add(article)
            count += 1
        session.commit()
    except Exception as exc:  # pylint: disable=broad-except
        session.rollback()
        logger.exception("Failed to persist Perigon articles: %s", exc)
        return "Perigon fetch encountered an error"
    finally:
        session.close()
    return f"Perigon fetch stored {count} new articles"


@celery_app.task
def dummy_task(name: str = "world") -> str:
    """Example task that returns a greeting.

    Celery requires at least one task to function.  You can remove this
    after adding your own tasks.
    """
    logger.info("Running dummy task for %s", name)
    return f"hello {name}"
