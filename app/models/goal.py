from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..db import db
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .task import Task



class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    tasks: Mapped[list["Task"]] = relationship(back_populates="goal")

    @classmethod
    def from_dict(cls, goal_dict):
        """Create a Goal instance from a dictionary."""
        return cls(
            title=goal_dict["title"]
        )
    
    def to_dict(self):
        """Return a dictionary representation of the Goal."""
        return {
            "id": self.id,
            "title": self.title
        }