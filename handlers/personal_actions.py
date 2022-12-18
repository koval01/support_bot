import traceback

from aiogram import types
from aiogram.types import ChatType, ContentType

import config
from dispatcher import dp
import logging as log
import answers
from group_logic import GroupLogic
from checker import Checker
from redis import Redis
from throttling import rate_limit


@dp.message_handler(commands=["start"])
@rate_limit(30, 'send_hello')
async def send_hello(message: types.Message):
    await message.reply(answers.messages["hello"])


@dp.message_handler(chat_type=[ChatType.PRIVATE], content_types=ContentType.ANY)
@rate_limit(3, 'send_question')
async def send_question(message: types.Message):
    ban = await Redis().get("sprt_ban_%d" % message.from_user.id, "ban")
    if ban:
        await message.answer(answers.messages["banned"])
        return

    ignore = await Redis().get("sprt_ignore_%d" % message.from_user.id, "ignore")
    if ignore:
        return

    text = message.text if message.text else (message.caption if message.caption else "")

    if not Checker.check_bad_words(text):
        await GroupLogic(message).send_to_group
        return

    await Redis().set_key(
        key="sprt_ignore_%d" % message.from_user.id,
        value={"ignore": True}, expire=300)

    await message.reply(answers.messages["bad_words"])


@dp.message_handler(
    lambda message: message.chat.id == config.BOT_GROUP,
    chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], commands=["ban", "unban"]
)
async def ban_user(message: types.Message):
    redis_data = await Redis().get(
        "sprt_gr_%d" % message.reply_to_message.message_id)

    command = message.get_command()[1:]
    ban = True if command == "ban" else False

    await Redis().set_key(
        key="sprt_ban_%d" % redis_data["user_id"],
        value={"ban": ban})

    if ban:
        await message.reply(answers.messages["user_banned"] % redis_data["full_name"])
        return

    await message.reply(answers.messages["user_unbanned"] % redis_data["full_name"])


@dp.message_handler(
    lambda message: message.chat.id == config.BOT_GROUP,
    chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], content_types=ContentType.ANY
)
async def send_answer(message: types.Message):
    try:
        await GroupLogic(message).send_from_group

    except Exception as e:
        log.warning("Send answer error : %s" % e)
        await message.reply(answers.messages["unknown_error"])
