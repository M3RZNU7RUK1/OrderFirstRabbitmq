from fastapi import Depends 
from src.servies.order_service import OrdersService, get_orders_service 
from src.utils.security import auth
from src.schemas.orders import OrderResponse
from faststream.rabbit.fastapi import RabbitRouter
from src.servies.user_service import UserService, get_user_service 
class OrderRourer:
    def __init__(self):
        self.router = RabbitRouter(tags=["Orders"])
        self._setup_routers()
        
    def _setup_routers(self):
        self.router.get("/find_orders")(self.find_orders)
        self.router.post("/create_order", response_model=OrderResponse)(self.create_order)
        self.router.delete("/delete_order")(self.del_order)

    async def find_orders(self, title: str
                          , token: str = Depends(auth.access_token_required),
                          order_service: OrdersService = Depends(get_orders_service)):
        orders = await order_service.find_order(title=title, user_id=int(token.sub))
        return orders 
    async def create_order(self, item_id: int, 
                        token: str = Depends(auth.access_token_required),
                        order_service: OrdersService = Depends(get_orders_service),
                        user_service: UserService = Depends(get_user_service)):
        order = await order_service.create_order(item_id=item_id, user_id=int(token.sub))
        user = await user_service.get_profile(user_id=int(token.sub))
        order_dict = {
            "id": order.id,
            "title": order.title,
            "price": order.price,
            "created_at": order.created_at.strftime("%d/%m/%Y, %H:%M"),
            "phone_number": user.phone_number
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
