import asyncio
import collections
import functools
import io
import random
import secrets

import discord
from discord.ext import commands
from PIL import Image


# Some large-ish Merseene prime cuz... idk.
_OFFSET = 2 ** 3217 - 1

# This seed is used to change the result of ->ship without having to do a
# complicated cache
_seed = 0


def _scale(old_min, old_max, new_min, new_max, value):
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


def _lerp(v0, v1, t):
    return v0 + t * (v1 - v0)

def _lerp_color(c1, c2, t, *, type=round):
    return tuple(round(_lerp(v1, v2, t)) for v1, v2 in zip(c1, c2))

_lerp_pink = functools.partial(_lerp_color, (0, 0, 0), (255, 105, 180))


async def _change_ship_seed():
    global _seed
    while True:
        _seed = secrets.randbits(256)
        next_delay = random.uniform(10, 60) * 60
        await asyncio.sleep(next_delay)


def _user_score(user):
    return (user.id
            + int(user.avatar or user.default_avatar.value, 16)
            # 0x10FFFF is the highest Unicode can go.
            + sum(ord(c) * 0x10FFFF * i for i, c in enumerate(user.name))
            + int(user.discriminator)
            )


_default_rating_comments = (
    'There is no chance for this to happen.',
    'Why...',
    'No way, not happening.',
    'Nope.',
    'Maybe.',
    'Woah this actually might happen.',
    'owo what\'s this',
    'You\'ve got a chance!',
    'Definitely.',
    'What are you waiting for?!',
)


_value_to_index = functools.partial(_scale, 0, 100, 0, len(_default_rating_comments) - 1)


class _ShipScore(collections.namedtuple('_ShipRating', 'score comment')):
    __slots__ = ()

    def __new__(cls, score, comment=None):
        if comment is None:
            index = round(_value_to_index(score))
            print(index)
            comment = _default_rating_comments[index]
        return super().__new__(cls, score, comment)


# List of possible ratings when someone attempts to ship themself
_self_ratings = [
    _ShipScore(0, "Rip {user1}, they're forever alone..."),
    _ShipScore(100, "Selfcest is bestest.")
]


def _calculate_rating(user1, user2):
    if user1 == user2:
        return _self_ratings[_seed % 2]

    score = ((_user_score(user1) + _user_score(user2)) * _OFFSET + _seed) % 100
    return _ShipScore(score)


class Ikusaba:
    def __init__(self, bot):
        if not hasattr(bot, 'session'):
            import aiohttp
            bot.session = aiohttp.ClientSession()

        self.bot = bot
        self._mask = open('cogs/resources/miku/heart.png', 'rb')
        self._future = asyncio.ensure_future(_change_ship_seed())

    def __unload(self):
        self._mask.close()
        self._future.cancel()

    async def _load_user_avatar(self, user):
        url = user.avatar_url_as(format='png', size=512)
        async with self.bot.session.get(url) as r:
            return await r.read()

    def _create_ship_image(self, score, avatar1, avatar2):
        ava_im1 = Image.open(avatar1).convert('RGBA')
        ava_im2 = Image.open(avatar2).convert('RGBA')

        # Assume the two images are square
        size = min(ava_im1.size, ava_im2.size)
        offset = round(_scale(0, 100, size[0], 0, score))

        ava_im1.thumbnail(size)
        ava_im2.thumbnail(size)

        # paste img1 on top of img2
        newimg1 = Image.new('RGBA', size=size, color=(0, 0, 0, 0))
        newimg1.paste(ava_im2, (-offset, 0))
        newimg1.paste(ava_im1, (offset, 0))

        # paste img2 on top of img1
        newimg2 = Image.new('RGBA', size=size, color=(0, 0, 0, 0))
        newimg2.paste(ava_im1, (offset, 0))
        newimg2.paste(ava_im2, (-offset, 0))

        # blend with alpha=0.5
        im = Image.blend(newimg1, newimg2, alpha=0.6)

        mask = Image.open(self._mask).convert('L')
        mask = mask.resize(ava_im1.size, resample=Image.BILINEAR)
        im.putalpha(mask)

        f = io.BytesIO()
        im.save(f, 'png')
        f.seek(0)
        return discord.File(f, filename='test.png')

    async def _ship_image(self, score, user1, user2):
        user_avatar_data1 = io.BytesIO(await self._load_user_avatar(user1))
        user_avatar_data2 = io.BytesIO(await self._load_user_avatar(user2))
        return await self.bot.loop.run_in_executor(None, self._create_ship_image, score,
                                                   user_avatar_data1, user_avatar_data2)

    @commands.command()
    async def testship(self, ctx, user1: discord.Member, user2: discord.Member=None):
        """Ships two users together, and scores accordingly."""
        if user2 is None:
            user1, user2 = ctx.author, user1

        score, comment = _calculate_rating(user1, user2)
        file = await self._ship_image(score, user1, user2)
        colour = discord.Colour.from_rgb(*_lerp_pink(score / 100))

        embed = (discord.Embed(colour=colour, description=f"{user1.mention} x {user2.mention}")
                 .set_author(name=f'Shipping')
                 .add_field(name='Score', value=f'{score}/100')
                 .add_field(name='\u200b', value=f'*{comment}*', inline=False)
                 .set_image(url='attachment://test.png')
                 )
        await ctx.send(file=file, embed=embed)


def setup(bot):
    bot.add_cog(Ikusaba(bot))
