import asyncio
import random
import time
import functools
import xml.etree as et
from io import BytesIO
import aiohttp
import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


class Nick:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(alisases=["r34"])
    async def rule34(self, ctx, *tags):
        embed = discord.Embed(title="Rule 34", colour=0x9B59B6, type="rich")
        if len(tags) == 0:
            while True:
                r34_post = await self.r34_random()
                embed.set_image(url=r34_post["url"])

                msg = await ctx.send(embed=embed)

                await msg.add_reaction("🔄")
                await msg.add_reaction("🚫")

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=15)
                except asyncio.TimeoutError:
                    await msg.clear_reactions()
                    return

                if str(reaction) == "🔄":
                    await msg.delete()
                    continue
                if str(reaction) == "🚫":
                    await msg.delete()
                    return

        else:
            r34_posts = await self.r34_search(*tags)

            if len(results) == 0:
                await self.bot.say("I was unable to find a post with those tags")
                return
            else:
                index = 0
                while True:
                    embed.set_image(url=r34_posts[index]["url"])
                    embed.set_footer(text="({}/{})".format(index + 1, str(len(r34_posts))))

                    msg = await ctx.send(embed=embed)

                    await msg.add_reaction("◀")
                    await msg.add_reaction("▶")
                    await msg.add_reaction("🚫")
                    
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=15)
                    except asyncio.TimeoutError:
                        await msg.clear_reactions()
                        embed.set_footer(discord.Embed.Empty)
                        return

                    if str(reaction) == "◀" and index > 0:
                        index -= 1
                    if str(reaction) == "▶" and index < len(r34_posts) - 1:
                        index += 1
                    if str(reaction) == "🚫":
                        await msg.delete()
                        return
                    

    @commands.command(aliases=["twilightzone"])
    async def tzone(self, ctx, content:str):
        """You unlock this door with the key of imagination"""
        x = functools.partial(self._tzone, ctx, content)
        tzone_image = await self.bot.loop.run_in_executor(None, x)

        await ctx.send(file=discord.File(tzone_image, filename="{}.png".format(content)))

    @commands.command()
    async def ping(self, ctx):
        """Displays ping"""
        before = time.perf_counter()
        msg = await ctx.send('...')
        after = time.perf_counter()
        rtt = (after - before) * 1000
        ws = self.bot.latency * 1000
 
        await msg.edit(content=f'RTT - **{rtt:.3f}ms**\nWS - **{ws:.3f}ms**')

    def _tzone(self, ctx, content:str):
        content = content.upper()
        img = Image.open("cogs/resources/nick/twilightzone.png")
        img_w, img_h = (1280, 900)

        font = ImageFont.truetype("cogs/resources/nick/twilightzone.ttf", 200)
        draw = ImageDraw.Draw(img)
        t_w, t_h = draw.textsize(content, font)
        draw.text(((img_w - t_w) / 2, (img_h - t_h) / 2), content, (192,192,192), font=font)

        bytesio = BytesIO()
        img.save(bytesio, "png")
        bytesio.seek(0)

        return bytesio
    
    async def r34_search(self, *tags): #Returns a list of dictionaries {"URL", "SCORE"} (rule34_posts)
        search_url = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}".format("+".join(tags))
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as resp:
                xml = et.fromstring(await resp.text())
                posts = []
                for post in xml:
                    post = {"url": post.attrib["file_url"], "score": int(post.attrib["score"])}
                    if ".webm" in post["url"]:
                        continue
                    posts.append(post)
                sorted_posts = sorted(posts, key=lambda post: post["score"], reverse=True)
        return sorted_posts
    
    async def r34_random(self):
        while True:
            page_id = str(random.randint(0,2372222))
            async with aiohttp.ClientSession() as session:
                async with session.get("http://rule34.xxx/index.php?page=dapi&s=post&q=index&id={}".format(page_id)) as resp:
                    xml = et.fromstring(await resp.text())
                    for post in xml:
                        post = {"url": post.attrib["file_url"], "score": int(post.attrib["score"])}
                        if ".webm" in post["url"]:
                            continue
                    return post


def setup(bot):
    bot.add_cog(Nick(bot))

