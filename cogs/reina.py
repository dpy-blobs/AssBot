import io
import inspect
import textwrap
import functools

import psutil
import discord
from discord.ext import commands
import youtube_dl


class SourceEntity(commands.Converter):
    async def convert(self, ctx, arg):
        cmd = ctx.bot.get_command(arg)
        if cmd is not None:
            return cmd.callback

        cog = ctx.bot.get_cog(arg)
        if cog is not None:
            return cog.__class__

        module = ctx.bot.extensions.get(arg)
        if module is not None:
            return module

        raise commands.BadArgument(f'{arg} is neither a command, a cog, nor an extension.')


class Reina:
    def __init__(self):
        self.process = psutil.Process()
        opts = {
            'quiet': True,
        }
        self.ytdl = youtube_dl.YoutubeDL(opts)

    @commands.command(aliases=['yt'])
    async def youtube(self, ctx, *, query: str):
        """Searches YouTube and gives you the first result."""

        func = functools.partial(self.ytdl.extract_info, f'ytsearch:{query}', download=False)
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
    async def source(self, ctx, *, entity: SourceEntity):
        """Posts the source code of a command, cog or extension."""
        code = inspect.getsource(entity)
        code = textwrap.dedent(code).replace('`', '\u200b`')

        if len(code) > 1990:
            name = entity.__name__
            gist = await ctx.bot.create_gist(f'Source for {name}', [(f'{name}.py', code)])
            return await ctx.send(f'**Your requested sauce was too stronk. So I uploaded to gist!**\n<{gist}>')

        return await ctx.send(f'```py\n{code}\n```')

    @source.error
    async def source_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(error)


def setup(bot):
    bot.add_cog(Reina())
