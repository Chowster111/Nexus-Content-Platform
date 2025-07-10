from pydantic import BaseModel

class TagCount(BaseModel):
    """Model for tag statistics in analytics."""
    tag: str
    count: int 