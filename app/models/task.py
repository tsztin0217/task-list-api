from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from sqlalchemy import DateTime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def return_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed_at": self.completed_at if self.completed_at else None
        }
