import discord
import asyncio
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

class Nick:
	def __init__(self, bot):
		self.bot = bot
	'''
	WIP AHHHH
	async def tzone(self, name):
		img_w, img_h = (1280, 900)
		img = await Image.open("twilightzone.png")
		font = await ImageFont.truetype("twilightzone.ttf", 200)
		draw = await ImageDraw.Draw(img)
		t_w, t_h = await draw.textsize(name, font)
		await draw.text(((img_w - t_w) / 2, (img_h - t_h) / 2), name, (192,192,192), font=font)
		await img.save("THE{}ZONE.png".format(name))
	'''

def setup(bot):
	bot.add_cog(Nick(bot))
	