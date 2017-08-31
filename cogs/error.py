import traceback

import discord
from discord.ext import commands


class CommandErrorHandler:
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        ctx   : Context
        error : Exception"""

        error = getattr(error, 'original', error)

        ignored = (commands.CommandNotFound, commands.BadArgument)
        if isinstance(error, ignored):
            return

        handler = {
            discord.Forbidden: '**I do not have the required permissions to run this command.**',
            commands.DisabledCommand: f'{ctx.command} has been disabled.',
            commands.NoPrivateMessage: f'{ctx.command} can not be used in Private Messages.',
        }

        try:
            message = handler[type(error)]
        except KeyError:
            pass
        else:
            return await ctx.send(message)

        embed = discord.Embed(title=f'Exception in command {ctx.command}')
        exc = ''.join(traceback.format_exception(type(error), error, error.__traceback__, chain=False))
        embed.description = exc
        await ctx.bot.get_channel(352915365577228289).send(embed=embed)


def setup(bot):
    bot.add_cog(CommandErrorHandler())
