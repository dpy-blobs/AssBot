import discord
from discord.ext import commands
import math
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO
import math # Why
import cmath
import collections
import aiohttp
import time
import random

okay = [[1, 1, 1],
        [1, 1, 2],
        [1, 2, 2],
        [1, 1, 3],
        [1, 2, 3],
        [18, 23, 27]]


class Circle():
    def __init__(self, x, y, r):
        """
            I probably don't need self.x or self.y with self.m...
            but I don't feel comfortable working with complex numbers yet :(
        """
        self.r = r
        self.x = x
        self.y = y
        self.m = (x+y*1j)
    def __hash__(self):
        return self.r+self.x+self.y
    def __eq__(self, c):
        if isinstance(c, Circle):
            return self.r == c.r and self.x == c.x and self.y == c.y
    def curv(self):
        """
            Curvature of a circle is apparently the inverse of its radius...
            Who knew?
        """
        return 1/self.r
    @property
    def bound(self):
        """
            Returns the upper left and bottom right coordinates that bound the circle
        """
        r = abs(self.r.real)
        return (int(self.x-r), int(self.y-r), int(self.x+r), int(self.y+r))
    @property
    def size(self):
        """
            For some reason self.r turns into an imaginary number...
            I don't know why?
        """
        return abs(self.r.real)
    def correct(self, cx, cy):
        """
            Literally just shifts the center of the circle off by whatever cx and cy are
        """
        self.x += cx
        self.y += cy
        self.m = (self.x+self.y*1j)
    def resize(self, factor):
        """
            With any luck, this rezies the circle with respect to the origin?
            Should maintain kissing
        """
        self.x *= factor
        self.y *= factor
        self.r *= factor
        self.m = (self.x+self.y*1j)

class Mycircles():
    def __init__(self, r1, r2, r3):
        self.circles = list(self.tang(1/r1, 1/r2, 1/r3))
        self.big = self.circles[0]
        self.todo = collections.deque()
    @property
    def num(self):
        return len(self.circles)
    def outer(self, c1, c2, c3):
        """Quality function that takes 3 circles and finds the outer circle what kisses all three"""
        cur1 = c1.curv()
        cur2 = c2.curv()
        cur3 = c3.curv()
        m1 = c1.m
        m2 = c2.m
        m3 = c3.m
        cur4 = cur1 + cur2 + cur3 - 2 * cmath.sqrt(cur1 * cur2 + cur2 * cur3 + cur3 * cur1) # Descartes theorem
        m4 = (cur1 * m1 + cur2 * m2 + cur3 * m3 - 2 * cmath.sqrt(cur1 * m1 * cur2 * m2 + cur2 * m2 * cur3 * m3 + cur3 * m3 * cur1 * m1)) / cur4 # Magic
        return Circle(m4.real, m4.imag, 1/cur4)
    def tang(self, r2, r3, r4):
        """Quality function that takes 3 radiuses and makes 4 circles that are kissing"""
        c2 = Circle(0, 0, r2) #The first circle is placed at the origin
        c3 = Circle(r2 + r3, 0, r3) #The second circle is placed kissing the first circle to the right
        x = (r2 * r2 + r2 * r4 + r2 * r3 - r3 * r4) / (r2 + r3) #Magic triangle maths to figure out where the of the third circle should go
        y = cmath.sqrt((r2 + r4) * (r2 + r4) - x * x)
        c4 = Circle(x.real, y.real, r4)
        c1 = self.outer(c2, c3, c4) # The outer circle is generated based on the first 3
        offx = 0 - c1.x
        offy = 0 - c1.y
        c2.correct(offx, offy) # Offsets all the circles so the biggest circle is centered instead of the first circle
        c3.correct(offx, offy)
        c4.correct(offx, offy)
        c1.correct(offx, offy)
        return (c1, c2, c3, c4)
    def sec(self, fixed, c1, c2, c3):
        """
            Quality function that takes one fixed circle and three circles.
            A new circle is generated such that it kisses the three circles but not the fixes circle.
        """
        curf = fixed.curv()
        cur1 = c1.curv()
        cur2 = c2.curv()
        cur3 = c3.curv()
        curn = 2 * (cur1 + cur2 + cur3) - curf
        mn = (2 * (cur1 * c1.m + cur2 * c2.m + cur3 * c3.m) - curf * fixed.m) / curn
        return Circle(mn.real, mn.imag, 1/curn)
    def fakerecursion(self, depth):
        """
            Fucking python won't let me do recursion properly so its 100% faked with a dequeue and a while loop
        """
        curdepth = 0
        self.todo.append(self.circles + [curdepth])
        while curdepth < depth:
            c1, c2, c3, c4, curdepth = self.todo.popleft() 
            if curdepth == 0:
                cn1 = self.sec(c1, c2, c3, c4)
                self.circles.append(cn1)
                self.todo.append([cn1, c2, c3, c4, curdepth + 1])
            cn2 = self.sec(c2, c1, c3, c4)
            if cn2 not in self.circles:
                self.circles.append(cn2)
            else:
                print("dup")
            self.todo.append([cn2, c1, c3, c4, curdepth + 1])
            cn3 = self.sec(c3, c1, c2, c4)
            if cn3 not in self.circles:
                self.circles.append(cn3)
            else:
                print("dup")
            self.todo.append([cn3, c1, c2, c4, curdepth + 1])
            cn4 = self.sec(c4, c1, c2, c3)
            if cn4 not in self.circles:
                self.circles.append(cn4)
            else:
                print("dup")
            self.todo.append([cn4, c1, c2, c3, curdepth + 1])

class Cute:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def ute(self, ctx):
        pre = self.bot.command_prefix()
        if pre == 'C':
            msg = 'You too~!'
        elif pre == 'M':
            msg = 'I will not!'
        await ctx.send(msg)
        
    @commands.command()
    async def quilt(self, ctx, *mems : discord.Member):
        if len(mems) == 0:
            mems = [ctx.author]
        avys = []
        for mem in mems:
            async with ctx.session.get(mem.avatar_url_as(format='png', size=512)) as r:
                avys.append(BytesIO(await r.read()))
        file = await self.bot.loop.run_in_executor(None, self._quilt, avys)
        await ctx.send(file=file)
    def _quilt(self, avys):
        """
            Makes a quilt of avatars of mems that tries to be as square as possible
        """
        xbound = math.ceil(math.sqrt(len(avys)))
        ybound = math.ceil(len(avys)/xbound)
        size = int(2520/xbound)
        base = Image.new(mode='RGBA', size=(xbound * size, ybound * size), color=(0, 0, 0, 0))
        x, y = 0, 0
        for avy in avys:
            im = Image.open(avy)
            base.paste(im.resize((size, size), resample=Image.BILINEAR), box=(x * size, y * size))
            if x < xbound - 1:
                x += 1
            else:
                x = 0
                y += 1
        buffer = BytesIO()
        base.save(buffer, 'png')
        buffer.seek(0)
        return discord.File(buffer, filename='quilt.png')

    @commands.command()
    async def avys(self, ctx, *plebs : discord.Member):
        """
            Makes a Apollonian gasket of avatars of plebs
        """
        if len(plebs) == 0:
            plebs = [ctx.author]
        datas = []
        async with ctx.channel.typing():
            for p in plebs:
                async with ctx.session.get(p.avatar_url_as(format='png')) as r:
                    datas.append(BytesIO(await r.read()))
            stime = time.monotonic()
            starting = random.choice(okay)
            random.shuffle(starting)
            file, i = await self.bot.loop.run_in_executor(None, self._fucker, 5, datas, False, starting)
            await ctx.send(f'*{i} Avatars drawn in {(time.monotonic() - stime)*1000:.2f}ms*', file=file)
    
    @commands.command()
    async def circles(self, ctx):
        """
            Makes a Apollonia gasket of uploaded attachments.
            Will fuck them up with resizing non-square images because I haven't decided how to crop them yet
        """
        if len(ctx.message.attachments) == 0:
            return
        datas = []
        async with ctx.channel.typing():
            for p in ctx.message.attachments:
                if p.width:
                    async with ctx.session.get(p.url) as r:
                        datas.append(BytesIO(await r.read()))
            if len(datas) == 0:
                return
            stime = time.monotonic() # Someone go fix this
            startingstuff = random.choice(okay)
            print(startingstuff)
            random.shuffle(startingstuff)
            print(startingstuff)
            file, i = await self.bot.loop.run_in_executor(None, self._fucker, 5, datas, False, startingstuff)
            await ctx.send(f'*{i} Avatars drawn in {(time.monotonic() - stime)*1000:.2f}ms*', file=file)
    @commands.command()
    async def avyserver(self, ctx):
        mems = ctx.guild.members
        await ctx.invoke(self.bot.get_command('avys'), *random.sample(mems, len(mems) if len(mems) <= 50 else 50))
    
    def _fucker(self, depth, data, firstlayer, starting):
        imgsize = 400 # Fixes intger because bleh. Should fix.
        asdf = Mycircles(starting[0], starting[1], starting[2])
        factor = ((imgsize/2)-1)/asdf.big.size # After initializing the first 4 circles from the 3 radiuses(?), resize them such that they fill imgsize
        for c in asdf.circles:
            c.resize(factor)
        asdf.fakerecursion(depth) # This is where the magic happens
        im = Image.new('RGBA', (imgsize, imgsize), color=(0, 0, 0, 0))
        maska = Image.new('RGBA', (1024, 1024), color=(0, 0, 0, 0))
        maskb = Image.new('L', (1024, 1024), color=255)
        draw = ImageDraw.Draw(maskb)
        draw.ellipse(((0,0), (1024, 1024)), fill=0)
        del draw
        maska.putalpha(maskb)
        imgs = collections.deque()
        for d in data:
            temp = Image.open(d).resize((1024, 1024), resample=Image.BILINEAR).convert('RGBA')
            avymask = temp.split()[3]
            avymask.paste(maska, (0, 0, 1024, 1024), maska)
            temp.putalpha(avymask) # Basically magic PIL stuff to crop a circle out of the image. Can probably be done more efficently
            imgs.append(temp)
        i = 0
        first = True
        for a in asdf.circles:
            if not firstlayer and first: # Whether or not to draw the outer circle that encompases everything
                first = False
                continue
            a.correct(imgsize/2, imgsize/2)
            x, y = a.bound[2]-a.bound[0], a.bound[3]-a.bound[1]
            if not x or not y: # Skips trying to draw zero width circles
                continue # Don't break because the list of circles aren't ordered by size
            curr = imgs.popleft()
            temp = curr.resize((x, y), resample=Image.BILINEAR)
            im.paste(temp, box=a.bound, mask=temp)
            imgs.append(curr)
            i += 1
        bb = BytesIO()
        im.save(bb, 'png')
        bb.seek(0)
        return (discord.File(bb, filename='fuckery.png'), i)
        
def setup(bot):
    bot.add_cog(Cute(bot))