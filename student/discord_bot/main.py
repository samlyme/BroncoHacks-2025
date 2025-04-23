import asyncio
import logging
import os
from dotenv import load_dotenv
import uvicorn

from bot import bot
from triggers import api


load_dotenv()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

TOKEN = os.getenv('DISCORD_TOKEN') or input('Input discord token: ')

async def run_web():
    config = uvicorn.Config(api, host="0.0.0.0", port=42069, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    await asyncio.gather(
        bot.start(TOKEN),
        run_web(),
    )

if __name__ == "__main__":
    asyncio.run(main())