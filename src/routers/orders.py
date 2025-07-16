from fastapi import Depends, HTTPException  
from src.servies.order_service import OrdersService, get_orders_service 
from src.utils.security import auth
from src.schemas.orders import OrderResponse
from faststream.rabbit.fastapi import RabbitRouter

class OrderRourer:
    def __init__(self):
        self.router = RabbitRouter(tags=["Orders"])
        self._setup_routers()
        
    def _setup_routers(self):
        self.router.get("/find_orders", response_model=list[OrderResponse])(self.find_orders)
        self.router.post("/create_order", response_model=OrderResponse)(self.create_order)
        self.router.delete("/delete_order")(self.del_order)

    async def find_orders(self, title: str
                          , token: str = Depends(auth.access_token_required),
                          order_service: OrdersService = Depends(get_orders_service)):
        orders = await order_service.find_order(title=title, user_id=int(token.sub))
        return orders
    async def create_order(self, item_id: int, 
                        token: str = Depends(auth.access_token_required),
                        order_service: OrdersService = Depends(get_orders_service)):
        order = await order_service.create_order(item_id=item_id, user_id=int(token.sub))
        
        order_dict = {
            "id": order.id,
            "title": order.title,
            "description": order.description,
            "price": order.price,
            "user_id": order.user_id,
            "created_at": order.created_at,
            "updated_at": order.updated_at
        }

        await self.router.broker.publish(
            order_dict,             
            queue="orders"
        )
        return order
    async def del_order(self, order_id: int,
                        token: str = Depends(auth.access_token_required),
                        order_service: OrdersService = Depends(get_orders_service)
                        ):
        order = await order_service.del_order(order_id=order_id, user_id=int(token.sub))
        return {"message": "deleted"}
