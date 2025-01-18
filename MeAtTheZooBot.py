import logging
import os
import time

import telebot
from telebot import types

# Логирование
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = os.getenv("MEATTHEZOOBOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Абсолютный путь к папке images
images_folder = os.path.join(os.path.dirname(__file__), 'images')

users = {}

TELEGRAM_CHAT_ID = 1277852544

animals = [
    {'bear': 'Малайский медведь'},
    {'puma': 'Пума'},
    {'bushdog': 'Кустарниковая собака'},
    {'penguin': 'Пингвин Гумбольта'},
    {'parrot': 'Сливоголовый попугай'},
    {'gadwall': 'Серая утка'},
    {'caiman': 'Чёрный кайман'},
    {'iguana': 'Игуана обыкновенная'},
    {'boiga': 'Мангровая змея'},
]

class MessageSendingError(Exception):
    """Ошибка отправки сообщения."""

    pass


FAILURE_TO_SEND_MESSAGE = '{error}, {message}'


@bot.message_handler(commands=['Save data!'])
def send_message(message: telebot.types.Message):
    """Отправляет сообщение пользователю"""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as error:
        raise MessageSendingError(FAILURE_TO_SEND_MESSAGE.format(
            error=error,
            message=message,
        ))

@bot.message_handler(commands=["start"])
def start(m):
    chat_id = m.chat.id
    text = '\tПриветствуем Вас в Московском зоопарке! \n\
Давайте определим Ваше тотемное животное?'

    # Открываем и отправляем изображение
    with open(os.path.join(images_folder, 'MZoo-logo.JPG'), 'rb') as logo:
        bot.send_photo(chat_id, logo)

    # Создаём клавиатуру с кнопкой "Подобрать"
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text='Подобрать', callback_data='pick_animal'))

    # Отправляем текстовое сообщение
    bot.send_message(chat_id, text, reply_markup=key)

@bot.callback_query_handler(func=lambda call: call.data == 'pick_animal')
def handle_pick_animal(call):
    chat_id = call.message.chat.id
    bot.send_message(chat_id, "Сейчас мы покажем Вам список животных")
    time.sleep(1)

    for dic in animals:  # выводит список словарей
        for key, val in dic.items():
            bot.send_message(chat_id, f'\n {val}')
            with open(os.path.join(images_folder, f'{key}.JPG'), 'rb') as img:
                bot.send_photo(chat_id, img)
            time.sleep(1)

    # Создаём клавиатуру с кнопками выбора категории животного
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text='Млекопитающие', callback_data="mammals"))
    key.add(types.InlineKeyboardButton(text='Птицы', callback_data="birds"))
    key.add(types.InlineKeyboardButton(text='Рептилии', callback_data="reptiles"))

    # Отправляем финальное сообщение
    bot.send_message(chat_id, 'Какие животные Вам больше нравятся?', reply_markup=key)

@bot.callback_query_handler(func=lambda call: True)
def inline(c):
    if c.data == 'mammals':
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Какое млекопитающее Вам понравилось больше?",
            parse_mode="markdown",
            reply_markup=inline_key(1))
    elif c.data == 'birds':
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Какая птица Вам понравилась больше?",
            parse_mode="markdown",
            reply_markup=inline_key(2))
    elif c.data == 'reptiles':
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="Какая рептилия Вам больше понравилась?",
            parse_mode="markdown",
            reply_markup=inline_key(3))
    elif c.data in ['bear', 'puma', 'bushdog', 'penguin', 'parrot', 'gadwall', 'caiman', 'iguana', 'boiga']:
        for dic in animals:  # выводит список словарей
            for key, val in dic.items():
                if c.data == key:
                    bot.answer_callback_query(callback_query_id=c.id, text='Готово!')
                    bot.edit_message_text(
                        chat_id=c.message.chat.id,
                        message_id=c.message.message_id,
                        text=f"123",
                        parse_mode="markdown",
                        reply_markup=fine_key(c.message.chat.id, key, val))


def fine_key(z, key, val):
    print(key, val, z)
    bot.send_message(chat_id=z, text=f"Поздравляем!\n\nВаше тотемное животное – {val}!")
    with open(os.path.join(images_folder, f'{key}.JPG'), 'rb') as img:
        bot.send_photo(chat_id=z, photo=img)
    time.sleep(1)

    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Московский зоопарк", url="https://moscowzoo.ru/animals/")
    keyboard.add(url_button)
    bot.send_message(z,
                     "Взять животное под опеку, а также найти информацию о нём, Вы можете на нашем сайте:",
                     reply_markup=keyboard)

    time.sleep(2)
    bot.send_message(chat_id=z, text=f"Не устраивает результат?\nПройти тест заново: /start\nПолучить информацию о зоопарке: /information \nКонтакт для обратной связи: igoroshust@yandex.ru")

def inline_key(num):
    """Функция для вывода кнопок"""
    keyboard = types.InlineKeyboardMarkup()
    if num == 1:
        keyboard.add(types.InlineKeyboardButton(text='Малайский медведь', callback_data="bear"))
        keyboard.add(types.InlineKeyboardButton(text='Пума', callback_data="puma"))
        keyboard.add(types.InlineKeyboardButton(text='Кустарниковая собака', callback_data="bushdog"))
    elif num == 2:
        keyboard.add(types.InlineKeyboardButton(text='Пингвин Гумбольта', callback_data="penguin"))
        keyboard.add(types.InlineKeyboardButton(text='Сливоголовый попугай', callback_data="parrot"))
        keyboard.add(types.InlineKeyboardButton(text='Серая утка', callback_data="gadwall"))
    elif num == 3:
        keyboard.add(types.InlineKeyboardButton(text='Чёрный кайман', callback_data="caiman"))
        keyboard.add(types.InlineKeyboardButton(text='Игуана обыкновенная', callback_data="iguana"))
        keyboard.add(types.InlineKeyboardButton(text='Мангровая змея', callback_data="boiga"))

    return keyboard


@bot.message_handler(commands=['help', 'information'])
def send_help(message):
    text = ('Московский зоопарк — один из старейших зоопарков Европы с уникальной коллекцией животных и профессиональным\
     сообществом. Он выполняет много функций, например, там проводятся разные лекции для посетителей и курсы \
     профессиональной переподготовки для специалистов сферы. \n \n \
О проекте:\n \
«Возьми животное под опеку» («Клуб друзей») — это одна из программ, помогающих зоопарку заботиться о его обитателях. \
Программа позволяет с помощью пожертвования на любую сумму внести свой вклад в развитие зоопарка и сохранение \
биоразнообразия планеты.\n \
\nВзять под опеку можно разных обитателей зоопарка, например, слона, льва, суриката или фламинго. Это возможность помочь любимому животному или даже реализовать детскую мечту подружиться с настоящим диким зверем. Почётный статус опекуна \
    позволяет круглый год навещать подопечного, быть в курсе событий его жизни и самочувствия.\n \
\nУчастником программы может стать любой неравнодушный: и ребёнок, и большая корпорация. Поддержка опекунов \
    помогает зоопарку улучшать условия для животных и повышать уровень их благополучия.\n \
    \nПодобрать животное: /start\nКонтакт для обратной связи: igoroshust@yandex.ru\n')
    bot.send_message(message.chat.id, text)

# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['photo', 'document', 'audio'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, 'Такой команды нет')

if __name__ == '__main__':
    print('Бот запущен!')
    bot.polling(none_stop=True)