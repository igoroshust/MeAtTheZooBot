import logging
import time
import os

import telebot
from telebot import types

# Логирование
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = "7583232505:AAF-jNPRMssXuAS5JwDDjauH1KeLYOhjRFw"
bot = telebot.TeleBot(TOKEN)

# Абсолютный путь к папке images
images_folder = os.path.join(os.path.dirname(__file__), 'images')


# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     bot.reply_to(message, "Привет! Я ваш бот в зоопарке!")
#
# @bot.message_handler(commands=['help'])
# def send_help(message):
#     bot.reply_to(message, "Это справка по командам.")
#
# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)
#
# if __name__ == '__main__':
#     bot.polling()

users = {}

TELEGRAM_CHAT_ID = 1277852544

animals = [
    {'bear': 'Малайский медведь'},
    {'puma': 'Пума'},
    {'bushdog': 'Кустарниковая собака'},
    {'penguin': 'Пингвин Гумбольдта'},
    {'parrot': 'Сливоголовый попугай'},
    {'gadwall': 'Серая утка'},
    {'caiman': 'Чёрный кайман'},
    {'iguana': 'Игуана обыкновенная'},
    {'boiga': 'Мангровая змея'},
]

class MessageSendingError(Exception):
    """Ошибка отправки сообщения"""
    pass

FAILURE_TO_SEND_MESSAGE = '{error}, {message}'

@bot.message_handler(commands=['Save data!'])
def send_message(message: users):
    """Отправляет сообщение пользователю в Telegram"""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
    except Exception as error:
        raise MessageSendingError(FAILURE_TO_SEND_MESSAGE.format(
            error=error,
            message=message,
        ))
    logging.info(f'Сообщение "{message}" доставлено')

@bot.message_handler(commands=["Feedback"])
def write_to_support(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Введите своё имя')
    users[chat_id] = {}
    bot.register_next_step_handler(message, save_username)

def save_username(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id]['name'] = name
    bot.send_message(chat_id, f'Хорошо, {name}. Ваше сообщение: ')
    bot.register_next_step_handler(message, save_surname)

def save_surname(message):
    chat_id = message.chat.id
    surname = message.text
    users[chat_id]['surname'] = surname
    keyboard = telebot.types.InlineKeyboardMarkup()
    button_save = telebot.types.InlineKeyboardButton(text="Сохранить", callback_data='save_data')
    button_change = telebot.types.InlineKeyboardButton(text="Изменить",callback_data='change_data')
    keyboard.add(button_save, button_change)
    bot.send_message(chat_id, f'Сохранить данные?', reply_markup=keyboard)


@bot.message_handler(commands=['who_i'])
def who_i(message):
    chat_id = message.chat.id
    name = users[chat_id]['name']
    text = users[chat_id]['text']
    bot.send_message(chat_id, f'Вы: {name} {text}')

@bot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    print(users)
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,text='Данные сохранены!', reply_markup=send_message(users))

@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Изменение данных!')
    write_to_support(message)

def fine_key(z, key, val):
    print(key, val, z)
    time.sleep(2)
    bot.send_message(chat_id=z, text=f"Поздравляем!\n\n Ваше тотемное животное – {val}!")
    bot.send_photo(chat_id=z, photo=open(os.path.join(images_folder, f'{key}.JPG'), 'rb'))
    time.sleep(2)
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Московский зоопарк", url="https://moscowzoo.ru/animals/")
    keyboard.add(url_button)
    bot.send_message(z,
                     "Взять животное под опеку, а также найти информацию о нём, можно найти на сайте:",
                     reply_markup=keyboard)

def inline_key(num):
    """Функция для вывода кнопок"""
    keyboard = types.InlineKeyboardMarkup()
    if num == 1:
        keyboard.add(types.InlineKeyboardButton(text='Малайский медведь', callback_data="bear"))
        keyboard.add(types.InlineKeyboardButton(text='Пума', callback_data="puma"))
        keyboard.add(types.InlineKeyboardButton(text='Кустарниковая собака', callback_data="bushdog"))
    elif num == 2:
        keyboard.add(types.InlineKeyboardButton(text='Пингвин Гумбольдта', callback_data="penguin"))
        keyboard.add(types.InlineKeyboardButton(text='Сливоголовый попугай', callback_data="parrot"))
        keyboard.add(types.InlineKeyboardButton(text='Серая утка', callback_data="gadwall"))
    elif num == 3:
        keyboard.add(types.InlineKeyboardButton(text='Чёрный кайман', callback_data="caiman"))
        keyboard.add(types.InlineKeyboardButton(text='Игуана обыкновенная', callback_data="iguana"))
        keyboard.add(types.InlineKeyboardButton(text='Мангровая змея', callback_data="boiga"))

    return keyboard


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

    for dic in animals:  # выводит список словарей
        for key, val in dic.items():
            bot.send_message(chat_id, f'\n {val}')
            with open(os.path.join(images_folder, f'{key}.JPG'), 'rb') as img:
                bot.send_photo(chat_id, img)
            time.sleep(1)

    # Создаём клавиатуру с кнопкой выбора категории животного
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text='Млекопитающие', callback_data="mammals"))
    key.add(types.InlineKeyboardButton(text='Птицы', callback_data="birds"))
    key.add(types.InlineKeyboardButton(text='Рептилии', callback_data="reptiles"))

    # Отправляем финальное сообщение
    bot.send_message(chat_id, 'Какие животные Вам больше нравятся?', reply_markup=key)
    logging.info(chat_id)


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
        print(c.data)
    elif c.data in ['bear', 'puma', 'bushdog', 'penguin', 'parrot', 'gadwall', 'caiman', 'iguana', 'boiga']:
        for dic in animals:  # выводит список словарей
            for key, val in dic.items():
                # print(f'{key} is {val}')
                if c.data == key:
                    # print(c.data, "*********")
                    bot.answer_callback_query(callback_query_id=c.id, text='! ! ! Ура ! ! !')
                    bot.edit_message_text(
                        chat_id=c.message.chat.id,
                        message_id=c.message.message_id,
                        text=f"123",
                        parse_mode="markdown",
                        reply_markup=fine_key(c.message.chat.id, key, val))
        time.sleep(2)
        bot.send_message(c.message.chat.id, text=f"\nНе устраивает результат? \nПройдите тест ещё раз - /start\
                            \nКонтакт - igoroshust@yandex.ru\nОбратная связь - /Feedback")


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['photo', 'document', 'audio'])
def say_lmao(message: telebot.types.Message):
    bot.reply_to(message, 'Nice meme XDD')


@bot.message_handler(commands=['help', 'information'])
def send_help(message):
    print(message.text)  # получить команду
    text = ('Московский зоопарк — один из старейших зоопарков Европы с уникальной коллекцией животных и профессиональным\
     сообществом. Он выполняет много функций, например, там проводятся разные лекции для посетителей и курсы \
     профессиональной переподготовки для специалистов сферы. \n \n \
О проекте:\n \
«Возьми животное под опеку» («Клуб друзей») — это одна из программ, помогающих зоопарку заботиться о его обитателях. \
Программа позволяет с помощью пожертвования на любую сумму внести свой вклад в развитие зоопарка и сохранение \
биоразнообразия планеты.\n \
\tВзять под опеку можно разных обитателей зоопарка, например, слона, льва, суриката или фламинго. Это возможность помочь \
любимому животному или даже реализовать детскую мечту подружиться с настоящим диким зверем. Почётный статус опекуна \
позволяет круглый год навещать подопечного, быть в курсе событий его жизни и самочувствия.\
переподготовки для специалистов сферы.\n \
\tУчастником программы может стать любой неравнодушный: и ребёнок, и большая корпорация. Поддержка опекунов \
помогает зоопарку улучшать условия для животных и повышать уровень их благополучия.\n \
Контакт - igoroshust@yandex.ru\n Обратная связь - /Feedback \n Подобрать подопечного - /start')
    bot.send_message(message.chat.id, text)


if __name__ == '__main__':
    print('Бот запущен!')

    bot.polling(none_stop=True)