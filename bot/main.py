import os
import interactions
from interactions import Client, Intents, listen
from dotenv import load_dotenv

bot = Client(intents=Intents.DEFAULT)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_message_create(event: interactions.api.events.discord.MessageCreate):
    # This event is called when a message is sent in a channel the bot can see
    print(type(event))
    print(f"message received: {event.message.jump_url}")
    if event.message.author.id != bot.user.id:
        await event.message.channel.send("lmao")


load_dotenv()
bot.start(os.getenv("DISCORD_TOKEN"))
