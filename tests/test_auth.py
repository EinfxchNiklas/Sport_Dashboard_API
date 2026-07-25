import pytest
from fastapi import HTTPException

from app.api.deps import require_admin
from app.config import settings


def test_require_admin_valid_key():
    result = require_admin(x_api_key=settings.admin_api_key)
    assert result is None


def test_require_admin_wrong_key():
    with pytest.raises(HTTPException) as exc_info:
        require_admin(x_api_key="wrong-key")
    assert exc_info.value.status_code == 401


def test_require_admin_no_key():
    with pytest.raises(HTTPException) as exc_info:
        require_admin(x_api_key=None)
    assert exc_info.value.status_code == 401
