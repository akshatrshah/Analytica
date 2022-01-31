from fastapi import FastAPI,Path,Query,HTTPException,status
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    name:str
    price:int
    brand: Optional[str]=None

class UpdateItem(BaseModel):
    name:Optional[str]=None
    price:Optional[int]=None
    brand: Optional[str] = None

inventory={}

@app.get("/get-item/{item_id}")
def get_item(item_id:int =Path(None,description="The ID of the item you want to see",gt=0)):
    return inventory[item_id]

@app.get("/get-by-name/{item_id")
def get_item(*,item_id:int,name:str=None, test:int):
    for item_id in inventory:
        if inventory[item_id].name==name:
            return inventory[item_id]
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item Name not find")

@app.post("/create-item/{item_id}")
def create_item(item_id:int,item:Item):
    if item_id in inventory:
        raise HTTPException(status_code=400,detail="Item already exists. ")
    inventory[item_id]=item
    return inventory[item_id]

@app.put("/update-item/{item_id")
def update_item(item_id:int, item:Item):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item Id does not exist. ")
    if item.name!=None:
        inventory[item_id].name=item.name
        return inventory[item_id]
    if item.price!=None:
        inventory[item_id].price=item.price
        return inventory[item_id]
    if item.brand!=None:
        inventory[item_id].brand=item.brand
        return inventory[item_id]

@app.delete("/delete-item")
def delete_item(item_id:int=Query(..., description="The ID of the item to be deleted")):
    if item_id not in inventory:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item Name not find")
    del inventory[item_id]
    return{"Succes":"Item Deleted."}