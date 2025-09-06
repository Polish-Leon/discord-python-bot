import discord
import os
import datetime
from discord.ext import commands
from discord import app_commands


description = '''Discord bot for a SCP TRP (Text role-play) server.'''

intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.all()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix='s?', description=description, intents=intents)

BotIntegration = None

BotID = 1407806952209125407

IntercomChnnel = 1413606516828803084

# level 3 - Owner
# level 2 - Manager
# level 1 - Mod
# level 0 - Guest

Authorizations = {482547124761002006:3}

async def check_access(ctx:commands.Context,NeededAccess:int):
    accesslevel = Authorizations.get(ctx.author.id)
     
    if accesslevel != None:
        if accesslevel >= NeededAccess:
            return True
    elif NeededAccess == 0:
        return True
    await ctx.send(content="**[ACCESS DENIED]:** Your access is not high enough.",delete_after=30.0)
    return False

@bot.event
async def on_ready():
    # Tell the type checker that User is filled up at this point
    assert bot.user is not None
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.CustomActivity("Site systems online."),status=discord.Status.online)

    '''current_guild = bot.get_guild(1407418719315038348)
    integrations = await current_guild.integrations()
    
    for integration in integrations:
        if integration.account.id == BotID:
            BotIntegration = integration
    
    if BotIntegration == None:
        print("INTEGRATION NOT FOUND IN THE SERVER!!!!")
        await bot.close()'''
    try:
        sync = await bot.tree.sync()
        print(sync)
    except Exception as e:
        print(e)
    


@bot.tree.command()
@app_commands.describe(status="Write the status that should be given to the bot.")
async def set_status(interaction:discord.Interaction, *status:str):
    await interaction.response.send_message(content="**[ACCESS GRANTED]:** Changing status.",delete_after=30.0)
    text = ""
    for s in status:
        text = text + s + " "
    await bot.change_presence(activity=discord.CustomActivity(text),status=discord.Status.online)

@bot.command()
async def intercom(ctx:commands.Context,*message):
    if not await check_access(ctx,2): return
    await ctx.send(content="**[ACCESS GRANTED]:** Begining transmission.",delete_after=30.0)
    text = ""
    for s in message:
        text = text + s + " "
    channel = ctx.guild.get_channel(IntercomChnnel)
    await channel.send(content=f"# ``INTERCOM ANNOUNCEMENT``\n**Current date: ``{datetime.datetime.now().day}.{datetime.datetime.now().month}.2011``**\n-# Beginning transmission.\n\n_{text}_\n\n-# End of transmission.\n### Secure Contain Protect | Message transmitted by {ctx.author.mention}")
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
    await bot.close()

@bot.command()
async def kill(ctx:commands.Context, user:discord.User):
    await ctx.send("*Pulls out a gun.*")
    await ctx.send(f"*Shoots {user.mention}*")

@bot.command()
async def respond_to_me_please(ctx:commands.Context):
    await ctx.reply("no fuck you!")
    

bot.run(BOT_TOKEN)