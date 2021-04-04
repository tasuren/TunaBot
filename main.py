# Discord bot TunaBot v2 by tasuren

import discord
from discord.ext import commands

from os import listdir


print("Now loading...")


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="t!", intents=intents)


# エクステンションのロードをする。
bot.load_extension("jishaku")
## cogフォルダにあるものを全て読み込む。
for filename in listdir:
    if not filename.startswith("_"):
        bot.load_extension(f"cog.{filename[:-3]}")


# 起動確認用にメッセージを表示する。
@bot.event
async def on_ready():
    print("Connected")


bot.run("ODE5MTIwNTc1MTgwMDQ2MzU4.YEh_ew.mmlJCSJllvaEfWcmwKdX2eQiiUs")
