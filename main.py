import discord
import os
from discord.ext import commands

description = '''Discord bot for a SCP TRP (Text role-play) server.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix='s?', description=description, intents=intents)



# level 3 - Owner
# level 2 - Manager
# level 1 - Mod
# level 0 - Guest

Authorizations = {482547124761002006:3}

def check_access(UserId:int):
    accesslevel = Authorizations.get(UserId)
     
    if accesslevel != None:
        return accesslevel
    else:
        return 0

@bot.event
async def on_ready():
    # Tell the type checker that User is filled up at this point
    assert bot.user is not None
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.CustomActivity("Site systems online."),status=discord.Status.online)

@bot.command()
async def set_status(ctx:commands.Context, *message):
    if check_access(ctx.author.id) < 2 :
        await ctx.send(content="**[ACCES DENIED]:** Your access is not high enough.",delete_after=30.0)
        return
    await ctx.send(content="**[ACCES GRANTED]:** Changing status.",delete_after=30.0)
    text = ""
    for s in message:
        text = text + s + " "
    await bot.change_presence(activity=discord.CustomActivity(text),status=discord.Status.online)


@bot.command()
async def get_categories(ctx:commands.Context):
    i = 0
    text = ""
    for category in ctx.guild.categories:
        i += 1
        if len(text) + len(f"{category.name}:{category.id}\n") > 2000:
            await ctx.send(text)
            text = f"{category.name}:{category.id}\n"
        else:
            text += f"{category.name}:{category.id}\n"
    await ctx.send(text)

@bot.command()
async def get_roles(ctx:commands.Context):
    i = 0
    text = ""
    for role in ctx.guild.roles:
        i += 1
        if len(text) + len(f"{role.name}:{role.id}\n") > 2000:
            await ctx.send(text)
            text = f"{role.name}:{role.id}\n"
        else:
            text += f"{role.name}:{role.id}\n"
    await ctx.send(text)

@bot.command()
async def test(ctx:commands.Context):
    await ctx.send(type(ctx))
    async for channel in type():
        await ctx.send(f"the bot is in server: {ctx.guild}")

@bot.command()
async def stop_living(ctx):
    ctx.send("Going off to retire (call me when needed)!")
    await bot.close()

@bot.command()
async def kill(ctx:commands.Context, user:discord.User):
    await ctx.send("*Pulls out a gun.*")
    await ctx.send(f"*Shoots {user.mention}*")

@bot.command()
async def respond_to_me_please(ctx:commands.Context):
    await ctx.reply("no fuck you!")
    

bot.run(BOT_TOKEN)