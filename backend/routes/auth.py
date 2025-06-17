from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.supabase_client import supabase

router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    password: str

class SigninRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(data: SignupRequest):
    try:
        res = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password
        })
        if res.get("error"):
            raise HTTPException(status_code=400, detail=res["error"]["message"])

        user = res["user"]
        if user:
            username = data.email.split("@")[0]
            supabase.table("users").insert({
                "id": user["id"],
                "username": username,
                "email": data.email
            }).execute()

        return {"message": "User created", "user": user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/signin")
def signin(data: SigninRequest):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password
        })

        if res.get("error"):
            raise HTTPException(status_code=401, detail=res["error"]["message"])

        session = res["session"]
        return {
            "message": "Signed in",
            "access_token": session["access_token"],
            "refresh_token": session["refresh_token"],
            "user": session["user"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
