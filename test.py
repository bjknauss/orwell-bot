import asyncio
import aioredis
from dynaconf import settings

async def main():
    redis: aioredis.Redis = await aioredis.create_redis((settings.REDIS.host, settings.REDIS.port), db=0)

    results = await redis.zrevrangebyscore('user-act:513812064557334538', withscores=True, count=300, offset=0)

    print(results)

async def test(redis: aioredis.Redis):
    redis.


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
