from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime
from ..db import db
from datetime import datetime
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from .goal import Goal


class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    goal_id: Mapped[Optional[int]] = mapped_column(ForeignKey("goal.id"))
    goal: Mapped[Optional["Goal"]] = relationship(back_populates="tasks")

    @classmethod
    def from_dict(cls, task_dict):
        """Create a Task instance from a dictionary."""
        goal_id = task_dict.get("goal_id")
        is_complete = task_dict.get("is_complete", False)
        completed_at = datetime.now() if is_complete else None
        
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            completed_at=completed_at,
            goal_id=goal_id
        )

    def to_dict(self):
        """Return a dictionary representation of the Task."""
        task_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
        if self.goal:
            task_dict["goal_id"] = self.goal.id

        return task_dict
