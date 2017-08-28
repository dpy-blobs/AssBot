from discord.ext import commands
import asyncio, discord
from itertools import cycle
bot = commands.Bot(command_prefix=lambda b,m: m.author.name[0], game=discord.Game(name="yes"))
async def cyc():
    await bot.wait_until_ready()
    guild = bot.get_guild(328873861481365514)
    for member in cycle(guild.members):
        await guild.me.edit(nick=member.name.upper())
        await asyncio.sleep(5)
@bot.command()
async def evul(ctx, code):
    await ctx.send(eval(code))
bot.loop.create_task(cyc())
bot.run("MjU0NjE1MTA4NTE5NDYwODY1.DIWGmw.BDtt1fYwK0Bx5U0BAwmqdSYZ9aA")
