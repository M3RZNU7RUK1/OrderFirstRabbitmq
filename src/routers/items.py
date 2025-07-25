from fastapi import APIRouter, Depends, HTTPException  
from src.servies.item_service import ItemsService, get_items_service
from src.schemas.items import ItemResponse
from src.utils.security import auth
from src.redisclient.cache import Cache 

class ItemRouter:
    def __init__(self):
        self.router = APIRouter(tags=["Items"])
        self.cache = Cache()
        self._setup_routers()
        
    def _setup_routers(self):
        self.router.get("/search")(self.find_item)
        self.router.post("/add_item", response_model=ItemResponse)(self.add_item)
        self.router.delete("/del_item")(self.del_item)
        
    def _check_admin(self, role: str):
        return True if role == "admin" else False 
        
    async def find_item(self, title: str, item_service: ItemsService = Depends(get_items_service)):
        cached_item = await self.cache.get_cached_item_data(key=title)
        if cached_item:
            return cached_item
        items = await item_service.find_items(title=title)
        items_response = [ItemResponse.model_validate(item) for item in items]
        await self.cache.set_cached_item_data(key=title, value=items_response)
        return items_response

    async def add_item(
        self, 
        title: str, 
        description: str, 
        price: int, 
        token: str = Depends(auth.access_token_required),
        item_service: ItemsService = Depends(get_items_service)
    ):
        if self._check_admin(role=token.role):
            if price <= 0 or price >= 2147483647:
                raise HTTPException(status_code=400, detail="Not enough access rights")
            item = await item_service.add_item(title=title, description=description, price=price)
            item_response = [ItemResponse.model_validate(item)]
            await self.cache.set_cached_item_data(key=title, value=item_response)            
            return item
        else:
            raise HTTPException(status_code=400, detail="Not enough access rights")

    async def del_item(
        self, 
        id: int, 
        token: str = Depends(auth.access_token_required),
        item_service: ItemsService = Depends(get_items_service)
    ):
        if self._check_admin(role=token.role):
            await item_service.del_item(item_id=id)
            return {"message": "deleted"}
        else:
             raise HTTPException(status_code=400, detail="Not enough access rights")
