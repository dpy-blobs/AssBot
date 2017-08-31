import traceback
import sys
import discord.ext


class AssBaseException:
    """Base exception for Class for AssBot."""
    pass


class CommandErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        if isinstance(error, discord.ext.commands.CommandNotFound):
            return

        try:
            if isinstance(error.original, discord.errors.Forbidden):
                await ctx.send(f'**I do not have the required permissions to run this command.**')
        except AttributeError:
            pass

        if isinstance(error, discord.ext.commands.DisabledCommand):
            try:
                await ctx.send(f'{ctx.command} has been disabled.')
            except:
                pass
            finally:
                return

        if isinstance(error, discord.ext.commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except:
                pass
            finally:
                return

        if isinstance(error, discord.ext.commands.BadArgument):
            return

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
