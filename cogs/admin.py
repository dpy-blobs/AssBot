import os
import json
import threading
import asyncio

import discord
from discord.ext import commands


class Admin:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        role = discord.utils.get(ctx.guild.roles, id=352849291733237771)
        return role in ctx.author.roles

    @commands.command()
    async def setavatar(self, ctx, link: str):
        """Sets the bot's avatar."""

        async with ctx.session.get(link) as r:
            if r.status == 200:
                try:
                    await ctx.bot.user.edit(avatar=await r.read())
                except Exception as e:
                    await ctx.send(e)
                else:
                    await ctx.send('Avatar set.')
            else:
                await ctx.send('Unable to download image.')

    @commands.command()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        module = f'cogs.{module}'
        try:
            ctx.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    async def reload(self, ctx, *, module: str):
        """Reloads a module."""
        module = f'cogs.{module}'
        try:
            ctx.bot.unload_extension(module)
            ctx.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        module = f'cogs.{module}'
        try:
            ctx.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    async def gitmerge(self, ctx, *pr_numbers):
        gh_token = os.environ['GH_TOKEN']

        success = []
        failure = []

        data = {'commit_title': f'Merged by {ctx.author}',
                'commit_message': 'Merged from command'}

        headers = {'Content-Type': 'application/json',
                   'Authorization': f"token {gh_token}"}

        for pr in pr_numbers:
            url = f'https://api.github.com/repos/dpy-blobs/AssBot/pulls/{pr}/merge'

            async with ctx.session.put(url, data=json.dumps(data), headers=headers) as resp:
                if resp.status == 200:
                    success.append(pr)
                else:
                    body = await resp.json()
                    failure.append(f"PR #{pr} | Merge Unsuccessful\nMessage: {body["message"]}\nStatus: {resp.status}")
            await asyncio.sleep(5)

        sjoin = ', '.join(success)
        fjoin = '\n'.join(failure)

        if failure and success:
            return await ctx.send(f"PR #(s) **{sjoin}** | Successfully Merged.\n{fjoin}")
        if not failure and success:
            return await ctx.send(f'PR #(s) **{sjoin}** | Successfully Merged.')
        else:
            await ctx.send(fjoin)

    @commands.command(name='threads', hidden=True)
    async def thread_counter(self, ctx):
        await ctx.send(len(threading.enumerate()))

    @commands.command()
    async def cleanup(self, ctx, limit: int = 100):
        """Cleans up the bot's messages."""

        prefixes = tuple(ctx.bot.command_prefix(ctx.bot, ctx.message))

        def check(m):
            return m.author == ctx.me or m.content.startswith(prefixes)

        deleted = await ctx.purge(limit=limit, check=check)
        await ctx.send(f'Cleaned up {len(deleted)} messages.')


def setup(bot):
    bot.add_cog(Admin(bot))
