import discord
import humanize
from discord.ext import commands


class Alex:
    """made by Alex from Alaska#9760 ( 108429628560924672 )"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx, msg, channel: discord.TextChannel=None):
        """
        Quotes a message.
        msg can be message ID or the output of shift clicking the 'copy id' button in the UI.
        """
        if '-' in msg:
            try:
                channel, msg = [int(i) for i in msg.split('-')]
                channel = self.bot.get_channel(channel)
            except ValueError or discord.errors.NotFound:
                raise commands.BadArgument("your input was not a message id")
        try:
            if channel is None:
                msg = await ctx.channel.get_message(msg)
            else:
                msg = await channel.get_message(msg)
        except (discord.errors.NotFound, discord.errors.HTTPException):
            return await ctx.send("cant find that message. \N{SLIGHTLY FROWNING FACE}")
        assert isinstance(msg, discord.Message)

        if channel is not None and channel.nsfw and not ctx.channel.nsfw:
            return await ctx.send("Cant send message from NSFW channel in SFW channel")

        ret = discord.Embed(color=discord.Color.blurple())

        if msg.content is "" and msg.attachments == []:
            embed = msg.embeds[0]
            try:
                assert isinstance(embed, discord.Embed)
            except AssertionError:
                return
            ret = embed
        else:
            ret.description = msg.content

            # handle images, and images attached with URLs
            try:
                ret.set_image(url=msg.attachments[0].url)
            except IndexError:
                try:
                    ret.set_image(url=msg.embeds[0].thumbnail.url)
                except IndexError:
                    pass

        ret.timestamp = msg.created_at
        ret.set_author(name=msg.author.name, icon_url=msg.author.avatar_url)
        age = ctx.message.created_at - ret.timestamp
        age = humanize.naturaldelta(age)

        ret.set_footer(text=f"Quoted message is {age} old, from ")

        await ctx.send(embed=ret)

    @commands.command()
    async def difference(self, ctx, object_one: int, object_two: int=None):
        """
        compares the creation of two discord IDs.
        interprets a missing second arg as the current ID.
        """
        one = discord.utils.snowflake_time(object_one)
        if object_two is None:
            object_two = ctx.message.id
        two = discord.utils.snowflake_time(object_two)
        if one > two:
            diff = two - one
        else:
            diff = one - two
        diff = humanize.naturaldelta(diff)
        one = humanize.naturaldate(one)
        two = humanize.naturaldate(two)
        await ctx.send(f'time difference from {one} to {two} is {diff}.')


def setup(bot):
    bot.add_cog(Alex(bot))
