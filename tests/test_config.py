from app.config import Settings, get_settings


def test_timezone():
    settings = get_settings()
    assert settings.timezone == "Europe/Berlin"


def test_app_env_is_set():
    settings = get_settings()
    assert settings.app_env != ""


def test_database_url_normalizes_postgres_scheme():
    s = Settings(database_url="postgres://u:p@h:5432/db")
    assert s.database_url.startswith("postgresql+psycopg://")


def test_database_url_normalizes_postgresql_scheme():
    s = Settings(database_url="postgresql://u:p@h:5432/db")
    assert s.database_url.startswith("postgresql+psycopg://")


def test_database_url_leaves_correct_scheme_unchanged():
    url = "postgresql+psycopg://sport:sport@localhost:5432/sportdb"
    s = Settings(database_url=url)
    assert s.database_url == url
