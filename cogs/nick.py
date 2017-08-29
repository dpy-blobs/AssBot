import discord
from discord.ext import commands
import asyncio
import os
import time
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Nick:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def tzone(self, name):
		'''You unlock this door with the key of imagination'''
		name = name.upper()
		img_w, img_h = (1280, 900)
		img = Image.open("cog_resources/nick/twilightzone.png")
		font = ImageFont.truetype("cog_resources/nick/twilightzone.ttf", 200)
		draw = ImageDraw.Draw(img)
		t_w, t_h = draw.textsize(name, font)
		draw.text(((img_w - t_w) / 2, (img_h - t_h) / 2), name, (192,192,192), font=font)
		bytesio = BytesIO()
		img.save(bytesio, "png")
		bytesio.seek(0)
		await self.bot.upload(fp=image, filename="{}.png".format(name))
	
	@commands.command()
	async def ping(self, ctx):
        before = time.perf_counter()
        msg = await ctx.send('...')
        after = time.perf_counter()
        rtt = (after - before) * 1000
        ws = self.bot.latency * 1000

        await msg.edit(content=f'Pong! \n RTT - {rtt:.3f}ms \n WS - {ws:.3f}ms')

def setup(bot):
	bot.add_cog(Nick(bot))
	