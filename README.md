# Easy Read Adapter

[![CI](https://github.com/adrianherediaportfolio/easy-read-adapter/actions/workflows/ci.yml/badge.svg)](https://github.com/adrianherediaportfolio/easy-read-adapter/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)

Easy Read Adapter helps educators prepare Spanish texts for students with dyslexia, autism, and other learning support needs. It adds sentence-level pictograms and Spanish readability scores.

## Features

- Adapt pasted text or PDF and TXT files.
- Use OpenAI when a key is configured. Local rules work without that key or a network connection.
- Select Lectura Fácil or a simpler adaptation.
- Review original and adapted INFLESZ scores.
- Find up to three pictograms per sentence through the configurable `own,mulberry,openmoji` chain.
- Adjust font, text size, line spacing, and letter spacing.
- Save and reopen a history of adaptations.
- Print a clean copy or use the browser's PDF option.

Own pictograms are proprietary. Mulberry Symbols and OpenMoji use CC BY-SA 4.0 and allow commercial use. ARASAAC is opt-in only, uses CC BY-NC-SA 4.0, and is for non-commercial use. Configure `PICTOGRAM_PROVIDERS` to choose the chain. The API and interface show only the attributions for sources used.

> Pictogramas: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España)

## Architecture

```text
easy-read-adapter/
├── backend/                 # FastAPI, local rules, OpenAI, SQLite
│   ├── src/
│   │   ├── api.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── services/
│   └── tests/
├── frontend/                # React, TypeScript, Vite, Tailwind
│   └── src/
├── docs/
│   ├── api-contract.md
│   └── architecture.md
├── docker-compose.yml
└── .env.example
```

The API stores adaptations in SQLite. The frontend talks to the API through `/api`. See [docs/api-contract.md](docs/api-contract.md) for the contract used by `learning-support-hub`.

## Quick start

### Backend

```bash
cd backend
cp ../.env.example .env
python3.11 -m venv .venv
source .venv/bin/activate
pip install ".[dev]"
uvicorn src.main:app --reload
```

The API documentation is available at `http://localhost:8000/docs`. The local rules work without an OpenAI key. Set `OPENAI_API_KEY` in `backend/.env` to enable OpenAI.

### Frontend

```bash
cd frontend
cp ../.env.example .env
npm ci
npm run dev
```

Open `http://localhost:5173`.

### Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: `http://localhost:3000`
- API: `http://localhost:8000/docs`

## Configuration

| Variable | Purpose |
| --- | --- |
| `OPENAI_API_KEY` | Enables OpenAI adaptation. Blank uses local rules. |
| `OPENAI_MODEL` | OpenAI model name. Defaults to `gpt-4o-mini`. |
| `API_KEY` | Optional key for `/api/*`, except `/api/health`. Blank disables authentication. |
| `VITE_API_KEY` | Frontend build value. Set it to the same value as `API_KEY` when using the optional key. |
| `DATABASE_PATH` | SQLite file path. Defaults to `./data/easy_read.db`. |
| `DEBUG` | Enables debug configuration. Defaults to `false`. |
| `PUBLIC_BASE_URL` | Absolute base URL used for local pictogram assets. |
| `PICTOGRAM_PROVIDERS` | Comma-separated provider order. Defaults to `own,mulberry,openmoji`. |

The browser receives `VITE_API_KEY` as part of its bundle. Use it only for a private deployment where users are trusted.

## API

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/api/adaptations` | Adapt JSON text. |
| `POST` | `/api/adaptations/upload` | Adapt a PDF or TXT upload. |
| `GET` | `/api/adaptations` | List saved adaptations. |
| `GET` | `/api/adaptations/{id}` | Read an adaptation. |
| `DELETE` | `/api/adaptations/{id}` | Delete an adaptation. |
| `GET` | `/api/health` | Check service and OpenAI configuration. |

The full request and response shape is in [docs/api-contract.md](docs/api-contract.md).

## Tests

```bash
cd backend
ruff check src tests
ruff format --check src tests
pytest

cd ../frontend
npm ci
npm run lint
npm test
npm run typecheck
npm run build
```

## Privacy

The local rules do not send text to an external service. Text is sent to OpenAI only when `OPENAI_API_KEY` is configured. The default pictogram chain uses local catalogs and remote image URLs without lookup requests. ARASAAC lookup requests happen only when explicitly added to `PICTOGRAM_PROVIDERS`. Saved adaptations stay in the configured SQLite database.

## Compatibility

[`learning-support-hub`](https://github.com/adrianherediaportfolio/learning-support-hub) can request adaptations through the documented API and save the returned sentence and pictogram data. The `source` field identifies the calling application.

## License

This project is proprietary. All rights are reserved. See [LICENSE](LICENSE).
