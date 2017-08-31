import io
import inspect
import textwrap

import psutil
import discord
from discord.ext import commands


class Reina:
    def __init__(self):
        self.process = psutil.Process()

    @commands.command()
    async def uptime(self, ctx):
        """Shows the bot's uptime."""

        await ctx.send(f'Uptime: **{ctx.bot.uptime}**.

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
        """Posts the source code of a command."""

        cmd = ctx.bot.get_command(command)
        if cmd is None:
            return await ctx.send(f'Command {command} not found.')

        code = inspect.getsource(cmd.callback)
        code = textwrap.dedent(code).replace('`', '\u200b​`')

        p = commands.Paginator(prefix='```py')
        for line in code.split('\n'):
            p.add_line(line)

        for page in p.pages:
            await ctx.send(page)


def setup(bot):
    bot.add_cog(Reina())
