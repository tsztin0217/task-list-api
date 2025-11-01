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

    # for the response when we get or create a task
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    
    # for creating a Task from a dictionary from a request body
    @classmethod
    def from_dict(cls, task_dict):
        is_complete = task_dict.get("is_complete", False)
        completed_at = datetime.now(datetime) if is_complete else None
        
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            completed_at=completed_at
        )