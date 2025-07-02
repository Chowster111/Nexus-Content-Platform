from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.supabase_client import supabase
from logging_config import logger

class SignupRequest(BaseModel):
    email: str
    password: str

class SigninRequest(BaseModel):
    email: str
    password: str

class AuthController:
    def __init__(self):
        self.router = APIRouter()
        self.register_routes()

    def register_routes(self):
        @self.router.post("/signup")
        def signup(data: SignupRequest):
            logger.info(f"📥 Signup attempt for email: {data.email}")
            try:
                res = supabase.auth.sign_up({
                    "email": data.email,
                    "password": data.password
                })

                if res.get("error"):
                    logger.warning(f"⚠️ Supabase signup error: {res['error']['message']}")
                    raise HTTPException(status_code=400, detail=res["error"]["message"])

                user = res["user"]
                if user:
                    username = data.email.split("@")[0]
                    supabase.table("users").insert({
                        "id": user["id"],
                        "username": username,
                        "email": data.email
                    }).execute()

                logger.info(f"✅ User created with ID: {user['id'] if user else 'Unknown'}")
                return {"message": "User created", "user": user}

            except Exception as e:
                logger.exception("❌ Exception during signup")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.post("/signin")
        def signin(data: SigninRequest):
            logger.info(f"📥 Signin attempt for email: {data.email}")
            try:
                res = supabase.auth.sign_in_with_password({
                    "email": data.email,
                    "password": data.password
                })

                if res.get("error"):
                    logger.warning(f"⚠️ Invalid signin: {res['error']['message']}")
                    raise HTTPException(status_code=401, detail=res["error"]["message"])

                session = res["session"]
                logger.info(f"✅ Signin successful for user: {session['user']['id']}")
                return {
                    "message": "Signed in",
                    "access_token": session["access_token"],
                    "refresh_token": session["refresh_token"],
                    "user": session["user"]
                }

            except Exception as e:
                logger.exception("❌ Exception during signin")
                raise HTTPException(status_code=500, detail=str(e))
