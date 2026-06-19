# My First FastAPI App

A simple beginner project built with **FastAPI** and served using **Uvicorn**. It demonstrates the core building blocks of a web API: a root endpoint, a path parameter, a query parameter, and full GET/POST endpoints backed by a Pydantic model.

## Tools Used

- Python
- FastAPI
- Uvicorn

## Project Structure

```
fastapi_project.py   # all application code lives in this single file
```

## Setup

1. Create and activate a virtual environment (if you haven't already):
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install fastapi "uvicorn[standard]"
   ```

## Running the App

From the project folder, run:

```bash
uvicorn fastapi_project:app --reload
```

You should see output similar to:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

The `--reload` flag automatically restarts the server whenever you save changes to the file — useful while developing.

## Interactive Docs

FastAPI auto-generates interactive API documentation. Once the server is running, open:

```
http://127.0.0.1:8000/docs
```

Every endpoint below can be tested directly from this page using the "Try it out" button — including POST requests.

## Endpoints

| Method | Path            | Description                                      |
|--------|-----------------|---------------------------------------------------|
| GET    | `/`             | Returns a welcome message                          |
| GET    | `/greet/{name}` | Path parameter — greets whoever's name is in the URL |
| GET    | `/search`       | Query parameter — searches for `q`, defaults to "FastAPI" if omitted |
| GET    | `/items`        | Returns all items currently stored                  |
| GET    | `/items/{item_id}` | Returns a single item by ID, or 404 if not found |
| POST   | `/items`        | Creates a new item from a JSON request body          |

### Example: Root

```
GET http://127.0.0.1:8000/
```
```json
{"message": "Welcome to my first FastAPI app!"}
```

### Example: Path Parameter

```
GET http://127.0.0.1:8000/greet/Shrisakthi
```
```json
{"message": "Hello, Shrisakthi! Welcome to FastAPI."}
```

### Example: Query Parameter

```
GET http://127.0.0.1:8000/search?q=python
```
```json
{"you_searched_for": "python"}
```

Without a query value, it falls back to the default:

```
GET http://127.0.0.1:8000/search
```
```json
{"you_searched_for": "FastAPI"}
```

### Example: Create an Item (POST)

In Postman:
- Method: `POST`
- URL: `http://127.0.0.1:8000/items`
- Body → raw → JSON:
  ```json
  {
    "name": "Notebook",
    "price": 2.5
  }
  ```

Response:
```json
{
  "id": 1,
  "name": "Notebook",
  "price": 2.5,
  "in_stock": true
}
```

### Example: List All Items

```
GET http://127.0.0.1:8000/items
```
```json
{"items": {"1": {"name": "Notebook", "price": 2.5, "in_stock": true}}}
```

### Example: Get a Single Item

```
GET http://127.0.0.1:8000/items/1
```
```json
{"name": "Notebook", "price": 2.5, "in_stock": true}
```

If the ID doesn't exist:
```json
{"detail": "Item not found"}
```

## Notes

- Item storage is **in-memory only** (a plain Python dictionary) — it resets every time the server restarts or reloads. This is intentional for keeping the project simple; it is not meant for persistent/production use.
- Path parameters (like `{name}` or `{item_id}`) are **required** — leaving them blank in the URL results in a 404.
- Query parameters (like `q`) can have **default values**, making them optional.
