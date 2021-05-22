# TunaBot Ext - Help

import discord
from discord.ext import commands

from aiofile import async_open
from json import load, dumps


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot, self.tuna = bot, bot.data
        with open("data/help.json", "r") as f:
            self.data = load(f)

    @commands.command()
    async def help(self, ctx, *, cmd=None):
        title, description = None, None
        if cmd:
            key = []
            for category in self.data:
                 if cmd == category:
                     key.append(category)
                     break
                 for c in self.data[category]:
                     if c == cmd:
                         key.append(c)
                         break
            if len(key) == 2:
                title = f"{cmd}のHELP"
                description = self.data[key[0]][key[1]]
            elif len(key) == 1:
                title = f"{cmd}のHELP"
                description = "\n".join(f"`{key}`" for key in self.data[category])
            else:
                title, description = "HELP", "見つかりませんでした。"
        else:
            title, description = "HELP", "\n".join(f"`{key}`" for key in self.data)
        await ctx.reply(embed=discord.Embed(title=title, description=description))


def setup(bot):
    bot.add_cog(Help(bot))
