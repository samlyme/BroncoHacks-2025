import os
import interactions
from interactions import Client, Intents, Permissions, listen, slash_command, SlashContext, OptionType, slash_default_member_permission, slash_option, Modal, ParagraphText, ShortText, User, Member, component_callback, modal_callback, ComponentContext, ComponentCommand, Button, ButtonStyle, integration_types, ModalContext
from dotenv import load_dotenv
import requests

# Create a bot instance with the specified intents
bot = Client(intents=Intents.GUILDS |
             Intents.GUILD_MEMBERS | Intents.GUILD_MESSAGES | Intents.MESSAGE_CONTENT)


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_member_join(event: interactions.api.events.discord.MemberAdd):
    print(f"{event.member.id} has joined")


@listen()
async def on_member_leave(event: interactions.api.events.discord.MemberRemove):
    print(f"{event.member.id} has left")


@slash_command(name="chat", description="Create a private thread with the bot")
@slash_option(
    name="thread_name",
    description="The name of the private thread",
    required=True,
    opt_type=OptionType.STRING
)
async def create_private_thread(ctx: SlashContext, thread_name: str):
    # Create a private thread in the current channel
    thread = await ctx.channel.create_private_thread(  # type: ignore
        name=thread_name,  # Name of the thread
        auto_archive_duration=60  # Auto-archive duration in minutes # type: ignore
    )

    # Add the user who created the thread to the thread
    await thread.add_member(ctx.author.id)

    # Notify the user privately
    await ctx.send(f"Private thread created: {thread.name}", ephemeral=True)


@listen()
async def on_message_create_in_thread(event: interactions.api.events.discord.MessageCreate):
    # Check if the channel is a thread
    if event.message.channel.type in [
        interactions.ChannelType.GUILD_PUBLIC_THREAD,
        interactions.ChannelType.GUILD_PRIVATE_THREAD
    ] and event.message.author.id != bot.user.id:  # Ignore the bot's own messages
        message_content = event.message.content
        message_user = event.message.author

        # Log the message and user
        print(f"Message in thread: {message_content}")
        print(f"User who sent: {message_user}")

        # Respond to the message in the thread
        await event.message.channel.send(f"Hello {message_user.username}, you said: {message_content}")

load_dotenv()
bot.start(os.getenv("DISCORD_TOKEN"))
