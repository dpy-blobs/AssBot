import discord
from discord.ext.commands import Bot
from discord.ext import commands
import aiohttp
import asyncio
import random
import xml.etree.ElementTree as ET

class Rule34():
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def rule34(self, ctx, *tags):
        embed = discord.Embed(title="Rule 34", colour=0x9B59B6, type="rich")
        if len(tags) == 0:
            while True:
                result = await self.random()
                embed.set_image(url=result["url"])
                result_message = await self.bot.send_message(ctx.message.channel, embed=embed)
                await self.bot.add_reroll_controls(result_message)
                awaited_reaction = await self.bot.wait_for_reaction(emoji=["\U0001f504", "\U0001F6AB"], message=result_message, timeout=15)
                if awaited_reaction is not None:
                    await self.bot.delete_message(result_message)
                    if awaited_reaction.reaction.emoji == "\U0001F6AB":
                        return
                else:
                    await self.bot.clear_reactions(result_message)
                    return
        else:
            results = await self.search(*tags)
            if len(results) == 0:
                await self.bot.say("I was unable to find a post with those tags")
                return
            results_pos = 0
            while True:
                embed.set_image(url=results[results_pos]["url"])
                embed.set_footer(text="({}/{})".format(results_pos + 1, str(len(results))))
                result_message = await self.bot.send_message(ctx.message.channel, embed=embed)
                await self.bot.add_content_controls(result_message)
                awaited_reaction = await self.bot.wait_for_reaction(emoji=["\U000025c0", "\U000025b6", "\U0001F6AB"], message=result_message, timeout=15)
                if awaited_reaction is not None:
                    if awaited_reaction.reaction.emoji == "\U000025c0" and results_pos > 0:
                        results_pos -= 1
                    if awaited_reaction.reaction.emoji == "\U000025b6" and results_pos < len(results) - 1:
                        results_pos += 1
                    await self.bot.delete_message(result_message)
                    if awaited_reaction.reaction.emoji == "\U0001F6AB":
                        return
                else:
                    await self.bot.clear_reactions(result_message)
                    embed.set_footer(discord.Embed.Empty)
                    return

    async def search(self, *tags): #Returns a list of dictionaries {"URL", "SCORE"} (rule34_posts)
        search_url = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}".format("+".join(tags))
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url) as resp:
                xml = ET.fromstring(await resp.text())
                posts = []
                for post in xml:
                    post = {"url": post.attrib["file_url"], "score": int(post.attrib["score"])}
                    if ".webm" in post["url"]:
                        continue
                    posts.append(post)
                sorted_posts = sorted(posts, key=lambda post: post["score"], reverse=True)
        return sorted_posts
    
    async def random(self):
        while True:
            page_id = str(random.randint(0,2372222))
            async with aiohttp.ClientSession() as session:
                async with session.get("http://rule34.xxx/index.php?page=dapi&s=post&q=index&id={}".format(page_id)) as resp:
                    xml = ET.fromstring(await resp.text())
                    for post in xml:
                        post = {"url": post.attrib["file_url"], "score": int(post.attrib["score"])}
                        if ".webm" in post["url"]:
                            continue
                    return post

def setup(bot):
    bot.add_cog(Rule34(bot))