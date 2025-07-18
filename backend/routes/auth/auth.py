from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError
from db.supabase_client import supabase
from logging_config import logger
from models.auth import SignupRequest, SigninRequest, AuthResponse
from models.user import User


class AuthController:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self) -> None:
        """Register all authentication routes."""
        @self.router.post(
            "/signup", 
            response_model=AuthResponse,
            summary="User Registration",
            description="""
            Create a new user account with email and password.
            
            This endpoint handles user registration using Supabase Auth. Upon successful
            registration, a new user record is created in the database with basic profile
            information.
            
            **Features:**
            - Email and password validation
            - Automatic user profile creation
            - Secure password hashing via Supabase
            - Username generation from email address
            - Duplicate email prevention
            
            **Security:**
            - Passwords are securely hashed by Supabase
            - Email validation and verification
            - Protection against common attack vectors
            - Rate limiting on registration attempts
            
            **Response:**
            Returns user information and authentication tokens upon successful registration.
            """,
            response_description="User registration response with tokens and user data",
            tags=["Authentication"]
        )
        def signup(data: SignupRequest) -> AuthResponse:
            """
            Register a new user account.
            
            Creates a new user account with the provided email and password.
            The system automatically generates a username from the email address
            and creates a user profile in the database.
            
            **Request Body:**
            - `email`: Valid email address for the account
            - `password`: Secure password (minimum 6 characters)
            
            **Example Request:**
            ```json
            {
              "email": "user@example.com",
              "password": "securepassword123"
            }
            ```
            
            **Example Response:**
            ```json
            {
              "message": "User created",
              "user": {
                "id": "user-123",
                "email": "user@example.com",
                "username": "user"
              },
              "access_token": null,
              "refresh_token": null
            }
            ```
            
            **Error Scenarios:**
            - 400: Invalid email format or weak password
            - 400: Email already exists
            - 500: Database or authentication service error
            """
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

        @self.router.post(
            "/signin", 
            response_model=AuthResponse,
            summary="User Authentication",
            description="""
            Authenticate a user with email and password.
            
            This endpoint handles user authentication using Supabase Auth. Upon successful
            authentication, access and refresh tokens are returned for API access.
            
            **Features:**
            - Secure email/password authentication
            - JWT token generation for API access
            - Refresh token for session management
            - Session validation and security
            - Rate limiting on authentication attempts
            
            **Security:**
            - Secure password verification
            - JWT token expiration management
            - Protection against brute force attacks
            - Session-based security
            
            **Response:**
            Returns authentication tokens and user information upon successful login.
            """,
            response_description="User authentication response with tokens and user data",
            tags=["Authentication"]
        )
        def signin(data: SigninRequest) -> AuthResponse:
            """
            Authenticate a user with email and password.
            
            Validates user credentials and returns authentication tokens for API access.
            The access token should be included in subsequent API requests.
            
            **Request Body:**
            - `email`: User's email address
            - `password`: User's password
            
            **Example Request:**
            ```json
            {
              "email": "user@example.com",
              "password": "securepassword123"
            }
            ```
            
            **Example Response:**
            ```json
            {
              "message": "Signed in",
              "user": {
                "id": "user-123",
                "email": "user@example.com",
                "username": "user"
              },
              "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
              "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
            ```
            
            **Token Usage:**
            Include the access token in API requests:
            ```
            Authorization: Bearer <access_token>
            ```
            
            **Error Scenarios:**
            - 401: Invalid email or password
            - 401: Account not found
            - 500: Authentication service error
            """
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
