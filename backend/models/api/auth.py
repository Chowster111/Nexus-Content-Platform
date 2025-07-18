from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class SignupRequest(BaseModel):
    """
    User signup request model.
    """
    email: str = Field(..., description="User email address")
    password: str = Field(..., min_length=6, description="User password")

class SigninRequest(BaseModel):
    """
    User signin request model.
    """
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")

class AuthResponse(BaseModel):
    """
    Authentication response model.
    """
    message: str
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None 