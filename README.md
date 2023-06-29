# PostgreSQL Notify

Use PostgreSQL `NOTIFY` and `LISTEN` to send and receive notifications. built with `fastapi`, `psycopg`, `websockets` and `vuejs`.

## Example

Run docker of PostgreSQL:

```bash
docker run -d -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=postgres -p 5432:5432 postgres postgres
```

The `DB_URL` environment variable needs to be set before each run:

```bash
export DB_URL=postgres://postgres:postgres@localhost/postgres
```

Run the server:

```bash
uvicorn app:app
```

Send a message:

```bash
python send_message.py
```
