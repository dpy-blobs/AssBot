import discord
from discord.ext import commands

class NCPlayz:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=["user_info"])
    async def userinfo(self, ctx, member: discord.Member = None):
        """Shows a profile. Defaults to you."""
        if member is None:
            member = ctx.message.author

        userinfo_embed = discord.Embed(
            title=f"{member.name}'s Profile",
            color=member.color
        )
        userinfo_embed.add_field(
            name="User:",
            value=str(member)
        )
        if member.display_name != member.name:
            userinfo_embed.add_field(
                name="Nickname:",
                value=member.display_name
            )
        userinfo_embed.add_field(
            name="Status:",
            value=str(member.status).title()
        )
        userinfo_embed.add_field(
            name="Playing:",
            value=str(member.game)
        )
        userinfo_embed.add_field(
            name="ID:",
            value=str(member.id)
        )
        userinfo_embed.add_field(
            name="Account Created At:",
            value=f"{member.created_at} UTC"
        )
        userinfo_embed.add_field(
            name="Joined Guild At:",
            value=f"{member.joined_at} UTC"
        )
        userinfo_embed.add_field(
            name="Roles:",
            value=', '.join([r.name for r in sorted(member.roles, key=lambda r: -r.position)])
        )
        userinfo_embed.set_thumbnail(url=ctx.message.author.avatar_url)
        userinfo_embed.set_footer(text=f"""{member}'s Profile | Requested by: 
        {ctx.message.author}""", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=userinfo_embed)

    @commands.command(aliases=["guild", "guildinfo", "serverinfo"])
    async def server(self, ctx):
        """Displays Server Info"""
        if ctx.guild.emojis:
            emotes = ''.join((str(x) for x in ctx.guild.emojis))
        server_embed = discord.Embed(
            title=f"The {ctx.guild.name} Server"
        )
        server_embed.add_field(
            name="Server ID:",
            value=str(ctx.guild.id)
        )
        text_count = len(ctx.guild.text_channels)
        voice_count = len(ctx.guild.voice_channels)
        text_hid = sum(
            1 for c in ctx.guild.channels
            if c.overwrites_for(ctx.guild.default_role).read_messages is False)
        server_embed.add_field(
            name="Channels",
            value=f"{text_count} Text ({text_hid}) Hidden / {voice_count} Voice"
        )
        server_embed.add_field(
            name="Owner:",
            value=ctx.guild.owner.mention
        )
        server_embed.add_field(
            name="Region:",
            value=ctx.guild.region
        )
        server_embed.add_field(
            name="Created:",
            value=f"{ctx.guild.created_at} UTC"
        )
        server_embed.add_field(
            name="Emotes:",
            value=f"{emotes}"
        )
        server_embed.add_field(
            name="Server Members:",
            value=str(ctx.guild.member_count)
        )
        roles_list = [r.mention.replace(f'<@&{ctx.guild.id}>', '@everyone') for r in
                      reversed(sorted(ctx.guild.roles, key=lambda role: role.position))]
        roles = ', '.join(roles_list)
        server_embed.add_field(
            name="Roles",
            value=roles
        )
        server_embed.set_thumbnail(url=ctx.guild.icon_url)
        server_embed.set_footer(text=f"""The {ctx.guild.name} Server Information | Requested by: 
        {ctx.message.author}""", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=server_embed)

def setup(bot):
    bot.add_cog(NCPlayz(bot))
