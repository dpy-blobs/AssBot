from discord.ext import commands



class Alex:
    """made by Alex from Alaska#9760 ( 108429628560924672 )"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx, msg:int, channel: discord.TextChannel=None):
        """Quotes a message"""
        try:
            if channel is not None:
                msg = await channel.get_message(msg)
            else:
                msg = await ctx.channel.get_message(msg)
        except discord.errors.NotFound:
            await ctx.send("cant find that message. \N{SLIGHTLY FROWNING FACE}")
        assert isinstance(msg, discord.Message)

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


def setup(bot):
    bot.add_cog(Alex(bot))
