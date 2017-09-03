import discord.utils

from discord.ext import commands
from cogs.error import ExplicitCheckFailure


def nsfw():
    """A :func:`.check` that checks if the channel is a NSFW channel."""
    def pred(ctx):
        if isinstance(ctx.channel, discord.TextChannel) and ctx.channel.is_nsfw():
            return True
        raise ExplicitCheckFailure(ctx.command)
    return commands.check(pred)


async def check_permissions(ctx, perms):
    author = ctx.author
    if await ctx.bot.is_owner(author):
        return True

    resolved = ctx.channel.permissions_for(author)
    missing = [name for name, value in perms.items() if getattr(resolved, name, None) != value]
    if not missing:
        return True

    raise commands.MissingPermissions(missing)


async def role_or_permissions(ctx, check, **perms):
    if not isinstance(ctx.channel, discord.abc.GuildChannel):
        raise commands.NoPrivateMessage

    role = discord.utils.find(check, ctx.author.roles)
    if role:
        return True

    if await check_permissions(ctx, perms):
        return True

    return False


def has_contrib_role():
    async def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, id=352849291733237771)
        return role in ctx.author.roles
    return commands.check(predicate)

def mod_or_permissions(**perms):
    async def predicate(ctx):
        return await role_or_permissions(ctx, lambda r: r.name in ('Mod', 'Admin'), **perms)

    return commands.check(predicate)


def admin_or_permissions(**perms):
    async def predicate(ctx):
        return await role_or_permissions(ctx, lambda r: r.name == 'Admin', **perms)

    return commands.check(predicate)


def is_in_guilds(*guild_ids):
    def predicate(ctx):
        guild = ctx.guild
        if guild is None:
            return False
        return guild.id in guild_ids
    return commands.check(predicate)
