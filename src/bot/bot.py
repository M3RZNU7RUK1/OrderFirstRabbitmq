from aiogram import Dispatcher, Bot
from dotenv import load_dotenv 
from faststream.rabbit.fastapi import RabbitBroker 
import asyncio 
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

dp = Dispatcher()

bot = Bot(token=TOKEN)

broker = RabbitBroker()

@broker.subscriber("orders")
async def handle_orders(order_data: dict):
    message = (
        "🛒 *Новый заказ!*\n\n"
        f"📌 *Номер заказа:* {order_data['id']}\n"
        f"📋 *Название:* {order_data['title']}\n"
        f"💰 *Цена:* {order_data['price']} руб.\n"
        f"⏰ *Номер телефона:* {order_data['phone_number']}\n"
        f"📅 *Дата создания заказа:* {order_data['created_at']}"
    )
    
    await bot.send_message(
        chat_id=1965822435,
        text=message,
        parse_mode="Markdown"
    )
@broker.subscriber("deletedorders")
async def handle_deleted_orders(data: str):
    await bot.send_message(
        chat_id=1965822435,
        text=data
    )

async def main():
    async with broker as br:
        await br.start()
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
