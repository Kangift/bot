#### MAIN.PY ####
from aiogram import executor
import bot
from filter import AccessFilter
from loader import dp

dp.filters_factory.bind(AccessFilter)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)



#### FILTER.PY ####
import configparser

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

config = configparser.ConfigParser()
config.read("config.ini")


class AccessFilter(BoundFilter):
    key = "access_filter"

    def __init__(self, access_filter=True):
        self.access_filter = access_filter

    async def check(self, message: types.Message):
        try:
            allowed_ids = list(map(int, config.get("users", "allowed_ids", fallback="").split(",")))
        except ValueError:
            allowed_ids = []

        return (message.from_user.id in allowed_ids) == self.access_filter



#### BOT.PY ####
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db import Database
from loader import dp, bot
from menu import get_settings_keyboard
from states import AddPairStates, ChangeRsiStates
from utils import validate_trading_pair, check_pair_exists

db = Database()


@dp.message_handler(commands=['settings'], state='*', access_filter=True)
async def cmd_start(message: types.Message):
    await message.answer(
        "🔧 Что будем настраивать?",
        reply_markup=get_settings_keyboard()
    )
