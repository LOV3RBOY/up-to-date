"""Database models for the EBC Intel Radar backend.

This module defines SQLAlchemy ORM models.  Only a minimal `Article`
table is provided out of the box; you can extend this to include
additional tables (e.g. `Event`, `Artist`, `Venue`) and relationships.
"""

from datetime import datetime
from typing import Any, Dict

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Article(Base):
    """A news article or intelligence item stored in the database."""

    __tablename__ = "articles"

    id: int = Column(Integer, primary_key=True, index=True)
    source: str = Column(String(255), index=True)
    title: str = Column(String(512), nullable=False)
    url: str = Column(String(2048), nullable=False, unique=True)
    published: datetime = Column(DateTime, default=datetime.utcnow, index=True)
    summary: str = Column(Text, nullable=True)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the article to a plain dictionary for JSON responses."""
        return {
            "id": self.id,
            "source": self.source,
            "title": self.title,
            "url": self.url,
            "published": self.published.isoformat() if self.published else None,
            "summary": self.summary,
        }
