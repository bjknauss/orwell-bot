from dynaconf import settings
from discord.ext import commands

bot = commands.Bot(command_prefix=',', description='Bot designed to track user activity.')
bot.load_extension('orwell.ext.activity')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')


@bot.command()
async def ping(ctx: commands.Context):
    '''Test that the server is working properly.'''
    await ctx.send(f'pong! Current latency is {round(bot.latency * 1000)} ms')
