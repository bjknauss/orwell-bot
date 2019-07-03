import discord
from discord.ext import commands
from typing import Optional
from redis import Redis
from dynaconf import settings
from orwell.ext.activity import keys, utils, shared
from datetime import date


class ActivityCog:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.redis: Redis = Redis(
            host=settings.REDIS.host,
            port=settings.REDIS.port,
            db=settings.REDIS.db)

    def get_result_set(self, key: str, start=0, num=1000,
                       role_filter=None) -> shared.RawResultSet:
        results = self.redis.zrevrangebyscore(
            key, '+inf', 0, withscores=True, start=start, num=num)
        if isinstance(role_filter, discord.Role):
            results = utils.filter_by_role(results, role_filter)
        return results

    @commands.command(aliases=['top_month', 'mtop'], name='top')
    @commands.guild_only()
    async def top_month(self,
                        ctx: commands.Context,
                        role: Optional[discord.Role] = None):
        '''Check user activity for this month.'''
        key = keys.monthly(ctx.message)
        results = self.get_result_set(key, role_filter=role)
        results = results[:25]
        results = utils.parse_results(self.bot, results)

        title = ctx.message.created_at.strftime('Top - %b')
        resp = self.print_top_results(ctx, results, title=title)
        await ctx.send(resp)

    @commands.command(aliases=['last_month', 'mlast'], name='last')
    @commands.guild_only()
    async def last_month(self,
                         ctx: commands.Context,
                         role: Optional[discord.Role] = None):
        '''Check last months activity.'''
        last_month = utils.get_previous_month(ctx)
        key = keys.monthly(ctx.message, last_month)
        results = self.get_result_set(key, role_filter=role)
        results = results[:25]
        results = utils.parse_results(self.bot, results)

        title = last_month.strftime('Top - %b')
        resp = self.print_top_results(ctx, results, title=title)
        await ctx.send(resp)

    @commands.command(aliases=['ms'], name='month_search')
    @commands.guild_only()
    async def month_search(self,
                           ctx: commands.Context,
                           year: int,
                           month: int,
                           role: Optional[discord.Role] = None):
        '''Allows you to check activity for a given month.'''
        if (month < 1 or month > 12):
            await ctx.send(f'"{month}" is not a valid month...')
            return
        d = date(year, month, 1)
        key = keys.monthly(ctx.message, d)
        results = self.get_result_set(key, role_filter=role)
        results = results[:25]
        results = utils.parse_results(self.bot, results)

        title = d.strftime('Top - %b')
        resp = self.print_top_results(ctx, results, title=title)
        await ctx.send(resp)

    async def on_message(self, message: discord.Message):
        if not isinstance(message.channel, discord.TextChannel):
            return

        if not isinstance(message.author, discord.Member):
            return

        if message.author.bot:
            return

        weekly = keys.weekly(message)
        monthly = keys.monthly(message)
        total = keys.total(message)

        user_id = str(message.author.id)
        user_dict = dict([(user_id, 1)])
        self.redis.zadd(weekly, user_dict, incr=True)
        self.redis.zadd(monthly, user_dict, incr=True)
        self.redis.zadd(total, user_dict, incr=True)

    def print_top_results(self,
                          ctx: commands.Context,
                          results: shared.ResultSet,
                          start=1,
                          title='Top Active'):
        response = f'__**{title}**__:\n\n'
        is_staff = utils.is_staff(ctx.author)

        for count, value in enumerate(results, start):
            response += utils.print_top_result_item(count, value, is_staff)

        return response

    def __unload(self):
        del self.redis
