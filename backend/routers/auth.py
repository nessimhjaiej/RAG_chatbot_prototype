"""Authentication router for FastAPI.

Provides endpoints for login, logout, and session verification.
"""

from fastapi import APIRouter, HTTPException, Response, Cookie, Depends
from pydantic import BaseModel
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path to import app modules
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.auth import authenticate_user as auth_user

router = APIRouter()


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    user: Optional[dict] = None
    message: Optional[str] = None


@router.post("/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """
    Authenticate user with username and password.
    Returns user info with role on success.
    """
    try:
        user = auth_user(credentials.username, credentials.password)
        if user:
            return LoginResponse(success=True, user=user, message="Login successful")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")


@router.post("/logout")
async def logout():
    """
    Logout the current user.
    In this simple implementation, just returns success.
    In production, you'd clear session/JWT tokens.
    """
    return {"success": True, "message": "Logged out successfully"}


@router.get("/verify")
async def verify_session():
    """
    Verify if the current session is valid.
    In this simple implementation, always returns true.
    In production, you'd check for valid session/JWT token.
    """
    return {"valid": True}
