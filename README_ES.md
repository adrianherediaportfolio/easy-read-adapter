# Easy Read Adapter

[![CI](https://github.com/adrianherediaportfolio/easy-read-adapter/actions/workflows/ci.yml/badge.svg)](https://github.com/adrianherediaportfolio/easy-read-adapter/actions)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![Licencia](https://img.shields.io/badge/Licencia-Propietaria-red)](LICENSE)

Easy Read Adapter ayuda a los equipos educativos a preparar textos en español para estudiantes con dislexia, autismo y otras necesidades de apoyo. Añade pictogramas por frase y puntuaciones de legibilidad en español.

## Funciones

- Adapta texto pegado y archivos PDF o TXT.
- Usa OpenAI si hay una clave configurada. Las reglas locales funcionan sin esa clave y sin conexión.
- Elige Lectura Fácil o una adaptación más sencilla.
- Compara las puntuaciones INFLESZ del texto original y del adaptado.
- Busca hasta tres pictogramas de ARASAAC por frase.
- Cambia la fuente, el tamaño del texto, el espacio entre líneas y entre letras.
- Guarda y abre el historial de adaptaciones.
- Imprime una copia limpia o usa la opción PDF del navegador.

Los pictogramas de ARASAAC tienen licencia CC BY-NC-SA y son para uso no comercial. La API y la interfaz muestran esta atribución:

> Pictogramas: Sergio Palao. Origen: ARASAAC (http://www.arasaac.org). Licencia: CC (BY-NC-SA). Propiedad: Gobierno de Aragón (España)

## Arquitectura

```text
easy-read-adapter/
├── backend/                 # FastAPI, reglas locales, OpenAI, SQLite
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

La API guarda las adaptaciones en SQLite. El frontend se comunica con la API mediante `/api`. Consulta [docs/api-contract.md](docs/api-contract.md) para el contrato que utiliza `learning-support-hub`.

## Inicio rápido

### Backend

```bash
cd backend
cp ../.env.example .env
python3.11 -m venv .venv
source .venv/bin/activate
pip install ".[dev]"
uvicorn src.main:app --reload
```

La documentación de la API está en `http://localhost:8000/docs`. Las reglas locales funcionan sin clave de OpenAI. Define `OPENAI_API_KEY` en `backend/.env` para activar OpenAI.

### Frontend

```bash
cd frontend
cp ../.env.example .env
npm ci
npm run dev
```

Abre `http://localhost:5173`.

### Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: `http://localhost:3000`
- API: `http://localhost:8000/docs`

## Configuración

| Variable | Uso |
| --- | --- |
| `OPENAI_API_KEY` | Activa la adaptación con OpenAI. Si está vacía, se usan las reglas locales. |
| `OPENAI_MODEL` | Modelo de OpenAI. El valor inicial es `gpt-4o-mini`. |
| `API_KEY` | Clave opcional para `/api/*`, excepto `/api/health`. Vacía significa autenticación desactivada. |
| `VITE_API_KEY` | Valor incluido en la build del frontend. Si usas `API_KEY`, debe tener el mismo valor. |
| `DATABASE_PATH` | Ruta del archivo SQLite. El valor inicial es `./data/easy_read.db`. |
| `DEBUG` | Activa la configuración de depuración. El valor inicial es `false`. |

El navegador recibe `VITE_API_KEY` dentro de su bundle. Úsala solo en despliegues privados con usuarios de confianza.

## API

| Método | Ruta | Descripción |
| --- | --- | --- |
| `POST` | `/api/adaptations` | Adapta texto en JSON. |
| `POST` | `/api/adaptations/upload` | Adapta un archivo PDF o TXT. |
| `GET` | `/api/adaptations` | Lista las adaptaciones guardadas. |
| `GET` | `/api/adaptations/{id}` | Consulta una adaptación. |
| `DELETE` | `/api/adaptations/{id}` | Elimina una adaptación. |
| `GET` | `/api/health` | Comprueba el servicio y la configuración de OpenAI. |

El contrato completo está en [docs/api-contract.md](docs/api-contract.md).

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

## Privacidad

Las reglas locales no envían texto a servicios externos. El texto se envía a OpenAI solo si se configura `OPENAI_API_KEY`. Si se activan los pictogramas, las búsquedas envían algunas palabras a ARASAAC. Las adaptaciones se guardan en el archivo SQLite configurado.

## Compatibilidad

[`learning-support-hub`](https://github.com/adrianherediaportfolio/learning-support-hub) puede solicitar adaptaciones mediante la API documentada y guardar las frases y los pictogramas de la respuesta. El campo `source` identifica a la aplicación que hace la llamada.

## Licencia

Este proyecto es propietario. Todos los derechos están reservados. Consulta [LICENSE](LICENSE).
