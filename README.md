# FastAPI Todo Demo

A simple todo CRUD REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL**.

## Features

- Full CRUD for todos (create, list, read, partial/full update, delete)
- Versioned routes under `/v1`
- Pydantic v2 request/response validation with ORM serialization
- Interactive API docs via Swagger UI and ReDoc
- Database configured entirely from environment variables — no credentials in source

## Tech Stack

| Component  | Technology            |
|------------|-----------------------|
| Framework  | FastAPI               |
| ORM        | SQLAlchemy 2.x        |
| Database   | MySQL (mysql-connector-python) |
| Validation | Pydantic v2           |
| Server     | Uvicorn               |

## Project Structure

```
fastapi-todo-demo/
├── main.py           # FastAPI app, routes, and API metadata
├── database.py       # Engine, session factory, env-var config
├── models.py         # SQLAlchemy ORM model (Todo)
├── schemas.py        # Pydantic schemas (Todo, TodoRead, TodoPatch)
├── repositories.py   # Database access / CRUD helpers
├── data.sql          # Reference MySQL table definition
├── requirements.txt  # Pinned dependencies
└── .env.example      # Environment variable template
```

## Getting Started

### 1. Prerequisites

- Python 3.10+
- A running MySQL server

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create the database

```bash
mysql -uroot -p -e "CREATE DATABASE IF NOT EXISTS todos;"
```

### 4. Configure the connection

Copy the template and adjust the values, then load it into your shell:

```bash
cp .env.example .env
# edit .env with your credentials
set -a; source .env; set +a
```

The app reads either a full `DB_URL`, or the individual parts:

| Variable      | Default       | Description                       |
|---------------|---------------|-----------------------------------|
| `DB_URL`      | *(built)*     | Full SQLAlchemy URL (overrides parts) |
| `DB_USER`     | `root`        | MySQL user                        |
| `DB_PASSWORD` | `root`        | MySQL password                    |
| `DB_HOST`     | `127.0.0.1`   | MySQL host                        |
| `DB_PORT`     | `3306`        | MySQL port                        |
| `DB_NAME`     | `todos`       | Database name                     |

Tables are created automatically on startup from the ORM models.

### 5. Run the server

```bash
uvicorn main:app --reload
```

Then open:

- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc
- OpenAPI schema → http://127.0.0.1:8000/openapi.json

## API Endpoints

All endpoints are prefixed with `/v1`.

| Method   | Path                | Description        | Success Status |
|----------|---------------------|--------------------|----------------|
| `GET`    | `/v1/todos`         | List all todos     | `200 OK`       |
| `POST`   | `/v1/todos`         | Create a new todo  | `201 Created`  |
| `GET`    | `/v1/todos/{id}`    | Get todo detail    | `200 OK`       |
| `PATCH`  | `/v1/todos/{id}`    | Partial update     | `200 OK`       |
| `PUT`    | `/v1/todos/{id}`    | Full update        | `200 OK`       |
| `DELETE` | `/v1/todos/{id}`    | Delete a todo      | `204 No Content` |

### curl Examples

The examples below assume the server is running at `http://127.0.0.1:8000`.

#### Create a todo — `POST /v1/todos`

```bash
curl -X POST http://127.0.0.1:8000/v1/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Read FastAPI docs", "status": "Doing"}'
```

Response (`201 Created`):

```json
{
  "title": "Read FastAPI docs",
  "status": "Doing",
  "id": 1,
  "created_at": "2026-07-17T10:00:00",
  "updated_at": "2026-07-17T10:00:00"
}
```

#### List all todos — `GET /v1/todos`

```bash
curl http://127.0.0.1:8000/v1/todos
```

Response (`200 OK`):

```json
[
  {
    "title": "Read FastAPI docs",
    "status": "Doing",
    "id": 1,
    "created_at": "2026-07-17T10:00:00",
    "updated_at": "2026-07-17T10:00:00"
  }
]
```

#### Get a single todo — `GET /v1/todos/{id}`

```bash
curl http://127.0.0.1:8000/v1/todos/1
```

Response (`200 OK`):

```json
{
  "title": "Read FastAPI docs",
  "status": "Doing",
  "id": 1,
  "created_at": "2026-07-17T10:00:00",
  "updated_at": "2026-07-17T10:00:00"
}
```

Returns `400 Bad Request` with `{"detail": "Todo is not found"}` if the id does not exist.

#### Partially update a todo — `PATCH /v1/todos/{id}`

Only the fields you send are changed; omit the rest.

```bash
curl -X PATCH http://127.0.0.1:8000/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "Done"}'
```

Response (`200 OK`):

```json
{
  "title": "Read FastAPI docs",
  "status": "Done",
  "id": 1,
  "created_at": "2026-07-17T10:00:00",
  "updated_at": "2026-07-17T10:05:00"
}
```

#### Fully update a todo — `PUT /v1/todos/{id}`

Both `title` and `status` are required.

```bash
curl -X PUT http://127.0.0.1:8000/v1/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Read FastAPI docs thoroughly", "status": "Done"}'
```

Response (`200 OK`):

```json
{
  "title": "Read FastAPI docs thoroughly",
  "status": "Done",
  "id": 1,
  "created_at": "2026-07-17T10:00:00",
  "updated_at": "2026-07-17T10:10:00"
}
```

#### Delete a todo — `DELETE /v1/todos/{id}`

```bash
curl -i -X DELETE http://127.0.0.1:8000/v1/todos/1
```

Returns `204 No Content` on success, or `400 Bad Request` with
`{"detail": "Todo is not found"}` if the id does not exist.

## License

Released under the [MIT License](https://opensource.org/licenses/MIT).

## Author

**Hendi Santika**
- Email: hendisantika@yahoo.co.id
- GitHub: [@hendisantika](https://github.com/hendisantika)
