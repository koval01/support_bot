from aioredis import Redis

from config import BOT_GROUP
from aiogram import types
from dispatcher import bot
from redis import Redis
import answers


class GroupLogic:

    def __init__(self, message: types.Message) -> None:
        self.message = message
        self.bot = bot
        self.group = BOT_GROUP

    @property
    async def send_to_group(self) -> None:
        ban_data = await Redis().get(
            "sprt_ban_%d" % self.message.from_user.id, "ban")

        if ban_data:
            await self.message.reply(answers.messages["banned"])
            return

        sent_message = await self.bot.forward_message(
            chat_id=self.group,
            from_chat_id=self.message.from_user.id,
            message_id=self.message.message_id)

        await Redis().set_key(
            key="sprt_gr_%d" % sent_message["message_id"],
            value={
                "user_id": self.message.from_user.id,
                "message_id": self.message.message_id,
                "full_name": self.message.from_user.full_name
            },
            expire=604800)

        await self.message.reply(answers.messages["message_sent"])

    @property
    async def send_from_group(self) -> None:
        redis_data = await Redis().get(
            "sprt_gr_%d" % self.message.reply_to_message.message_id)
        print(redis_data)

        text = self.message.text if self.message.text else (
            self.message.caption if self.message.caption else "")

        return await self.bot.copy_message(
            message_id=self.message.message_id,
            chat_id=redis_data["user_id"],
            from_chat_id=self.message.chat.id,
            reply_to_message_id=redis_data["message_id"],
            protect_content=True,
            caption=f"{text}\n\nОтправил: {self.message.from_user.full_name}")
