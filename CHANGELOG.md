# Changelog

Alle wesentlichen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/).

## [0.1.0] - 2026-07-23

### Hinzugefügt

- Projekt-Fundament: Struktur, Konfiguration, Datenbank-Session, Logging
- SQLAlchemy-2.0-Modelle: Competition, Team, Match, Driver, Race, NflTeam
- Pydantic-v2-Schemas (Base/Create/Read) für alle Entitäten
- FastAPI-Grundgerüst: Health-Endpoint `/api/v1/health`, Admin-Auth via `X-API-Key`, zentraler v1-Router
- Synchrone Datenquellen-Clients für OpenF1, API-Football und Tank01 (httpx)
- Alembic-Setup mit Initial-Migration für alle 6 Tabellen
- Import-Services (Fetch → Normalize → Upsert) für Bundesliga, Formel 1 und NFL
- Minimale Seed-Daten inkl. CLI (`python -m app.database.seed`)
- REST-Endpunkte für Bundesliga, F1, NFL sowie Admin-Import-Endpunkte
- APScheduler-Integration mit dynamischem Match-Monitor und Lifespan-Anbindung
- Deployment-Konfiguration: `docker-compose.yml` (Postgres + pgAdmin) und `render.yaml`; DB-URL-Normalisierung für Render
- Deutschsprachige Dokumentation unter `docs/` und README
