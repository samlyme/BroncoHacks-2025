import discord
from fastapi import FastAPI
from bot import bot


api = FastAPI()

@api.get('/')
async def send():
    print('trigger received')
    channel = bot.get_channel(1363086601994895434) 
    print(type(channel))
    if isinstance(channel, discord.channel.TextChannel):
        await channel.send("trigger received")