from fastapi import APIRouter, Depends, HTTPException  
from src.servies.order_service import OrdersService, get_orders_service 
from src.utils.security import auth

class OrderRourer:
    def __init__(self):
        self.router = APIRouter(tags=["Items"])
        self._setup_routers()
        
    def _setup_routers(self):
        self.router.get("/find_orders")(self.find_orders)

    async def find_orders(self, title: str
                          , token: str = Depends(auth.access_token_required),
                          order_service: OrdersService = Depends(get_orders_service)):
        orders = await order_service.find_order(user_id=int(token.uid), title=title)
        return orders

        
