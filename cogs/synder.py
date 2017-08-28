import random

from discord.ext import commands

class Synder:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["c"])
    async def choose(self, ctx, *, choices):
        """Chooses between a number of options

        Seperate choices with "|" to denote seperate options.
        """
        parsed_choices = [choice.strip() for choice in choices.split("|")]
        await ctx.send(random.choice(parsed_choices))

def setup(bot):
    bot.add_cog(Synder(bot))
