import random

from discord.ext import commands

class Synder:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["c"])
    async def choose(self, ctx, *, choices):
        f"""
        Chooses between a number of options
        Syntax = {ctx.prefix}choose option 1 | option 2 | option 3 | option 4
        """
        parsed_choices = [choice.strip() for choice in choices.split("|")]
        await ctx.send(random.choice(parsed_choices))

def setup(bot):
    bot.add_cog(Synder(bot))
