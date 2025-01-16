import logging
import time

import telebot
from telebot import types

# Логирование
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

TOKEN = "7583232505:AAF-jNPRMssXuAS5JwDDjauH1KeLYOhjRFw"
bot = telebot.TeleBot(TOKEN)


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
    bot.send_message(chat_id, f'Отлично, {name}. Ваше сообщение: ')
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
    bot.send_message(chat_id=z, text=f"Ваше тотемное животное в Московском зоопарке – {val}")
    bot.send_photo(chat_id=z, photo=open(f'images/{key}.JPG', 'rb'))

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
# главное меню
def start(m):
    chat_id = m.chat.id
    text = '\tМосковский зоопарк предлагает - \n\
взять под опеку можно разных обитателей зоопарка, например:'
    bot.send_message(m.chat.id, text)
    time.sleep(3)
    for dic in animals:  # выводит список словарей
        for key, val in dic.items():
            # print(f'{key} is {val}')
            bot.send_message(m.chat.id, f'\n {val}')
            img = open(f'{key}.JPG', 'rb')
            bot.send_photo(m.chat.id, img)
            # bot.send_photo(m.chat_id, photo=open(f'{key}.JPG', 'rb'))
            time.sleep(1)

    img = open(f'MZoo-logo-сircle-preview.JPG', 'rb')
    bot.send_photo(m.chat.id, img)
    key = types.InlineKeyboardMarkup()
    key.add(types.InlineKeyboardButton(text='Мне нравятся млекопитающие животные', callback_data="butt1"))
    key.add(types.InlineKeyboardButton(text='Мне больше нравятся птицы', callback_data="butt2"))
    key.add(types.InlineKeyboardButton(text='Мне больше нравятся рептилий', callback_data="butt3"))
    msg = bot.send_message(m.chat.id, 'Какие животные Вам больше нравятся?', reply_markup=key)
    logging.info(m.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def inline(c):
    if c.data == 'butt1':
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="выбор - *млекопитающие*",
            parse_mode="markdown",
            reply_markup=inline_key(1))
    elif c.data == 'butt2':
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="выбор - *птицы*",
            parse_mode="markdown",
            reply_markup=inline_key(2))
    elif c.data == 'butt3':
        bot.edit_message_text(
            chat_id=c.message.chat.id,
            message_id=c.message.message_id,
            text="выбор - *рептилии*",
            parse_mode="markdown",
            reply_markup=inline_key(3))
        print(c.data)
    elif c.data == 'bear' or 'puma' or 'bushdog' or 'penguin' or 'parrot' or \
            'gadwall' or 'caiman' or 'iguana' or 'boiga':
        for dic in animals:  # выводит список словарей
            for key, val in dic.items():
                # print(f'{key} is {val}')
                if c.data == key:
                    # print(c.data, "*********")
                    bot.answer_callback_query(callback_query_id=c.id, text='! ! ! Ура ! ! !')
                    bot.edit_message_text(
                        chat_id=c.message.chat.id,
                        message_id=c.message.message_id,
                        text=f'Поздравляем!!!\
                         \nВаш подопечный - {val}! \nЕсть сомнения? \nПройдите тест ещё раз - /start\
                        \nКонтакт - igorchan@mail.ru\nОбратная связь - /Feedback',
                        parse_mode="markdown",
                        reply_markup=fine_key(c.message.chat.id, key, val))
        time.sleep(2)
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Московский зоопарк", url="https://moscowzoo.ru/animals/")
        keyboard.add(url_button)
        bot.send_message(TELEGRAM_CHAT_ID, "Информацию о животных можно найти на сайте:", reply_markup=keyboard)


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