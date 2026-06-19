from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Create the FastAPI application instance.
# This object is what Uvicorn runs, and what FastAPI uses to
# auto-generate the interactive docs at /docs.
app = FastAPI(
    title="My First FastAPI App",
    description="A simple beginner project demonstrating FastAPI basics.",
    version="1.1.0",
)


# =========================================================
# 1. Root endpoint
# =========================================================
@app.get("/")
def read_root():
    """Returns a simple welcome message."""
    return {"message": "Welcome to my first FastAPI app!"}


# =========================================================
# 2. Path parameter endpoint
# =========================================================
@app.get("/greet/{name}")
def greet(name: str):
    """
    Captures whatever is typed after /greet/ in the URL.
    Path parameters are required - if no value is given,
    FastAPI returns a 404, since the URL itself is incomplete.
    """
    return {"message": f"Hello, {name}! Welcome to FastAPI."}


# =========================================================
# 3. Query parameter endpoint
# =========================================================
@app.get("/search")
def search(q: str = "FastAPI"):
    """
    Reads a value after '?' in the URL, e.g. /search?q=python.
    Query parameters can have defaults, so they're optional -
    if 'q' is left out, it falls back to "FastAPI".
    """
    return {"you_searched_for": q}


# =========================================================
# 4. Pydantic model - defines the shape of data for POST requests
# =========================================================
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True  # optional, defaults to True


# Simple in-memory storage (resets when the server restarts).
items: dict[int, Item] = {}
next_id = 1


# =========================================================
# 5. GET - list all items
# =========================================================
@app.get("/items")
def list_items():
    """Returns every item currently stored."""
    return {"items": items}


# =========================================================
# 6. GET - fetch a single item by ID
# =========================================================
@app.get("/items/{item_id}")
def get_item(item_id: int):
    """Returns one item by ID, or a 404 if it doesn't exist."""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# =========================================================
# 7. POST - create a new item
# =========================================================
@app.post("/items")
def create_item(item: Item):
    """
    Creates a new item from JSON sent in the request body.
    FastAPI validates the incoming data against the Item model
    automatically - missing or wrong-typed fields are rejected
    before this function even runs.
    """
    global next_id
    items[next_id] = item
    created = {"id": next_id, **item.model_dump()}
    next_id += 1
    return created