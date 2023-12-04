from fastapi import FastAPI
from customer import router as customer_router
from inventory import router as inventory_router
from order import router as order_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items")
async def get_items(v: list[int]):
    return v


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

app.mount("/customers", customer_router.app)
app.mount("/inventory", inventory_router.app)
app.mount("/orders", order_router.app)
