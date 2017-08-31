# import discord
from discord.ext import commands


class CuteListeners:
    raise NotImplementedError


class MystRandomThings:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='binary', aliases=['b1nary', '0101'])
    async def binary_decrpyt(self, ctx, *, inp: str):

        inp = inp.replace(' ', '')

        try:
            out = ''.join(chr(int(inp[i * 8:i * 8 + 8], 2)) for i in range(len(inp) // 8))
        except:
            return await ctx.send('**This is not binary!**')

        return await ctx.send(out)


class MystSimpleTunesPlayer:
    raise NotImplementedError


class MystSimpleTunes:
    raise NotImplementedError


class MystMain:
    raise NotImplementedError


class MystHandlers:
    raise NotImplementedError


def setup(bot):
    bot.add_cog(MystRandomThings(bot))
