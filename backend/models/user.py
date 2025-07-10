from pydantic import BaseModel

class User(BaseModel):
    """User model for authentication responses."""
    id: str
    username: str
    email: str 