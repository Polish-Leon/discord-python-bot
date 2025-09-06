import discord
import os
import datetime
import mysql.connector
from discord.ext import commands
from discord import app_commands
from discord import ui


T_ACCES_DENIED = "**[ACCESS DENIED]:** Your access is not high enough."
IntercomChnnel = 1413606516828803084



description = "Discord bot for a SCP TRP (Text role-play) server."
intents = discord.Intents.all()
intents.members = True
intents.message_content = True
intents.all()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = commands.Bot(command_prefix='s?', description=description, intents=intents)

class intercom_modal(ui.Modal, title='Intercom Broadcast'):
    broadcast = ui.TextInput(label='Broadcast',required=True,style=discord.TextStyle.long)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(content="**[ACCESS GRANTED]:** Begining transmission.", ephemeral=True)
        channel = interaction.guild.get_channel(IntercomChnnel)
        await channel.send(content=f"# ``INTERCOM ANNOUNCEMENT``\n**Current date: ``{datetime.datetime.now().day}.{datetime.datetime.now().month}.2011``**\n-# Beginning transmission.\n\n_{self.broadcast}_\n\n-# End of transmission.\n### Secure Contain Protect | Message transmitted by {interaction.user.mention}")

    async def on_error(self, interaction: discord.Interaction):
        interaction.response.send_message(content="Broadcast failed.",ephemeral=True)



# level 9 - Owner
# level 8 - RolePlay Manager
# level 7 - RolePlay cordinator
# level 6 - Director
# level 5 - Site Menagment
# level 4 - Site Division Manager
# level 3 - Site Senior employee
# level 2 - Site employee
# level 1 - Site junior employee
# level 0 - Guest

Authorizations = {482547124761002006:9,756962442180821143:8}

def check_access(UserID:int,NeededAccess:int):
    accesslevel = Authorizations.get(UserID)
     
    if accesslevel != None:
        if accesslevel >= NeededAccess:
            return True
    elif NeededAccess == 0:
        return True
    return False


@bot.event
async def on_ready():
    # Tell the type checker that User is filled up at this point
    assert bot.user is not None
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.change_presence(activity=discord.CustomActivity("Site systems online."),status=discord.Status.online)

    try:
        sync = await bot.tree.sync()
        print(f"Syncing up {len(sync)} commands.")
    except Exception as e:
        print(e)

#def C_authorize(UserID:int,level:int):
    
    

@bot.tree.command(name="authorize",description="Authorize someone.")
@app_commands.describe(member="Select a member's authorization.")
async def authorization(interaction:discord.Interaction, member:discord.User,level:int):
    if not await check_access(interaction.user.id,2):
        await interaction.response.send_message(content=T_ACCES_DENIED,ephemeral=True)
        return
    if level > 7 or level < 0:
        interaction.response.send_message(content="Wrong access level.")
        return
    await interaction.response.send_message(content="**[ACCESS GRANTED]:** Changing authorization.",ephemeral=True)

   # C_authorize(member.id,level)

@bot.tree.command(name="set_status",description="Change the status of the site.")
@app_commands.describe(status="Write the status that should be given to the bot.")
async def set_status(interaction:discord.Interaction, status:str):
    if not check_access(interaction.user.id,2):
        await interaction.response.send_message(content=T_ACCES_DENIED,ephemeral=True)
        return
    await interaction.response.send_message(content="**[ACCESS GRANTED]:** Changing status.",ephemeral=True)
    await bot.change_presence(activity=discord.CustomActivity(status),status=discord.Status.online)

@bot.tree.command(name="intercom",description="Broadcast a message over the intercom.")
async def intercom(interaction:discord.Interaction):
    if not check_access(interaction.user.id,2):
        await interaction.response.send_message(content=T_ACCES_DENIED,ephemeral=True)
        return
    
    await interaction.response.send_modal(intercom_modal())

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