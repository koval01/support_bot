from aioredis import Redis

from config import BOT_GROUP
from aiogram import types
from dispatcher import bot
from redis import Redis
import json
import answers


class GroupLogic:

    def __init__(self, message: types.Message) -> None:
        self.message = message
        self.bot = bot
        self.group = BOT_GROUP

    @property
    async def send_to_group(self) -> Redis:
        sent_message = await self.bot.forward_message(
            chat_id=self.group,
            from_chat_id=self.message.from_user.id,
            message_id=self.message.message_id
        )

        return await Redis().set_key(
            key="sprt_gr_%d" % sent_message["message_id"],
            value=json.dumps({
                "user_id": self.message.from_user.id,
                "message_id": self.message.message_id
            }),

            expire=604800
        )

    @property
    async def send_from_group(self) -> None:
        r = await Redis().get_key(
            "sprt_gr_%d" % self.message.reply_to_message.message_id
        )
        redis_data = json.loads(bytes(r).decode())

        return await self.bot.send_message(
            chat_id=redis_data["user_id"],
            reply_to_message_id=redis_data["message_id"],

            text=answers.answer % (
                self.message.text,
                self.message.from_user.full_name
            )
        )
