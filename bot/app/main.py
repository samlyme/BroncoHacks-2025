import os
import interactions
from interactions import Client, Intents, Permissions, listen, slash_command, SlashContext, OptionType, slash_default_member_permission, slash_option, Modal, ParagraphText, ShortText, User, Member, component_callback, modal_callback, ComponentContext, ComponentCommand, Button, ButtonStyle, integration_types
from dotenv import load_dotenv

# Create a bot instance with the specified intents
bot = Client(intents=Intents.GUILDS |
             Intents.GUILD_MEMBERS | Intents.GUILD_MESSAGES)
# intents are what events we want to receive from discord, `DEFAULT` is usually fine


@listen()  # this decorator tells snek that it needs to listen for the corresponding event, and run this coroutine
async def on_ready():
    # This event is called when the bot is ready to respond to commands
    print("Ready")
    print(f"This bot is owned by {bot.owner}")


@listen()
async def on_member_join(event: interactions.api.events.discord.MemberAdd):
    print(f"{event.member.username} joined")

    button = Button(
        style=ButtonStyle.PRIMARY,
        label="Fill out join form",
        custom_id="open_join_form"
    )

    try:
        await event.member.send(
            "👋 Welcome to the server! Please click below to fill out the join form:",
            components=button
        )
        print(f"Sent join form button to {event.member.username}")
    except Exception as e:
        print(f"Couldn't DM {event.member.username}: {e}")


@component_callback("open_join_form")
async def on_button_click(ctx: ComponentContext):
    join_modal = Modal(
        ShortText(label="Name", required=True,
                  placeholder="Enter your name", custom_id="name_modal"),
        ShortText(label="Email", required=True,
                  placeholder="Enter your email", custom_id="email_modal"),
        ShortText(label="Student ID", required=True,
                  placeholder="Enter your student ID", custom_id="student_id_modal"),
        title="Join Form",
        custom_id="join_form"
    )
    await ctx.send_modal(join_modal)


@modal_callback("join_form")
async def on_modal_submit(ctx: ComponentContext, name_modal: str, email_modal: str, student_id_modal: str):
    await ctx.send(
        f"✅ Thanks for submitting your info!\n**Name**: {name_modal}\n**Email**: {email_modal}\n**Student ID**: {student_id_modal}",
        ephemeral=True
    )


@listen()
async def on_message_create(event: interactions.api.events.discord.MessageCreate):
    # This event is called when a message is sent in a channel the bot can see
    print(type(event))
    print(f"message received: {event.message.jump_url}")
    if event.message.author.id != bot.user.id:
        await event.message.channel.send("lmao")

# command to create a thread from the current channel


@slash_command(name="chat", description="Create a thread from the current channel")
# string option
@slash_option(
    name="string_option",
    description="A string option for the command",
    required=True,
    opt_type=OptionType.STRING
)
# function that takes a SlashContext and a string option
async def create_thread_with_option(ctx: SlashContext, string_option: str):
    thread = await ctx.channel.create_thread(name=string_option,  # type: ignore
                                             auto_archive_duration=60)  # type: ignore
    await ctx.send(f"Thread created: {thread.mention}")


load_dotenv()
bot.start(os.getenv("DISCORD_TOKEN"))
