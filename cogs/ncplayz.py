import discord
from discord.ext import commands

class NCPlayz:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ["id"])
    async def ID(self, ctx):
        """Get the ID of a channel, user, role, or the server."""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Type! {0.subcommand_passed} is not a valid command!'.format(ctx))

    @ID.command()
    async def channel(self, ctx, *, channel: discord.TextChannel = None):
        """Fetches the ID of a specified channel"""
        channel = channel or ctx.channel
        msg = "The id of the channel `{0}` is `{0.id}".format(channel)
        await ctx.send(msg)
        
    @channel.error
    async def error_channel(self, ctx):
        if isinstance(exception, commands.BadArgument):
            await ctx.send("Invalid Channel ID! Make sure it is case sensitive and is spelt correctly.")
            
    @ID.command()
    async def role(self, ctx, *, role: discord.Role):
        """Fetches the ID of a specified role"""
        if role:
             msg = "The id of the role `{0}` is `{0.id}".format(role)
        await ctx.send(msg)
        
    @role.error
    async def error_role(self, ctx):
        if isinstance(exception, commands.BadArgument):
            await ctx.send("Invalid Role ID! Make sure it is case sensitive and is spelt correctly.")
    
    @ID.command()
    async def member(self, ctx, *, member: discord.Member = None):
        """Fetches the ID of a specified member/user."""
        member = member or ctx.author
        if member:
            msg = "The id of the member `{0.name}` is `{0.id}".format(member)
        await ctx.send(msg)
      

    @member.error
    async def error_member(self, ctx):
        if isinstance(exception, commands.BadArgument):
            await ctx.send("Invalid Member ID! Make sure it is case sensitive and is spelt correctly.")
            
    @commands.guild_only()            
    @ID.command()
    async def server(self, ctx):
        """Fetches the ID of the server """
        msg = "The id of the server `{0}` is `{0.id}".format(ctx.guild)
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(NCPlayz(bot))
