from sqlalchemy.orm import Mapped, mapped_column
from ..db import db
from datetime import datetime
from sqlalchemy import DateTime
from typing import Optional

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    @classmethod
    def from_dict(cls, task_dict):
        """Create a Task instance from a dictionary."""
        is_complete = task_dict.get("is_complete", False)
        completed_at = datetime.now() if is_complete else None
        
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            completed_at=completed_at
        )

    def to_dict(self):
        """Return a dictionary representation of the Task."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    