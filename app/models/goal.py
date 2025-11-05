from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Goal(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]

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