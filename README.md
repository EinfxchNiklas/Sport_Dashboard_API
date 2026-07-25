# Sport Dashboard API

Eine zentrale REST-API für Sport-Live- und Historikdaten. Aktuell unterstützte Sportarten:

- **Bundesliga** – Tabelle & Spielpläne (via API-Football)
- **Formel 1** – Rennen & Fahrer (via OpenF1)
- **NFL** – Teams & Spiele (via Tank01 / RapidAPI)

> **Hinweis:** Web-Crawler sind im aktuellen Stand nicht enthalten und folgen in einer späteren Ausbaustufe.

---

## Features

- REST-API mit FastAPI – automatische Swagger UI (`/docs`) und ReDoc (`/redoc`)
- Datenbankanbindung via SQLAlchemy 2.0 + PostgreSQL (psycopg v3)
- Schemavorvalidierung mit Pydantic v2
- Datenbankmigrationen mit Alembic
- Admin-Endpunkte zum Auslösen von Datenimporten (geschützt per `X-API-Key`)
- Hintergrundaufgaben mit APScheduler
- Deployment-Ready für [Render](https://render.com) (`render.yaml`)
- Lokale Entwicklung mit Docker Compose (PostgreSQL + pgAdmin)

---

## Tech-Stack

| Komponente         | Technologie                        |
|--------------------|------------------------------------|
| Sprache            | Python 3.14                        |
| Web-Framework      | FastAPI + Uvicorn                  |
| Datenbank          | PostgreSQL (psycopg v3)            |
| ORM / Migrationen  | SQLAlchemy 2.0 + Alembic           |
| Schemas            | Pydantic v2                        |
| HTTP-Client        | httpx                              |
| Scheduler          | APScheduler                        |
| Tests              | pytest                             |

---

## Projektstruktur

```
Sport_Dashboard_API/
├── main.py                    # Anwendungs-Einstiegspunkt (FastAPI + Lifespan)
├── requirements.txt
├── alembic.ini
├── docker-compose.yml         # Lokale DB: PostgreSQL + pgAdmin
├── render.yaml                # Render-Deployment-Blueprint
├── .env.example               # Vorlage für Umgebungsvariablen
├── app/
│   ├── config.py              # Einstellungen via Pydantic Settings
│   ├── logging_config.py
│   ├── api/
│   │   └── v1/                # FastAPI-Router (health, bundesliga, f1, nfl, admin)
│   ├── models/                # SQLAlchemy-Modelle
│   ├── schemas/               # Pydantic-Schemas (Base/Create/Read)
│   ├── services/              # Import-Services (Fetch → Normalize → Upsert)
│   │   └── datasources/       # HTTP-Clients (OpenF1, API-Football, Tank01)
│   ├── schedulers/            # APScheduler-Integration
│   └── database/              # Session, Seed
├── migrations/                # Alembic-Migrationen
├── tests/                     # pytest-Tests
└── docs/                      # Dokumentation (Deutsch)
```

---

## Schnellstart

### 1. Virtuelle Umgebung aktivieren

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Umgebungsvariablen einrichten

```powershell
copy .env.example .env
```

Öffne `.env` und trage deine Werte ein – insbesondere `DATABASE_URL`, `ADMIN_API_KEY` und die API-Keys für die Datenquellen.
Details: [docs/datenquellen.md](docs/datenquellen.md)

### 3. Datenbank starten (Docker)

```powershell
docker compose up -d
```

Details zur Docker-Einrichtung (auch für Einsteiger): [docs/docker-anleitung.md](docs/docker-anleitung.md)

### 4. Migrationen ausführen

```powershell
alembic upgrade head
```

### 5. Seed-Daten einspielen (optional)

```powershell
python -m app.database.seed
```

### 6. Anwendung starten

```powershell
uvicorn main:app --reload
```

API erreichbar unter: [http://localhost:8000](http://localhost:8000)
Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API-Endpunkte (Überblick)

Alle Endpunkte haben den Präfix `/api/v1`.

| Methode | Pfad                              | Auth         | Beschreibung                          |
|---------|-----------------------------------|--------------|---------------------------------------|
| GET     | `/health`                         | Nein         | Health Check                          |
| GET     | `/bundesliga/table`               | Nein         | Bundesliga-Tabelle                    |
| GET     | `/bundesliga/matches`             | Nein         | Bundesliga-Spiele                     |
| GET     | `/f1/races`                       | Nein         | F1-Rennen                             |
| GET     | `/f1/drivers`                     | Nein         | F1-Fahrer                             |
| GET     | `/nfl/teams`                      | Nein         | NFL-Teams                             |
| GET     | `/nfl/games`                      | Nein         | NFL-Spiele                            |
| POST    | `/admin/import/bundesliga`        | `X-API-Key`  | Bundesliga-Daten importieren          |
| POST    | `/admin/import/f1/races`          | `X-API-Key`  | F1-Rennen importieren                 |
| POST    | `/admin/import/f1/drivers`        | `X-API-Key`  | F1-Fahrer importieren                 |
| POST    | `/admin/import/nfl/teams`         | `X-API-Key`  | NFL-Teams importieren                 |
| POST    | `/admin/import/nfl/games`         | `X-API-Key`  | NFL-Spiele importieren                |

Vollständige API-Referenz: [docs/api.md](docs/api.md)

---

## Authentifizierung

Admin-Endpunkte erfordern den HTTP-Header:

```
X-API-Key: <dein ADMIN_API_KEY>
```

Der Wert wird in der Umgebungsvariable `ADMIN_API_KEY` definiert. Öffentliche GET-Endpunkte benötigen keinen Key.

---

## Dokumentation

| Dokument                                          | Inhalt                                      |
|---------------------------------------------------|---------------------------------------------|
| [docs/entwicklung.md](docs/entwicklung.md)        | Lokales Setup, Tests, neue Migrationen      |
| [docs/docker-anleitung.md](docs/docker-anleitung.md) | Docker-Einrichtung für Einsteiger        |
| [docs/api.md](docs/api.md)                        | Vollständige API-Referenz                   |
| [docs/datenquellen.md](docs/datenquellen.md)      | OpenF1, API-Football, Tank01 – Keys & Setup |
| [docs/deployment.md](docs/deployment.md)          | Deployment auf Render                       |

---

## Tests

```powershell
pytest -q
```
