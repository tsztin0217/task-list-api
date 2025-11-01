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

    # for creating/updating a Task from a dictionary from a request body
    # which came in json format
    # then converted to a dictionary by request.get_json()
    # and here we create a Task object from that dictionary
    # so that we can add it to the database
    # flow: from request body in json --> from_dict() --> to Task object
    @classmethod
    def from_dict(cls, task_dict):
        is_complete = task_dict.get("is_complete", False)
        completed_at = datetime.now() if is_complete else None
        
        return cls(
            title=task_dict["title"],
            description=task_dict["description"],
            completed_at=completed_at
        )

    # to return a response with the new info including newlyy generated id 
    # after we get or create a task record in database
    # return a dictionary representation of the Task object
    # flow: from database --> Task object --> to_dict() --> to json response
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_complete": self.completed_at is not None
        }
    