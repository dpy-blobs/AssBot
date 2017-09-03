import io
import inspect
import textwrap
import functools

import psutil
import discord
from discord.ext import commands
import youtube_dl


class Reina:
    def __init__(self):
        self.process = psutil.Process()
        opts = {
            'default_search': 'auto',
            'quiet': True
        }
        self.ytdl = youtube_dl.YoutubeDL(opts)

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, query: str):
        """Searches YouTube and gives you the first result."""

        func = functools.partial(self.ytdl.extract_info, query, download=False)
        try:
            info = await ctx.bot.loop.run_in_executor(None, func)
        except youtube_dl.DownloadError:
            await ctx.send('Video not found.')
        else:
            if 'entries' in info:
                info = info['entries'][0]
            await ctx.send(info.get('webpage_url'))

    @commands.command()
    async def uptime(self, ctx):
        """Shows the bot's uptime."""

        await ctx.send(f'Uptime: **{ctx.bot.uptime}**')

    @commands.command()
    async def memory(self, ctx):
        """Shows the bot's memory usage."""

        memory_usage = self.process.memory_full_info().uss / 1024**2
        await ctx.send(f'Memory Usage: **{memory_usage:.2f} MiB**')

    @commands.command()
    async def cpu(self, ctx):
        """Shows the bot's cpu usage."""

        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        await ctx.send(f'CPU Usage: **{cpu_usage}%**')

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member=None):
        """Posts a member's avatar."""

        member = member or ctx.author
        avatar_url = member.avatar_url_as(static_format='png')

        async with ctx.session.get(avatar_url) as r:
            if r.status != 200:
                return await ctx.send('Failed to download avatar.')

            filetype = r.headers.get('Content-Type').split('/')[1]
            filename = f'{member.name}.{filetype}'
            await ctx.send(file=discord.File(io.BytesIO(await r.read()),
                                             filename))

    @commands.command()
    async def source(self, ctx, *, command: str):
        """Posts the source code of a command or cog."""

        cmd = ctx.bot.get_command(command)
        if cmd is not None:
            code = inspect.getsource(cmd.callback)
            code = textwrap.dedent(code).replace('`', '\u200b​`')
        else:
            cog = ctx.bot.get_cog(command)
            if cog is None:
                return await ctx.send('I could not find this command or cog.')
            code = inspect.getsource(cog.__class__)
            code = textwrap.dedent(code).replace('`', '\u200b​`')

        if len(code) > 1990:
            gist = await ctx.bot.create_gist(f'Source for {command}', [(f'{command}.py', code)])
            return awaitc ctx.send(f'**Your requested sauce was too stronk. So I uploaded to gist!**\n<{gist}>')

        return await ctx.send(f'```py\n{code}\n```')


def setup(bot):
    bot.add_cog(Reina())
