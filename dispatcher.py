import logging
from aiogram import Bot, Dispatcher
from filters import IsOwnerFilter, IsAdminFilter
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")

# init
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=RedisStorage2(
    host=config.REDIS_CONNECT["host"],
    port=config.REDIS_CONNECT["port"],
    pool_size=config.REDIS_CONNECT["max_connections"],
    prefix="aiogram_sprt_"
))

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
