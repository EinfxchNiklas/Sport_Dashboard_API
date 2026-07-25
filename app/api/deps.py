from fastapi import Header, HTTPException, status

from app.config import settings
from app.database.session import get_db

__all__ = ["get_db"]


def require_admin(x_api_key: str | None = Header(default=None, alias="X-API-Key")) -> None:
    if not x_api_key or x_api_key != settings.admin_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ungültiger oder fehlender API-Key")
