from discord.ext import commands
import asyncio, discord, io, textwrap, traceback
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

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    code = textwrap.indent(body, '  ')
    to_compile = f'async def func():\n{code}'

    try:
        exec(to_compile, env)
    except SyntaxError as e:
        return await ctx.send(get_syntax_error(e))

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'​`​`​`py\n{value}{traceback.format_exc()}\n​`​`​`')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            bot._last_result = ret
            await ctx.send(f'```py\n{value}{ret}\n```')
async def on_ready():
    print("yes")
bot.loop.create_task(cyc())
bot.run("MjU0NjE1MTA4NTE5NDYwODY1.DIWGmw.BDtt1fYwK0Bx5U0BAwmqdSYZ9aA")
