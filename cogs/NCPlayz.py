import discord
from discord.ext import commands

class NCPlayz:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases = ["id"])
    async def ID(self, ctx):
        """Get the ID of a channel, user, or role"""
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid Type! {0.subcommand_passed} is not a valid command!'.format(ctx))

    @ID.command()
    async def channel(self, ctx, request):
        """Fetches the ID of a specified channel"""
        type = "channel"
        obj = get(ctx, type, request)
        if obj:
            msg = "The id of the channel `{0}` is `{0.id}".format(obj)
        else: 
            await ctx.send(content = "**Error!** A channel named {0} could not be found! You must enter the exact name (including caps).").format(request)

    @ID.command()
    async def role(self, ctx, request):
        """Fetches the ID of a specified role"""
        type = "role"
        obj = get(ctx, type, request)
        if obj:
            msg = "The id of the role `{0}` is `{0.id}".format(obj)
        else: 
            await ctx.send(content = "**Error!** A role named {0} could not be found! You must enter the exact name (including caps).").format(request)
    
    @ID.command(aliases = ["user"])
    async def member(self, ctx, request):
        """Fetches the ID of a specified member/user."""
        type = "member"
        obj = get(ctx, type, request)
        if obj:
            msg = "The id of the user `{0}` is `{0.id}".format(obj)
        else: 
            await ctx.send(content = "**Error!** A user named {0} could not be found! You must enter the exact name (including caps).").format(request)

    @ID.command()
    async def server(self, ctx):
        """Fetches the ID of the server """
        if obj:
            msg = "The id of the server `{0}` is `{0.id}".format(ctx.guild)

def get(ctx, type, name):
    if (type == "channel"):
        get = ctx.guild.channels
    elif (type == "user" or type == "member"):
        get = ctx.guild.members
    elif (type == "role"):
        get = ctx.guild.roles
    try:
        fin = discord.utils.get(get, name=name)
    except:
        print("failed")
    finally:
        return fin

def setup(bot):
    bot.add_cog(NCPlayz(bot))
    
