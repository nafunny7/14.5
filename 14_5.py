from aiogram import types, Dispatcher, executor, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_def = ReplyKeyboardMarkup(resize_keyboard=True)
but_def1 = KeyboardButton(text="Рассчитать")
but_def2 = KeyboardButton(text="Информация")
kb_def.add(but_def1, but_def2)

kb_inline = InlineKeyboardMarkup(resize_keyboard=True)
but_inline1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
but_inline2 = InlineKeyboardButton(text="Формулы расчёта", callback_data="formulas")
kb_inline.add(but_inline1, but_inline2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer("Введите свой возраст:")
    await call.answer()
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    res = int(int(data["weight"]) * 10 + 6.25 * int(data["growth"]) - 4.92 * int(data["age"]))
    await message.answer(f"Ваша норма калорий в день составляет: {res}")
    await state.finish()


@dp.message_handler(commands=["start"])
async def com_start(message):
    await message.answer("Выберите виджет:", reply_markup=kb_def)


@dp.message_handler(text="Информация")
async def information(message):
    await message.answer("Информация про бота отсутствует🤫")


@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb_inline)


@dp.callback_query_handler(text="formulas")
async def get_formulas(call):
    await call.message.answer("10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161")
    await call.answer()


@dp.callback_query_handler(text="calories")
async def set_age(call):
    await call.message.answer()


@dp.message_handler()
async def all_message(message):
    await message.answer("😊")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
