import discord
from discord.ext import commands
import asyncio
import os
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import functools

class Nick:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tzone(self, ctx, name:str):
        '''You unlock this door with the key of imagination'''
        x = functools.partial(self._tzone, ctx, name)
        tzone_image = await bot.loop.run_in_executor(None, x)

        await ctx.send(file=discord.File(tzone_image, filename="{}.png".format(name)))

    def _tzone(self, ctx, name:str):
        name = name.upper()
        img = Image.open("cog_resources/nick/twilightzone.png")
        img_w, img_h = (1280, 900)

        font = ImageFont.truetype("cog_resources/nick/twilightzone.ttf", 200)
        draw = ImageDraw.Draw(img)
        t_w, t_h = draw.textsize(name, font)
        draw.text(((img_w - t_w) / 2, (img_h - t_h) / 2), name, (192,192,192), font=font)

        bytesio = BytesIO()
        img.save(bytesio, "png")
        bytesio.seek(0)

        return bytesio

def setup(bot):
    bot.add_cog(Nick(bot))
	
