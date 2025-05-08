import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

API_TOKEN = "7789005145:AAEE9g3yuBeMU43XiE8Bnjm5K9lXz8BEBrE"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

user_data = {}

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Привет! Чтобы записаться на марафон, отправь мне своё ФИО.")
    user_data[message.from_user.id] = {"step": "fio"}

@dp.message_handler(commands=['list'])
async def list_participants(message: types.Message):
    try:
        with open("registrations.txt", "r", encoding="utf-8") as f:
            participants = f.readlines()

        if not participants:
            await message.reply("Пока никто не записался.")
        else:
            response = "📋 Список записавшихся:\n" + "".join(participants)
            await message.reply(response)
    except FileNotFoundError:
        await message.reply("Файл с регистрациями ещё не создан.")

@dp.message_handler()
async def handle_message(message: types.Message):
    user_id = message.from_user.id

    if user_id not in user_data:
        await message.reply("Сначала напиши /start.")
        return

    step = user_data[user_id].get("step")

    if step == "fio":
        user_data[user_id]["fio"] = message.text
        user_data[user_id]["step"] = "race"
        await message.reply("Спасибо! Теперь укажи тип забега (5 км, 10 км, марафон):")

    elif step == "race":
        user_data[user_id]["race"] = message.text
        fio = user_data[user_id]["fio"]
        race = user_data[user_id]["race"]

        with open("registrations.txt", "a", encoding="utf-8") as f:
            f.write(f"{fio} — {race}\n")

        await message.reply(f"✅ Ты записан:\n👤 ФИО: {fio}\n🏃 Тип забега: {race}")
        user_data.pop(user_id)

if name == 'main':
    executor.start_polling(dp, skip_updates=True)