from os import getenv
import json

BOT_TOKEN = getenv("BOT_TOKEN")
BOT_OWNER = int(getenv("BOT_OWNER"))
BOT_GROUP = int(getenv("BOT_GROUP"))

REDIS_CONNECT = json.loads(getenv("REDIS_CONNECT"))
"""
{
    "host": "127.0.0.1",
    "port": 6379,
    "max_connections": 300
}
"""

