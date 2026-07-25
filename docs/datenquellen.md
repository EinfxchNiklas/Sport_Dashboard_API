# Datenquellen

Die Sport Dashboard API bezieht ihre Daten aus drei externen APIs. Dieser Artikel beschreibt jede Quelle, welche Umgebungsvariablen benötigt werden und wie du die Keys einträgst.

> **Hinweis:** Web-Crawler (Scraping) sind im aktuellen Stand bewusst nicht enthalten und folgen in einer späteren Ausbaustufe.

---

## OpenF1 (Formel 1)

**Website:** [https://openf1.org](https://openf1.org)

OpenF1 ist eine kostenlose, öffentliche API für Formel-1-Daten (Fahrer, Rennen, Sessions, Telemetrie).

- **API-Schlüssel:** Nicht erforderlich
- **Zugehörige Modelle:** `Race`, `Driver`
- **Zugehörige Endpunkte:** `/api/v1/f1/races`, `/api/v1/f1/drivers`

### Umgebungsvariablen

| Variable            | Pflicht | Beschreibung                                          |
|---------------------|---------|-------------------------------------------------------|
| `OPENF1_BASE_URL`   | Nein    | Basis-URL der API. Standard: `https://api.openf1.org/v1` |

Da kein API-Schlüssel nötig ist, kann `OPENF1_BASE_URL` entweder weggelassen (Standard wird verwendet) oder auf eine eigene Instanz gesetzt werden.

---

## API-Football (Fußball / Bundesliga)

**Website:** [https://www.api-football.com/](https://www.api-football.com/)

API-Football bietet umfangreiche Fußballdaten für hunderte Ligen weltweit, darunter die Bundesliga.

- **API-Schlüssel:** Erforderlich (kostenpflichtig, mit kostenlosem Kontingent für Tests)
- **Zugehörige Modelle:** `Competition`, `Team`, `Match`
- **Zugehörige Endpunkte:** `/api/v1/bundesliga/table`, `/api/v1/bundesliga/matches`

### Key besorgen

1. Registriere dich auf [https://www.api-football.com/](https://www.api-football.com/).
2. Wähle einen Plan (der kostenlose Plan reicht für Tests).
3. Deinen API-Schlüssel findest du im Dashboard unter „My Subscriptions" oder „API Keys".

### Umgebungsvariablen

| Variable                | Pflicht | Beschreibung                              |
|-------------------------|---------|-------------------------------------------|
| `API_FOOTBALL_KEY`      | Ja      | Dein API-Schlüssel von api-football.com   |
| `API_FOOTBALL_BASE_URL` | Nein    | Basis-URL. Standard laut `.env.example`   |

---

## Tank01 (NFL)

**RapidAPI-Seite:** [https://rapidapi.com/tank01/api/tank01-nfl-live-in-game-real-time-statistics-nfl](https://rapidapi.com/tank01/api/tank01-nfl-live-in-game-real-time-statistics-nfl)

Tank01 stellt NFL-Live- und Historikdaten bereit und wird über die RapidAPI-Plattform bezogen.

- **API-Schlüssel:** Erforderlich (RapidAPI-Konto nötig)
- **Zugehörige Modelle:** `NflTeam`
- **Zugehörige Endpunkte:** `/api/v1/nfl/teams`, `/api/v1/nfl/games`

### Key besorgen

1. Registriere dich auf [https://rapidapi.com/](https://rapidapi.com/).
2. Öffne die Tank01-NFL-API-Seite (Link oben).
3. Klicke auf „Subscribe to Test" und wähle einen Plan.
4. Deinen Key findest du unter „Security" → „X-RapidAPI-Key" in der API-Konsole.

### Umgebungsvariablen

| Variable      | Pflicht | Beschreibung                                    |
|---------------|---------|-------------------------------------------------|
| `TANK01_KEY`  | Ja      | Dein `X-RapidAPI-Key` von RapidAPI              |
| `TANK01_HOST` | Ja      | Der RapidAPI-Host, z. B. `tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com` |

---

## Keys in `.env` eintragen

Öffne die Datei `.env` im Projekt-Root und trage die Werte ein:

```dotenv
# Formel 1 (kein Key nötig)
OPENF1_BASE_URL=https://api.openf1.org/v1

# Fußball / Bundesliga
API_FOOTBALL_KEY=dein_api_football_schluessel
API_FOOTBALL_BASE_URL=https://v3.football.api-sports.io

# NFL
TANK01_KEY=dein_rapidapi_schluessel
TANK01_HOST=tank01-nfl-live-in-game-real-time-statistics-nfl.p.rapidapi.com
```

> **Sicherheitshinweis:** Füge die `.env`-Datei niemals in ein öffentliches Git-Repository ein. Sie ist in `.gitignore` ausgeschlossen.
