import asyncio

from discord.ext import commands

class Luna:
    """Gay commands"""
    def _init__(self, bot):
        self.bot = bot

    @commands.command()
    async def blink(self, ctx, *, text: str):
        """Blink text every 2 seconds."""
        m = await ctx.send(text)
        for i in range(10):
            if i % 2 == 0:
                await m.edit(content=f'**{text}**')
            else:
                await m.edit(content=text)

            await asyncio.sleep(2)

def setup(bot):
    bot.add_cog(Luna(bot))
