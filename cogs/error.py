import datetime
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

        embed = discord.Embed(title=f'Command Exception', color=discord.Color.red())
        embed.set_footer(text='Occured on')
        embed.timestamp = datetime.datetime.utcnow()

        exc = ''.join(traceback.format_exception(type(error), error, error.__traceback__, chain=False))
        embed.description = f'```py\n{exc}\n```'

        embed.add_field(name='Command', value=ctx.command.qualified_name)
        embed.add_field(name='Invoker', value=ctx.author)
        embed.add_field(name='Location', value=f'Guild: {ctx.guild}\nChannel: {ctx.channel}')
        embed.add_field(name='Message', value=ctx.message.content)

        hook = (await ctx.bot.get_channel(352915365577228289).webhooks())[0]
        await hook.send(embed=embed)


def setup(bot):
    bot.add_cog(CommandErrorHandler())
