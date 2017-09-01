import discord.utils

from discord.ext import commands


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
