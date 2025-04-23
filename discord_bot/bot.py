import discord


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