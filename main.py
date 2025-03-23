import discord
from discord.ext import commands
from discord.ext import tasks
from discord import app_commands
import json
import requests

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

from colorama import init
from colorama import Fore, Back, Style
init()

try:
    file = open("config.json","r")
    config = json.loads(file.read())
except FileNotFoundError:
    print (f"{Back.RED}{Style.BRIGHT}[error]{Style.RESET_ALL} no config file pls make one")
    exit()

token = config["token"]
url = config["url"]
host = config["host"]

bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")

@bot.command(aliases=["mm", "nm", "np", "nowplaying", "music"])
async def now(ctx):
    r = requests.get(url)
    rj = r.json()

    embed=discord.Embed(title="listening to")
    embed.set_thumbnail(url=rj['covers']['extra_large'])
    embed.add_field(name=rj['track'], value=f"by {rj['artist']} on {rj['album']}", inline=False)
    embed.set_footer(text=rj['timestamp'])
    await ctx.send(embed = embed)

@bot.event
async def on_ready():
    print (f"{Back.GREEN}{Style.BRIGHT}[ready]{Style.RESET_ALL} authorised as {bot.user}")

bot.run(token)