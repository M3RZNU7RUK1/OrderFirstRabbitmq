from fastapi import APIRouter, Depends, Request
from src.servies.item_service import ItemsService, get_items_service
from src.schemas.items import ItemResponse
from fastapi.exceptions import ResponseValidationError

class ItemRouter:
    def __init__(self):
        self.router = APIRouter(tags=["Items"])
        self._setup_routers()

    def _setup_routers(self):
        self.router.get("/search")(self.find_item)

    async def find_item(self,title: str,  item_service: ItemsService = Depends(get_items_service)):
        items = await item_service.find_items(title=title)
        return items