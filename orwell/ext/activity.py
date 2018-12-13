import discord
from datetime import datetime
from discord.ext import commands
from dynaconf import settings
import redis

def tracked_roles_key(ctx: commands.Context):
    return f'tracked-roles:{str(ctx.guild.id)}'


def user_activity_key(message: discord.Message):
    return f'user-act:{message.guild.id}'

def user_daily_activity_key(message: discord.Message):
    return f'user-daily-act:{message.guild.id}:{datetime.utcnow().date()}'

class Activity:
    def __init__(self, bot):
        self.bot = bot
        self.redis = redis.Redis(
            host=settings.REDIS.host,
            port=settings.REDIS.port,
            db=settings.REDIS.db
        )

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def add_roles(self, ctx: commands.Context, roles: commands.Greedy[commands.RoleConverter]):
        '''Add roles to track activity for.'''
        if(roles):
            role_ids = [ role.id for role in roles]
            result = self.redis.sadd(tracked_roles_key(ctx), *role_ids)
            await ctx.send(f'Added {result} roles!')
        else:
            await ctx.send(f'No roles specified!')


    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def remove_roles(self, ctx: commands.Context, roles: commands.Greedy[commands.RoleConverter]):
        '''Remove roles that are currently tracking activity.'''
        if(roles):
            role_ids = [ role.id for role in roles]
            result = self.redis.srem(tracked_roles_key, *role_ids)
            await ctx.send(f'Removed {result} roles!')
        else:
            await ctx.send(f'No roles specified!')

    @commands.command()
    @commands.is_owner()
    async def rdbsave(self, ctx: commands.Context):
        result = self.redis.save()
        await ctx.send(f'Responded with: {result}')



    async def on_message(self, message: discord.Message):
        if not isinstance(message.channel, discord.TextChannel):
            return

        if not isinstance(message.author, discord.Member):
            return

        if message.author.bot:
            return

        user_id = str(message.author.id)
        user_dict = dict([(user_id, 1)])
        self.redis.zadd(user_activity_key(message), user_dict, incr=True)
        self.redis.zadd(user_daily_activity_key(message), user_dict, incr=True)


    def __unload(self):
        del self.redis


def setup(bot: commands.Bot):
    bot.add_cog(Activity(bot))
