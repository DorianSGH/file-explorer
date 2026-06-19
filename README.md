# File Explorer

A web-based file system explorer supporting folders, subfolders, and files — with search and autocomplete. Built with FastAPI, React, and PostgreSQL, containerised with Docker.

## Stack

- **Backend:** FastAPI, SQLAlchemy, Alembic
- **Frontend:** React (Vite)
- **Database:** PostgreSQL
- **Infrastructure:** Docker Compose

## Project structure

```
.
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── servers.json              # pgAdmin auto-registration
│   ├── alembic/
│   │   └── versions/
│   │       └── 0001_create_folders_and_files.py
│   ├── app/
│   │   ├── main.py               # App entry point, CORS, lifespan
│   │   ├── config.py             # Settings (DATABASE_URL)
│   │   ├── database.py           # SQLAlchemy engine and session
│   │   ├── models.py             # Folder and File ORM models
│   │   ├── schemas.py            # Pydantic request/response schemas
│   │   ├── logger.py             # Logging configuration
│   │   ├── repositories/
│   │   │   ├── files_repo.py     # File database operations and search
│   │   │   └── folders_repo.py   # Folder database operations
│   │   └── routers/
│   │       ├── files_router.py   # File endpoints
│   │       ├── folders_router.py # Folder endpoints
│   │       └── search_router.py  # Search and autocomplete endpoints
│   └── tests/
│       ├── conftest.py           # Test client and database fixtures
│       ├── test_files.py
│       └── test_folders.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── api.js                # API client
│       ├── App.jsx
│       ├── main.jsx
│       ├── styles.css
│       └── components/
│           ├── Breadcrumbs.jsx
│           ├── CreateItemForm.jsx
│           ├── ErrorBoundary.jsx
│           ├── FileExplorer.jsx  # Main component, state management
│           └── SearchBar.jsx
└── logs/                         # Daily rotating log files
```

## Running the application

1. Copy the environment file:
   ```bash
   cp .env.example .env
   ```

2. Build and start all services:
   ```bash
   docker compose up --build
   ```
   The backend automatically runs `alembic upgrade head` on startup, so the database schema is always up to date.

3. Services:

   | Service     | URL                        |
   |-------------|----------------------------|
   | Frontend    | http://localhost:5173       |
   | Backend API | http://localhost:8000       |
   | Swagger UI  | http://localhost:8000/docs  |
   | pgAdmin     | http://localhost:5050       |

   In pgAdmin, the database is pre-registered under **Servers → File Explorer DB**.

To stop: `docker compose down`. Add `-v` to also clear the database volume.


## Debugging (VSCode)

A VSCode debug configuration is included in `.vscode/launch.json`.

To debug the backend:

1. Start the backend in debug mode:
   ```bash
   # Linux/macOS
   DEBUG_MODE=true docker compose up --build

   # Windows (PowerShell)
   $env:DEBUG_MODE="true"; docker compose up --build
   ```

2. In VSCode, open the Run and Debug panel (Ctrl+Shift+D), select **"Python: Attach to Backend (Docker)"** and click the play button.

3. Set breakpoints in any `.py` file under `backend/` — execution will pause when they are hit.

Note: `--reload` is disabled in debug mode since it conflicts with the debugger. To return to normal development with hot-reload, restart without `DEBUG_MODE`.

## Running tests

Tests use an in-memory SQLite database and do not require a running Postgres instance.

```bash
docker compose exec backend pytest tests/ -v
```

## API

| Method | Path                         | Description                                    |
|--------|------------------------------|------------------------------------------------|
| GET    | `/folders/browse?parent_id=` | List contents of a folder (subfolders + files) |
| GET    | `/folders`                   | List all folders                               |
| GET    | `/folders/{id}`              | Get a folder by ID                             |
| POST   | `/folders`                   | Create a folder                                |
| DELETE | `/folders/{id}`              | Delete a folder and all its contents           |
| GET    | `/files`                     | List all files                                 |
| GET    | `/files/{id}`                | Get a file by ID                               |
| POST   | `/files`                     | Create a file                                  |
| DELETE | `/files/{id}`                | Delete a file                                  |
| GET    | `/search?q=&folder_id=`      | Exact name search                              |
| GET    | `/search/autocomplete?q=`    | Top 10 files starting with query               |

Full interactive documentation is available at `/docs` while the backend is running.

## Database migrations

Generate a migration after changing a model:
```bash
docker compose exec backend alembic revision --autogenerate -m "describe the change"
```

Apply migrations:
```bash
docker compose exec backend alembic upgrade head
```

Roll back the last migration:
```bash
docker compose exec backend alembic downgrade -1
```

## Logs

Application logs are written to both stdout and daily log files under `logs/` in the project root. Log files are named by date (e.g. `2024-11-01.log`) and kept for 30 days.
