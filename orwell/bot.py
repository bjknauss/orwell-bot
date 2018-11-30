from dynaconf import settings
from discord.ext import commands

class OrwellBot(commands.Bot):
    '''Bot designed to track user activity.'''

    @commands.command()
    '''Test that the server is working properly.'''
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'pong! Current latency is {self.latency} ms')

