from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError
from db.supabase_client import supabase
from logging_config import logger
from ..models.auth import SignupRequest, SigninRequest, AuthResponse
from ..models.user import User


class AuthController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all authentication routes."""
        @self.router.post("/signup", response_model=AuthResponse)
        def signup(data: SignupRequest) -> AuthResponse:
            """Handle user signup."""
            logger.info(f"AUTH Signup attempt for email: {data.email}")
            try:
                res: Dict[str, Any] = supabase.auth.sign_up({
                    "email": data.email,
                    "password": data.password
                })

                if res.get("error"):
                    logger.warning(f"ERROR Supabase signup error: {res['error']['message']}")
                    raise HTTPException(status_code=400, detail=res["error"]["message"])

                user: Dict[str, Any] = res["user"]
                if user:
                    username: str = data.email.split("@")[0]
                    supabase.table("users").insert({
                        "id": user["id"],
                        "username": username,
                        "email": data.email
                    }).execute()

                logger.info(f"AUTH User created with ID: {user['id'] if user else 'Unknown'}")
                try:
                    return AuthResponse(message="User created", user=user)
                except ValidationError as ve:
                    logger.error(f"Validation error for AuthResponse: {user} | {ve}")
                    raise HTTPException(status_code=500, detail=f"Validation error: {ve}")

            except Exception as e:
                logger.exception("ERROR Exception during signup")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.post("/signin", response_model=AuthResponse)
        def signin(data: SigninRequest) -> AuthResponse:
            """Handle user signin."""
            logger.info(f"Signin attempt for email: {data.email}")
            try:
                res: Dict[str, Any] = supabase.auth.sign_in_with_password({
                    "email": data.email,
                    "password": data.password
                })

                if res.get("error"):
                    logger.warning(f"ERROR Invalid signin: {res['error']['message']}")
                    raise HTTPException(status_code=401, detail=res["error"]["message"])

                session: Dict[str, Any] = res["session"]
                logger.info(f"SUCCESS Signin successful for user: {session['user']['id']}")
                try:
                    return AuthResponse(
                        message="Signed in",
                        access_token=session["access_token"],
                        refresh_token=session["refresh_token"],
                        user=session["user"]
                    )
                except ValidationError as ve:
                    logger.error(f"Validation error for AuthResponse: {session} | {ve}")
                    raise HTTPException(status_code=500, detail=f"Validation error: {ve}")

            except Exception as e:
                logger.exception("Exception during signin")
                raise HTTPException(status_code=500, detail=str(e))
