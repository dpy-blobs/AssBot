import asyncio

import discord


class CannotPaginate(Exception):
    pass


class Pages:
    """Implements a paginator that queries the user for the
    pagination interface.

    Pages are 1-index based, not 0-index based.

    If the user does not reply within 2 minutes then the pagination
    interface exits automatically.

    Parameters
    ------------
    ctx
        The ctx object.
    entries
        A list of entries to paginate.
    per_page
        How many entries show up per page.

    Attributes
    -----------
    embed: discord.Embed
        The embed object that is being used to send pagination info.
        Feel free to modify this externally. Only the description,
        footer fields, and colour are internally modified.
    permissions: discord.Permissions
        Our permissions for the channel.
    """
    def __init__(self, ctx, *, entries, per_page=12):
        self.ctx = ctx
        self.bot = ctx.bot
        self.entries = entries
        self.author = ctx.author
        self.per_page = per_page
        pages, left_over = divmod(len(self.entries), self.per_page)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        self.embed = discord.Embed()
        self.paginating = len(entries) > per_page
        self.reaction_emojis = [
            ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.first_page),
            ('\N{BLACK LEFT-POINTING TRIANGLE}', self.previous_page),
            ('\N{BLACK RIGHT-POINTING TRIANGLE}', self.next_page),
            ('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.last_page),
            ('\N{INPUT SYMBOL FOR NUMBERS}', self.numbered_page),
            ('\N{BLACK SQUARE FOR STOP}', self.stop_pages),
            ('\N{INFORMATION SOURCE}', self.show_help),
        ]

        guild = ctx.guild
        if guild is not None:
            self.permissions = self.ctx.channel.permissions_for(guild.me)
        else:
            self.permissions = self.ctx.channel.permissions_for(self.bot.user)

        if not self.permissions.embed_links:
            raise CannotPaginate('Bot does not have embed links permission.')

    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.entries[base:base + self.per_page]

    async def show_page(self, page, *, first=False):
        self.current_page = page
        entries = self.get_page(page)
        p = []
        for t in enumerate(entries, 1 + ((page - 1) * self.per_page)):
            p.append('%s. %s' % t)

        self.embed.set_footer(text=f'Page {page}/{self.maximum_pages} ({len(self.entries)} entries)')

        if not self.paginating:
            self.embed.description = '\n'.join(p)
            return await self.ctx.send(embed=self.embed)

        if not first:
            self.embed.description = '\n'.join(p)
            await self.message.edit(embed=self.embed)
            return

        # verify we can actually use the pagination session
        if not self.permissions.add_reactions:
            raise CannotPaginate('Bot does not have add reactions permission.')

        if not self.permissions.read_message_history:
            raise CannotPaginate('Bot does not have Read Message History permission.')

        p.append('')
        p.append('Confused? React with \N{INFORMATION SOURCE} for more info.')
        self.embed.description = '\n'.join(p)
        self.message = await self.ctx.send(embed=self.embed)
        for (reaction, _) in self.reaction_emojis:
            if self.maximum_pages == 2 and reaction in ('\u23ed', '\u23ee'):
                # no |<< or >>| buttons if we only have two pages
                # we can't forbid it if someone ends up using it but remove
                # it from the default set
                continue

            await self.message.add_reaction(reaction)

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        """goes to the first page"""
        await self.show_page(1)

    async def last_page(self):
        """goes to the last page"""
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        """goes to the next page"""
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        """goes to the previous page"""
        await self.checked_show_page(self.current_page - 1)

    async def show_current_page(self):
        if self.paginating:
            await self.show_page(self.current_page)

    async def numbered_page(self):
        """lets you type a page number to go to"""
        to_delete = []
        to_delete.append(await self.ctx.send('What page do you want to go to?'))

        def check(m):
            return m.author == self.author and m.channel == self.message.channel and m.content.isdigit()

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
        except:
            to_delete.append(await self.ctx.send('Took too long.'))
        else:
            page = int(msg.content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                to_delete.append(await self.ctx.send(f'Invalid page given. ({page}/{self.maximum_pages})'))
        await asyncio.sleep(5)

        try:
            await self.message.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def show_help(self):
        """shows this message"""
        e = discord.Embed()
        messages = ['Welcome to the interactive paginator!\n']
        messages.append('This interactively allows you to see pages of text by navigating with '
                        'reactions. They are as follows:\n')

        for (emoji, func) in self.reaction_emojis:
            messages.append(f'{emoji} {func.__doc__}')

        e.description = '\n'.join(messages)
        e.colour = 0x738bd7  # blurple
        e.set_footer(text=f'We were on page {self.current_page} before this message.')
        await self.message.edit(embed=e)

        async def go_back_to_current_page():
            await asyncio.sleep(60.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def stop_pages(self):
        """stops the interactive pagination session"""
        await self.message.delete()
        self.paginating = False

    def react_check(self, reaction, user):
        if reaction.message.id != self.message.id:
            return False
        if user is None or user.id != self.author.id:
            return False

        for (emoji, func) in self.reaction_emojis:
            if reaction.emoji == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        """Actually paginate the entries and run the interactive loop if necessary."""
        await self.show_page(1, first=True)

        while self.paginating:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=self.react_check, timeout=120.0)
            except:
                self.paginating = False
                try:
                    await self.message.clear_reactions()
                except:
                    pass
                finally:
                    break

            try:
                await self.message.remove_reaction(reaction.emoji, user)
            except:
                pass  # can't remove it so don't bother doing so

            await self.match()
