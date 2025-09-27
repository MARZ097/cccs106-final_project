from datetime import datetime

class Task:
    def __init__(
        self,
        id,
        title,
        description="",
        category="uncategorized",
        created_at=None,
        updated_at=None,
        completed=False
    ):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at
        self.completed = completed
    
    def to_dict(self):
        """Convert task to dictionary for storage"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "completed": self.completed
        }
