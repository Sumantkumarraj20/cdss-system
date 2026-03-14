from fastapi import APIRouter, Body, HTTPException, status, Depends
import os
from fastapi.responses import JSONResponse

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.auth import require_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
def login(payload: dict = Body(...)):
    expected = os.getenv("CDSS_API_TOKEN")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="API token not configured",
        )
    if payload.get("token") != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    access = create_access_token("admin")
    refresh = create_refresh_token("admin")
    response = JSONResponse({"access_token": access, "refresh_token": refresh})
    response.set_cookie(
        "cdss_access",
        access,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        "cdss_refresh",
        refresh,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


@router.post("/refresh")
def refresh(token: dict = Body(...)):
    sub = decode_token(token.get("refresh_token") or token.get("token") or "")
    if not sub:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    access = create_access_token(sub)
    response = JSONResponse({"access_token": access})
    response.set_cookie(
        "cdss_access",
        access,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return response


@router.get("/me")
def me(_: str = Depends(require_token)):
    return {"role": "admin"}
