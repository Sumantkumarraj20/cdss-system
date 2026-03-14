from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import os

from app.core.security import decode_token

security = HTTPBearer(auto_error=False)
API_TOKEN = os.getenv("CDSS_API_TOKEN")


def require_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if credentials:
        token = credentials.credentials
        # Accept either static API token or valid JWT
        if API_TOKEN and token == API_TOKEN:
            return token
        if decode_token(token):
            return token
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
