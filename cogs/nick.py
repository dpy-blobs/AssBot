import discord
from discord.ext import commands
import asyncio
import os
from io import BytesIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Nick:

	nick_resources = os.path.join(os.pardir, "cog_resources/nick")

	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def tzone(self, name):
		img_w, img_h = (1280, 900)
		img = Image.open(os.path.join(self.nick_resources, "twilightzone.png"))
		font = ImageFont.truetype(os.path.join(self.nick_resources, "twilightzone.ttf"), 200)
		draw = ImageDraw.Draw(img)
		t_w, t_h = draw.textsize(name, font)
		draw.text(((img_w - t_w) / 2, (img_h - t_h) / 2), name, (192,192,192), font=font)
		bytesio = BytesIO()
		img.save(bytesio, "png")
		bytesio.seek(0)
		await self.bot.upload(fp=image, filename="{}.png".format(name))

def setup(bot):
	bot.add_cog(Nick(bot))
	