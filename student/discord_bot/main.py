# This example requires the 'message_content' intent.

import asyncio
import logging
import os
import discord
from dotenv import load_dotenv
from fastapi import FastAPI
import uvicorn

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return

    if bot.user in message.mentions:
        await message.channel.send(f'{message.author.mention} mentioned me')
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

api = FastAPI()

@api.get('/')
async def send():
    print('trigger received')
    channel = bot.get_channel(1363086601994895434) 
    print(type(channel))
    if isinstance(channel, discord.channel.TextChannel):
        await channel.send("trigger received")

load_dotenv()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

TOKEN = os.getenv('DISCORD_TOKEN') or input('Input discord token: ')
# bot.run(TOKEN, log_handler=handler)

# Run FastAPI in a separate task
async def run_web():
    config = uvicorn.Config(api, host="0.0.0.0", port=8000, log_level="info", loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

# Main function to run both bot and web server
async def main():
    await asyncio.gather(
        bot.start(TOKEN),
        run_web(),
    )

if __name__ == "__main__":
    asyncio.run(main())