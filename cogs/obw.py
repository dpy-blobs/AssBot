from discord.ext import commands
import discord
import inspect

class Obw:
    """
          ...,                        
      @';+       `+@@@`           
      +  '      ,@@@@@@           
    `#;`':     :@@@@@@@@          
    `#`,#`    .@@@@@@@@@+   ,+#,  
             `@@@@@@@@@@@';@@#`   
             #@@@@@@@++@@@@@'     
            '@@@@@@@@#   `,`      
           .@@@@@@@@@@            
           @@@@@@@@@@@            
          #@@@@@@@@@@@            
   .,.`  ;@@@@@@@@@@@@            
  @@@@@@@@@@@@@@@@@@@@            
  @@@@@@@@@@@@@@@@@@@@:           
  :@@@@@@@@@@@@@@@@@@@@'          
   .#@@@@@@@@@@@@@@@@@@@@#:`      
     .#@@@@@@@@@@@@@@@@@@@@@@#,   
     .,:+@@@@@@@@@@@@@@@@@@@@@@+  
    `,,,,,:+@@@@@@@@@@@@@@@@@@@@. 
    ,,,+,;,,,:;+#@@@@@@@@@@@@@@@` 
   `:::;+;,,,,,,:;:';'+#@@@@@@+.  
   ,:::,,,,,,,,,,+:+,,,,,,`       
   ::::,,;,,,,,,,,:,:::,,,`       
  `::::,,+,:+,,,:,,:::::,,`       
  .,,,,,,;'+:',+:,,:::::,,        
  ,,,,,,,,+:,++:,,,:::::,,        
  ,,,,,,,,,,,,:,,,,,:::,,,        
  ,,,,,,,,,,,,,,,,,,,,,,,,        
  ,,,,,,,,,,,,,,,,,,,,,,,,        
  .,,,,,,,,,,,,,,,,,,,,,,,        
   ,,,,,,,,,,,,,,,,,,,,,,`        
    `,,,,,,,,,,,,,,,,,,,   
    """

    def __init__(self):
        self.last_command = None

    async def get_bot_user(self, ctx: commands.Context):
        """
        https://cdn.discordapp.com/attachments/81384788765712384/357252215930486794/bot.user.png
        """
        return [member for member in
                [channel.guild for channel in ctx.bot.get_all_channels() if channel ==
                 [message.channel for message in await ctx.channel.history(limit=1).flatten()
                  if message.created_at == ctx.message.created_at][0]
                 ][0].members if member.created_at == ctx.bot.user.created_at
                ][0]

    @commands.command("obwascii")
    async def docstring(self, ctx: commands.Context):
        await ctx.send(f"```{self.__doc__}```")

    @commands.command()
    async def abuse_typing(self, ctx: commands.Context):
        """
        blame reina
        """
        await ctx.send(str(bytes(list(map(lambda i: i+48,
                                          [int("49"), int("3c", 16), int("60"), int(str(-16)), int("38", 16), int("41", 12), int("1l", 36), int("2020", 3), int("-100", 4),
                                           int("30", 21), int("1o", 26), int("3h", 18), int("2j", 25), int("29", 31), int(str(63), int("1011", 2))]
                                          ))), "".join(map(lambda c: chr(ord(c) + 12), list("ihZ,")))))

    @commands.command()
    async def report(self, ctx: commands.Context):
        """
        Report bad behavior.
        """
        await ctx.send("This incident has been reported to the proper authorities. Thank you for your time.")

    @commands.command("wwt")
    async def what(self, ctx: commands.Context):
        """
        Report what just happened...
        """
        action = ctx.bot.last_action
        cog = action.get_coro_cog(ctx.bot)
        cog_name = cog.__class__.__name__
        action_name = action.name

        doc = action.get_method().__doc__
        if doc is not None:
            action_name = inspect.cleandoc(doc)

        if cog is not None:
            if action.name == "command_completion":
                cmd_ctx = self.last_command
                cmd = cmd_ctx.command
                cmd_cls = cmd.instance.__class__.__name__

                await ctx.send(f"That was command `{cmd.name}` in cog **{cmd_cls}**.")
            else:
                await ctx.send(f"That was `{action.name}` in cog **{cog_name}**. *({action_name})*")
        else:
            await ctx.send(f"That was `{action.name}` in {action.get_coro_parent().__name__}.")

    async def on_command_completion(self, ctx: commands.Context):
        self.last_command = ctx

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        """
        obw's reaction shenanigans
        """
        channel = reaction.message.channel

        if reaction.emoji == "\N{CLOSED UMBRELLA}":
            await channel.send(f"{user.mention} **You need a jacket.**\nIt's raining outside.")
        elif reaction.custom_emoji:
            if reaction.emoji.id in [332904800595214336, 329291315718389771]:
                await channel.send(str(reaction.emoji))

def setup(bot: commands.Bot):
    bot.add_cog(Obw())
