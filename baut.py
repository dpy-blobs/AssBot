<<<<<<< HEAD
import io
import textwrap
import traceback
import asyncio
import discord
from discord.ext import commands
from itertools import cycle
from contextlib import redirect_stdout

bot = commands.Bot(command_prefix=lambda b,m: m.author.name[0], game=discord.Game(name="yes"))
bot._last_result = None

async def cyc():
    await bot.wait_until_ready()
    guild = bot.get_guild(328873861481365514)
    for member in cycle(guild.members):
        await guild.me.edit(nick=member.name.upper())
        await asyncio.sleep(5)

def cleanup_code(content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

def get_syntax_error(e):
    if e.text is None:
        return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

@bot.command(name='eval')
async def _eval(ctx, *, body: str):
    """Evaluates code."""
    env = {
        'bot': ctx.bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': bot._last_result
    }
=======
import asyncio
from pathlib import Path
from itertools import cycle
>>>>>>> 82031d9c1d50e25bc2568fd41f81ae99d68b0156

import aiohttp
import discord
from discord.ext import commands


class Context(commands.Context):
    @property
    def session(self):
        return self.bot.session


class Bot(commands.Bot):
    def __init__(self):
        def get_prefix(bot, message):
            return message.author.name[0]

        super().__init__(command_prefix=get_prefix,
                         game=discord.Game(name="yes"))

        self.session = aiohttp.ClientSession(loop=self.loop)

        startup_extensions = [x.stem for x in Path('cogs').glob('*.py')]
        for extension in startup_extensions:
            try:
                self.load_extension(f'cogs.{extension}')
            except Exception as e:
                error = f'{extension}\n {type(e).__name__}: {e}'
                print(f'Failed to load extension {error}')

        self.loop.create_task(cyc())

    def _do_cleanup(self):
        self.session.close()
        super()._do_cleanup()

    async def on_ready(self):
        print(f'Logged in as {self.user}')
        print('-------------')

    async def on_message(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.prefix is not None:
            ctx.command = self.all_commands.get(ctx.invoked_with.lower())
            await self.invoke(ctx)

    async def cyc(self):
        await self.wait_until_ready()
        guild = self.get_guild(328873861481365514)
        for member in cycle(guild.members):
            await guild.me.edit(nick=member.name.upper())
            await asyncio.sleep(5)


<<<<<<< HEAD
        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            bot._last_result = ret
            await ctx.send(f'```py\n{value}{ret}\n```')

@bot.event
async def on_ready():
    print("yes")

bot.loop.create_task(cyc())
bot.run("MjU0NjE1MTA4NTE5NDYwODY1.DIWGmw.BDtt1fYwK0Bx5U0BAwmqdSYZ9aA")
=======
if __name__ == '__main__':
    bot = Bot()
    bot.run("MjU0NjE1MTA4NTE5NDYwODY1.DIWGmw.BDtt1fYwK0Bx5U0BAwmqdSYZ9aA")
>>>>>>> 82031d9c1d50e25bc2568fd41f81ae99d68b0156
