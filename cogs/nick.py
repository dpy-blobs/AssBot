import asyncio
import random
import time
import functools
import xml.etree.ElementTree as et
from io import BytesIO
import aiohttp
import discord
from discord.ext import commands
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from bs4 import BeautifulSoup
from utils.checks import nsfw
from utils.connectors import fetch


class Nick:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["element"])
    async def atom(self, ctx, element):
        html = await fetch(ctx.session, f"http://www.chemicalelements.com/elements/{element}.html", 15, body='text')
        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text()

        element_name = text.split('Name: ')[1].split('\n')[0]
        element_symbol = text.split('Symbol: ')[1].split('\n')[0]
        atomic_number = text.split('Atomic Number: ')[1].split('\n')[0]
        atomic_mass = text.split('Atomic Mass: ')[1].split('\n')[0]
        neutrons = text.split('Number of Neutrons: ')[1].split('\n')[0]
        shells = text.split('Number of Energy Levels: ')[1].split('\n')[0]
        family = text.split('Classification: ')[1].split('\n')[0]
        color = text.split('Color: ')[1].split('\n')[0]
        uses = text.split('Uses: ')[1].split('\n')[0]
        discovery_year = text.split('Date of Discovery: ')[1].split('\n')[0]
        discoverer = text.split('Discoverer: ')[1].split('\n')[0]

        embed = discord.Embed(title=element_name, colour=0x33cc82, type="rich")
        embed.add_field(name='Name', value=element_name)
        embed.add_field(name='Symbol', value=element_symbol)
        embed.add_field(name='Atomic Number', value=atomic_number)
        embed.add_field(name='Atomic Mass', value=atomic_mass)
        embed.add_field(name='Neutrons', value=neutrons)
        embed.add_field(name='Shells', value=shells)
        embed.add_field(name='Family', value=family)
        embed.add_field(name='Color', value=color)
        embed.add_field(name='Uses', value=uses)
        embed.add_field(name='Year of Discovery', value=discovery_year)
        embed.add_field(name='Discoverer', value=discoverer)

        await ctx.send(embed=embed)

    @commands.command(aliases=["gh"])
    async def github(self, ctx):
        await ctx.send("https://github.com/dpy-blobs/AssBot")

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("https://discordapp.com/oauth2/authorize?client_id=254615108519460865&scope=bot")

    @commands.command(aliases=["8ball"])
    async def ask(self, ctx, *, question=None):
        '''Ask a question'''
        question = question.lower()

        if question.startswith("should"):
            responses = ("Yes", "No", "Definitely", "Sure", "Of course", "Maybe", 
                         "Probably" "Definitely not", "No way", "Please don't", 
                         "Go ahead!", "I mean, if you want to, sure", "Sure, but be careful", 
                         "That's probably not a good idea")
        elif question.startswith("where"):
            fast_food_chains = ("McDonald's", "Wendy's", "Burger King", "A&W", "KFC", "Taco Bell")
            responses = ("Just over there", "In your closet", "Probably hiding from you",
                         f"At the nearest {random.choice(fast_food_chains)}",
                         "Right behind you", "At the store", "Just a few blocks away",
                         "Nowhere near here")
        elif question.startswith("when"):
            time_units = ("years", "months", "days", "hours", "minutes", "seconds")
            responses = ("In a few hours", "Sometime this month", "When pigs fly",
                         "Not anythime soon, that's for sure", "By the end of the week",
                         "Let's hope that never happens", "I am genuinely unsure",
                         "Soon", "No idea, but be sure to tell me when it does",
                         "In a dog's age", "I don't know, but hopefully it's in my lifetime",
                         f"In {random.randint(1, 101)} {random.choice(time_units)}")
        elif question.startswith("who"):
            html = await fetch(ctx.session, "https://www.randomlists.com/random-celebrities?a", 15, body='text')
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all(class_="crux")
            celebrities = []
            for tag in tags:
                celebrities.append(tag.text)
            responses = celebrities
        elif question.startswith(("what movie should", "what film should")):
            html = await fetch(ctx.session, "https://www.randomlists.com/random-movies?a", 15, body='text')
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all(class_="support")
            movies = []
            for tag in tags:
                movies.append(tag.text)
            responses = movies
        elif question.startswith(("what game should", "what video game should", "what videogame should")):
            html = await fetch(ctx.session, "https://www.randomlists.com/random-video-games?a", 15, body='text')
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all(class_="support")
            games = []
            for tag in tags:
                games.append(tag.text)
            responses = games
        else:
            responses = ("Yes", "No", "Definitely", "Sure", "Of course", "Maybe", 
                         "Probably", "Most likely", "Definitely not", "No way",
                         "I hope not", "Better be", "I don't think so")

        if question is None:
            await ctx.send("You forgot to ask a question")
        else:
            await ctx.send(random.choice(responses))

    @commands.command()
    async def coinflip(self, ctx):
        '''Flips a coin'''
        responses = ["Heads", "Tails"]
        await ctx.send(random.choice(responses))

    @commands.command(aliases=["r34"])
    @nsfw()
    async def rule34(self, ctx, *tags):
        """Gets NSFW photos from rule 34"""
        embed = discord.Embed(title="Rule 34", colour=0x9B59B6, type="rich")
        if len(tags) == 0:
            while True:
                r34_post = await self.r34_random(ctx)
                embed.set_image(url=r34_post["url"])

                msg = await ctx.send(embed=embed)

                def check(reaction, user):
                    return (user.id != self.bot.user.id
                            and reaction.message.id == msg.id)

                await msg.add_reaction("🔄")
                await msg.add_reaction("🚫")

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)
                except asyncio.TimeoutError:
                    return await msg.delete()

                await msg.delete()
                if str(reaction) == "🔄":
                    continue
                if str(reaction) == "🚫":
                    return

        else:
            r34_posts = await self.r34_search(ctx, *tags)

            if len(r34_posts) == 0:
                await ctx.send("I was unable to find a post with those tags")
                return
            else:
                index = 0
                while True:
                    embed.set_image(url=r34_posts[index]["url"])
                    embed.set_footer(text="({}/{})".format(index + 1, str(len(r34_posts))))

                    msg = await ctx.send(embed=embed)
                    # Thanks for the repetition Nick.
                    def check(reaction, user):
                        return (user.id != self.bot.user.id
                                and reaction.message.id == msg.id)

                    await msg.add_reaction("◀")
                    await msg.add_reaction("▶")
                    await msg.add_reaction("🚫")

                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)
                    except asyncio.TimeoutError:
                        return await msg.delete()

                    await msg.delete()
                    if str(reaction) == "◀" and index > 0:
                        index -= 1
                    if str(reaction) == "▶" and index < len(r34_posts) - 1:
                        index += 1
                    if str(reaction) == "🚫":
                        return

    @commands.command(aliases=["twilightzone"])
    async def tzone(self, ctx, content: str):
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

    async def r34_search(self, ctx, *tags):  # Returns a list of dictionaries {"URL", "SCORE"} (rule34_posts)
        base = "http://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={}".format("+".join(tags))

        try:
            data = await fetch(ctx.session, base, 15, body='text')
        except:
            return await ctx.send('There was an error with your request. Please try again later.')

        _posts = et.fromstring(data)
        posts = []
        for post in _posts:
            post = {"url": post.attrib["file_url"], "score": int(post.attrib["score"])}
            if ".webm" in post["url"]:
                continue
            posts.append(post)
        sorted_posts = sorted(posts, key=lambda post: post["score"], reverse=True)
        return sorted_posts

    async def r34_random(self, ctx):
        while True:
            page_id = str(random.randint(0, 2372222))
            try:
                data = await fetch(ctx.session,
                                        "http://rule34.xxx/index.php?page=dapi&s=post&q=index&id={}".format(page_id),
                                        body='text')
            except:
                return await ctx.send('There was an error with your request. Please try again.')

            posts = et.fromstring(data)
            if len(posts) == 0:
                continue
            else:
                for post in posts:
                    post = {"url": post.attrib["file_url"], "score": int(post.attrib["score"])}
                    if ".webm" in post["url"]:
                        continue
            return post

    def _tzone(self, ctx, content: str):
        content = content.upper()
        img = Image.open("cogs/resources/nick/twilightzone.png")
        img_w, img_h = (1280, 900)

        font = ImageFont.truetype("cogs/resources/nick/twilightzone.ttf", 200)
        draw = ImageDraw.Draw(img)
        t_w, t_h = draw.textsize(content, font)
        draw.text(((img_w - t_w) / 2, (img_h - t_h) / 2), content, (192, 192, 192), font=font)

        bytesio = BytesIO()
        img.save(bytesio, "png")
        bytesio.seek(0)

        return bytesio


def setup(bot):
    bot.add_cog(Nick(bot))

