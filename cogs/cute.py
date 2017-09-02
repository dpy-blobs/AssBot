import discord
from discord.ext import commands
import math
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO

class Cute:
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def quilt(self, ctx, *mems : discord.Member):
        if len(mems) == 0:
            mems = [ctx.author]
        avys = []
        for mem in mems:
            async with ctx.session.get(mem.avatar_url_as(format='png', size=512)) as r:
                avys.append(BytesIO(await r.read()))
        file = await self.bot.loop.run_in_executor(None, self._quilt, avys)
        await ctx.send(file=file)
    def _quilt(self, avys):
        xbound = math.ceil(math.sqrt(len(avys)))
        ybound = math.ceil(len(avys)/xbound)
        size = int(2520/xbound)
        base = Image.new(mode='RGBA', size=(xbound * size, ybound * size), color=(0, 0, 0, 0))
        x, y = 0, 0
        for avy in avys:
            im = Image.open(avy)
            base.paste(im.resize((size, size), resample=Image.BILINEAR), box=(x * size, y * size))
            if x < xbound - 1:
                x += 1
            else:
                x = 0
                y += 1
        buffer = BytesIO()
        base.save(buffer, 'png')
        buffer.seek(0)
        return discord.File(buffer, filename='quilt.png')

def setup(bot):
    bot.add_cog(Cute(bot))