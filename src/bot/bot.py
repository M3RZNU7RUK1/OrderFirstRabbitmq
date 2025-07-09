from aiogram import Dispatcher, Bot
from aiogram.types import Message
from dotenv import load_dotenv 
from faststream.rabbit.fastapi import RabbitBroker 
import asyncio 
import logging 
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

dp = Dispatcher()

bot = Bot(token=TOKEN)

broker = RabbitBroker()

@broker.subscriber("orders")
async def handle_orders(data: str):
    await bot.send_message(
        chat_id=1965822435,
        text=data,
    )

async def main():
    async with broker as br:
        await br.start()
        await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
