import random

from discord.ext import commands


class Synder:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pick", "c"])
    async def choose(self, ctx, *, choices):
        """Chooses between a number of options

        Seperate choices with "|" to denote seperate options.
        """
        parsed_choices = [choice.strip() for choice in choices.split("|")]

        if len(parsed_choices) < 1:
            await ctx.send("You need to give me things to choose from")
        elif len(parsed_choices) == 1:
            await ctx.send("ಠ╭╮ಠ")
        else:
            await ctx.send(random.choice(parsed_choices))


def setup(bot):
    bot.add_cog(Synder(bot))
