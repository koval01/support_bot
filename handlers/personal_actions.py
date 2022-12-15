from aiogram import types
from aiogram.types import ChatType, ContentType

from dispatcher import dp
import config
import answers
from group_logic import GroupLogic
from checker import Checker
from throttling import rate_limit


@dp.message_handler(commands=["start"])
@rate_limit(30, 'send_hello')
async def send_hello(message: types.Message):
    await message.reply(answers.messages["hello"])


@dp.message_handler(chat_type=[ChatType.PRIVATE], content_types=ContentType.TEXT)
@rate_limit(10, 'send_question')
async def send_question(message: types.Message):

    if not Checker.check_bad_words(message.text):
        await message.reply(answers.answer % (answers.messages["message_sent"], "Система"))
        await GroupLogic(message).send_to_group
        return

    await message.reply(answers.answer % (answers.messages["bad_words"], "Система"))


@dp.message_handler(chat_type=[ChatType.SUPERGROUP, ChatType.GROUP], content_types=ContentType.TEXT)
async def send_answer(message: types.Message):
    await GroupLogic(message).send_from_group


@dp.message_handler(content_types=ContentType.ANY)
async def error_handler(message: types.Message):
    await message.reply(answers.messages["unsupported_message"])
