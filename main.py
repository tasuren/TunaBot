# Discord bot TunaBot v2 by tasuren

import discord
from discord.ext import commands

from os import listdir
from ujson import load


print("Now loading...")


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="t!", intents=intents)
with open("data.json", "r") as f:
    bot.data = load(f)


# エクステンションのロードをする。
bot.load_extension("jishaku")
## cogフォルダにあるものを全て読み込む。
for filename in listdir("cog"):
    if not filename.startswith("_") and filename.endswith(".py"):
        bot.load_extension(f"cog.{filename[:-3]}")


# 起動確認用にメッセージを表示する。
@bot.event
async def on_ready():
    print("Connected")


bot.run(bot.data["token"])
