import discord
from discord.ext import commands

from cogs.error import InvalidChannelCheck, BotPermissionsCheck


class Spoon:
    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        """checks to see if the command was used in a guild
         and if bot has perms to perform mod tasks"""
        if not isinstance(ctx.channel, discord.TextChannel):
            raise InvalidChannelCheck(ctx.command)
        me = ctx.me.guild_permissions
        perms = (me.manage_messages, me.manage_nicknames, me.ban_members, me.kick_members)
        if not all(perms):
            raise BotPermissionsCheck(ctx.command)
        else:
            return True

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, target: discord.Member, reason=None):
        """kicks a pleb from the server"""
        await target.kick(reason=reason)
        await ctx.send(f'\N{OK HAND SIGN} {target} kicked')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, target: discord.Member, reason=None):
        """bans a pleb from the server"""
        await target.ban(reason=reason)
        await ctx.send(f'\N{OK HAND SIGN} {target} banned')

    @commands.command(aliases=['soft'])
    @commands.has_permissions(kick_members=True)
    async def softban(self, ctx, target: discord.Member, reason=None):
        """softbans a pleb from the server"""
        await target.ban(reason=reason)
        await target.unban(reason=reason)
        await ctx.send(f'\N{OK HAND SIGN} {target} softbanned')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, target: discord.Member=None, amount: int=10):
        """removes messages from target, max messages 100, default target is Bot"""
        if amount > 100:
            return ctx.send('Maximum messages is 100')
        if target is None:
            target = ctx.me
        await ctx.message.delete()
        delete = []
        async for m in ctx.channel.history(limit=200):
            if m.author == target:
                delete.append(m)
        await ctx.channel.delete_messages(delete[:amount - 1])

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, amount: int = 30):
        """Removes all messages in channel, default amount: 30, max 100"""
        if amount > 100:
            return ctx.send('Maximum messages is 100')
        await ctx.channel.purge(limit=amount)
        
        async def on_member_update(self, b, a):
        if b.id == 353535708310536202:
            if a.status.offline:
                spoon = self.bot.get_user(120636888418615300)
                e = discord.Embed(title='Botto Offline', colour=0x0fa03f)
                current = datetime.datetime.utcnow().strftime('%H:%M %d/%m/%Y')
                e.add_field(name='\uFEFF', value=current)
                return await spoon.send(embed=e)


def setup(bot):
    bot.add_cog(Spoon(bot))
