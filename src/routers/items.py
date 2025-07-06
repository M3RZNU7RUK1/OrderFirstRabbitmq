from fastapi import APIRouter, Depends, HTTPException  
from src.servies.item_service import ItemsService, get_items_service
from src.schemas.items import ItemResponse
from src.utils.security import auth

class ItemRouter:
    def __init__(self):
        self.router = APIRouter(tags=["Items"])
        self._setup_routers()

    def _setup_routers(self):
        self.router.get("/search")(self.find_item)
        self.router.post("/add_item", response_model=ItemResponse)(self.add_item)

    async def find_item(self,title: str,  item_service: ItemsService = Depends(get_items_service)):
        items = await item_service.find_items(title=title)
        return items
    
    async def add_item(self, title: str, description: str, price: int, 
                       role: str = Depends(auth.access_token_required), 
                        item_service: ItemsService = Depends(get_items_service)):
        if role == "admin":
            item = await item_service.add_item(title=title, description=description, price=price)
            return item
        else:
            raise HTTPException(status_code=400, detail="Бро ты не админ что бы такое вытворять :-0")
