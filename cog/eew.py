# Tuna - EEW

import discord
from discord.ext import commands, tasks

from aiofiles import open as async_open
from aiohttp import ClientSession
from ujson import load, dumps
from os.path import exists
from time import time


class EEW(commands.Cog):
    def __init__(self, bot):
        self.bot, self.tuna = bot, bot.data
        self.JSON_PATH = "data/eew.json"
        if exists(self.JSON_PATH):
            with open(self.JSON_PATH, "r") as f:
                self.data = load(f)
        else:
            with open(self.JSON_PATH, "w") as f:
                f.write('{"before": 0}')
            self.data = {}
        if self.data["before"] == 0:
            self.data["before"] = time()
        self.eew_send.start()

    @commands.command()
    async def eew(self, ctx):
        self.data[str(ctx.channel.id)] = False if self.data.get(str(ctx.channel.id), False) else True
        async with async_open(self.JSON_PATH, "w") as f:
            await f.write(dumps(self.data, indent=4))
        await ctx.send("Ok")

    @tasks.loop(seconds=3)
    async def eew_send(self):
        async with ClientSession() as session:
            async with session.get("https://api.iedred7584.com/eew/json") as r:
               data = await r.json()
        if data["ParseStatus"] != "Error":
            for channel_id in self.data:
                if channel_id == "before":
                    if data["OriginTime"]["UnixTime"] > self.data["before"]:
                        self.data["before"] = data["OriginTime"]["UnixTime"]
                        embed = discord.Embed(
                            title=data["Title"]["String"],
                            description=data["Title"]["Detail"]
                        )
                        embed.add_field(name="Place", value=data["Hypocenter"]["Name"])
                        embed.add_field(name="MaxIntensity", value=data["MaxIntensity"]["String"])
                        embed.add_field(name="OriginTime", value=data["OriginTime"]["String"])
                    else:
                        break
                else:
                    channel = self.bot.get_channel(int(channel_id))
                    if not channel:
                        continue
                    await channel.send(embed=embed)

    def cog_unload(self):
        self.eew_send.cancel()


def setup(bot):
    bot.add_cog(EEW(bot))
