import io
import textwrap
import traceback
import asyncio
import discord
from discord.ext import commands
from itertools import cycle
from contextlib import redirect_stdout


class Admin:
    def __init__(self, bot):
        self.bot = bot
        self.bot._last_result = None

    async def __local_check(self, ctx):
        return ctx.author in self.bot.blob_guild.members

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

    def cleanup_code(self, content):
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return f'```py\n{e.__class__.__name__}: {e}\n```'
        return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'


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
    
    @commands.command(name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates code."""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self.bot._last_result,
            'kkk': 'Racist!'
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        code = textwrap.indent(body, '  ')
        to_compile = f'async def func():\n{code}'

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            return await ctx.send(self.get_syntax_error(e))

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('🍡')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self.bot._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command()
 	async def gitmerge(self, ctx, pr_number):
 		pass
 		'''Soon™
        auth = {"username": "",
 				"password": ""}
 		data = {"commit_title": f"Merged by {ctx.author}",
 				"commit_message": "Merged from command"}
      	resp = await ctx.session.put(f'https://api.github.com/repos/dpy-blobs/AssBot/pulls/{pr_number}/merge', auth=auth, data=data)
 		if resp == 200:
 			await ctx.send(f"PR #{pr_number} | Successfully Merged")
 		else:
 			await ctx.send(f"PR #{pr_number} | Merge Unsuccessful")
 		'''


def setup(bot):
    bot.add_cog(Admin(bot))
