from apps.bot.config import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis


from apps.bot.handlers import setup_handlers
from apps.bot.middlewares import setup_middlewares

redis = Redis.from_url(config.REDIS_URL)

dp = Dispatcher(storage=RedisStorage(redis=redis))

setup_middlewares(dp)

setup_handlers(dp)
