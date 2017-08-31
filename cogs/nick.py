import discord
from discord.ext import commands
import asyncio
import os
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import functools
import time

class Nick:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tzone(self, ctx, content:str):
        '''You unlock this door with the key of imagination'''
        x = functools.partial(self._tzone, ctx, content)
        tzone_image = await self.bot.loop.run_in_executor(None, x)

        await ctx.send(file=discord.File(tzone_image, filename="{}.png".format(content)))

    @commands.command()
    async def ping(self, ctx):
        '''Displays ping'''
        before = time.perf_counter()
        msg = await ctx.send('...')
        after = time.perf_counter()
        rtt = (after - before) * 1000
        ws = self.bot.latency * 1000
 
        await msg.edit(content=f'RTT - **{rtt:.3f}ms**\nWS - **{ws:.3f}ms**')

    def _tzone(self, ctx, content:str):
        content = content.upper()
        img = Image.open("cog_resources/nick/twilightzone.png")
        img_w, img_h = (1280, 900)

        font = ImageFont.truetype("cog_resources/nick/twilightzone.ttf", 200)
        draw = ImageDraw.Draw(img)
        t_w, t_h = draw.textsize(content, font)
        draw.text(((img_w - t_w) / 2, (img_h - t_h) / 2), content, (192,192,192), font=font)

        bytesio = BytesIO()
        img.save(bytesio, "png")
        bytesio.seek(0)

        return bytesio

def setup(bot):
    bot.add_cog(Nick(bot))
	
