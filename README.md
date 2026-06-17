# File Explorer

A browser-based file system (folders, subfolders, and files) — built
with FastAPI, React, and PostgreSQL, running in Docker.

## Stack

- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Frontend:** React (Vite)
- **Database:** PostgreSQL
- **Infrastructure:** Docker Compose (with hot-reload for dev)
- **Dev tools:** pgAdmin at http://localhost:5050

## Project structure

```
.
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── requirements.txt
│   ├── servers.json               # pgAdmin auto-registration
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   │       └── 0001_create_folders_and_files.py
│   ├── app/
│   │   ├── main.py                # FastAPI app, CORS, lifespan, routers
│   │   ├── config.py              # Pydantic settings (DATABASE_URL etc.)
│   │   ├── database.py            # SQLAlchemy engine / session / get_db
│   │   ├── models.py              # Folder and File ORM models
│   │   ├── schemas.py             # Pydantic request/response schemas
│   │   ├── crud.py                # Database query functions
│   │   └── routers/
│   │       ├── folders.py         # browse / create / delete folders
│   │       ├── files.py           # create / delete files
│   │       └── search.py          # exact search + autocomplete
│   └── tests/
│       ├── conftest.py            # test DB, client fixture
│       ├── test_health.py
│       └── test_nodes.py
└── frontend/
    ├── Dockerfile
    ├── package.json
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── api.js                 # backend API client
        └── components/
            ├── FileExplorer.jsx
            ├── Breadcrumbs.jsx
            ├── CreateItemForm.jsx
            └── SearchBar.jsx
```

## Running the application

1. Copy the environment template:

   ```bash
   cp .env.example .env
   ```

2. Build and start everything:

   ```bash
   docker compose up --build
   ```

   On startup the backend container automatically runs
   `alembic upgrade head` before launching the server, so the database
   schema is always in sync.

3. Once running:

   | Service        | URL                           |
   | -------------- | ----------------------------- |
   | Frontend       | http://localhost:5173          |
   | Backend API    | http://localhost:8000          |
   | Swagger UI     | http://localhost:8000/docs     |
   | pgAdmin        | http://localhost:5050          |

   In pgAdmin, expand **Servers → File Explorer DB → Databases →
   fileexplorer → Schemas → Tables** to browse the data.

To stop: `docker compose down` (add `-v` to also drop the database
volume and start fresh).

## Running without Docker (optional)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate       # venv\Scripts\activate on Windows
pip install -r requirements.txt
export DATABASE_URL=postgresql://fileexplorer:fileexplorer@localhost:5432/fileexplorer
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Database migrations (Alembic)

Generate a new migration after changing a model:

```bash
docker compose exec backend alembic revision --autogenerate -m "describe the change"
```

Apply migrations manually (also runs automatically on startup):

```bash
docker compose exec backend alembic upgrade head
```

Roll back the last migration:

```bash
docker compose exec backend alembic downgrade -1
```

## API

| Method | Path                          | Description                       |
| ------ | ----------------------------- | --------------------------------- |
| GET    | `/folders?parent_id=`         | Browse a folder (subfolders + files) |
| POST   | `/folders`                    | Create a folder                   |
| DELETE | `/folders/{id}`               | Delete a folder (cascades)        |
| POST   | `/files`                      | Create a file                     |
| DELETE | `/files/{id}`                 | Delete a file                     |
| GET    | `/search?q=&folder_id=`       | Exact-name search                 |
| GET    | `/search/autocomplete?q=`     | Top-10 "starts with" suggestions  |

Full interactive docs at http://localhost:8000/docs while the backend
is running.

## Features

- [ ] Create folders and subfolders
- [ ] Create files within folders
- [ ] Browse a folder's contents (subfolders + files)
- [ ] Exact-name search (within a folder / globally)
- [ ] "Starts with" autocomplete (top 10 results)
- [ ] Delete folders (cascades to all contents)
- [ ] Delete files

## Notes / assumptions

TODO: document any assumptions or trade-offs made during implementation.
