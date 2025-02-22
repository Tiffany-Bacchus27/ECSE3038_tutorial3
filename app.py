from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from fastapi.responses import JSONResponse

app = FastAPI()

fruits_inv = []

class Fruit(BaseModel):
    name: str
    variety: str
    quantity: int
    supplier: str
    harvest_date: datetime
    creation_date: datetime = None
    available: bool
    price: float 


@app.get ("/api/fruits")
async def get_all_fruits(): 
    available_fruits = [fruit for fruit in fruits_inv if fruit.available]
    return available_fruits


@app.get ("/api/fruit/{id}")
async def get_fruits(id: int):
    if id < 0 or id >= len(fruits_inv):    
        raise HTTPException(status_code=404, detail = "Fruit not found")
    return fruits_inv[id]

@app.post("/api/fruits")
async def add_fruit(fruit: Fruit):
    fruit.creation_date = datetime.now(timezone.utc)
    fruits_inv.append(fruit)
    return JSONResponse(content=fruit.model_dump(), status_code=201)

@app.patch("/api/fruits/{fruit_id}")
async def update_fruit(fruit_id: int, fruit: Fruit):
    if fruit_id < 0 or fruit_id >= len(fruits_inv):
        raise HTTPException(status_code=404, detail="Fruit not found")
    
    existing_fruit = fruits_inv[fruit_id]
    existing_fruit.available = fruit.available
    existing_fruit.price = fruit.price
    existing_fruit.quantity = fruit.quantity

    return existing_fruit

@app.delete("api/fruits/{fruit_id}", status_code=204)
async def delete_fruit(fruit_id: int):
    if fruit_id < 0 or fruit_id >= len(fruits_inv):
        raise HTTPException(status_code=404, detail = "Fruit not found")
    
    fruits_inv[fruit_id].available = False
    return {"message": "Fruit is unavailable"}
    