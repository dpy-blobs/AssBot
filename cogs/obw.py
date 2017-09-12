from discord.ext import commands
import discord

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

    @commands.command("__docstring__")
    async def docstring(self, ctx: commands.Context):
        await ctx.send(f"```{self.__doc__}```")

    @commands.command()
    async def report(self, ctx: commands.Context):
        """
        Report bad behavior.
        """
        await ctx.send("This incident has been reported to the proper authorities. Thank you for your time.")

    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.User):
        channel = reaction.message.channel

        if reaction.emoji == "\N{CLOSED UMBERELLA}":
            await channel.send(f"{user.mention} **You need a jacket.**\nIt's raining outside.")
        elif reaction.custom_emoji:
            if reaction.emoji.id == 332904800595214336:
                await channel.send(str(reaction.emoji))

def setup(bot: commands.Bot):
    bot.add_cog(Obw())
