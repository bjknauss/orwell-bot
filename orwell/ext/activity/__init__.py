from discord.ext import commands
from orwell.ext.activity import cog

def setup(bot: commands.Bot):
    bot.add_cog(cog.ActivityCog(bot))
