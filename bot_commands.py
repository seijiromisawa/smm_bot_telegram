from telebot import types
from enum import Enum, auto

import telebot
import telebot.callback_data

class CommandId(Enum):
    NONE = auto()
    POST = auto()
    IMAGE = auto()
    TIME = auto()
    PUBLISH = auto()

class BotCommands:
    bot: telebot = None

    def __init__(self, bot: telebot):
        self.bot = bot

    def create_commands(self, message: str, is_shown_stop: bool = False):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Сгенерировать пост", callback_data="post")
        btn_photo = types.InlineKeyboardButton("Загрузить фото", callback_data="photo")
        markup.add(btn_post, btn_photo)
        if (is_shown_stop == False):
            btn_time = types.InlineKeyboardButton("Задать расписание", callback_data="timer")
            markup.add(btn_time)

        if (is_shown_stop == True):
            btn_stop_time = types.InlineKeyboardButton("Удалить расписание", callback_data="stop_schedule")
            markup.add(btn_stop_time)
        
        self.bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)

    def add_post_commands(self, message: str, showGen: bool = True):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Опубликовать", callback_data="publish")
        if showGen:
            btn_time = types.InlineKeyboardButton("Сгенерировать еще раз", callback_data="post")
            markup.add(btn_post, btn_time)
        else:
            markup.add(btn_post)
        self.bot.send_message(message.chat.id, "Выбери следующий шаг:", reply_markup=markup)
    
    def add_image_commands(self, message: str):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Сгенерировать текст", callback_data="text")
        btn_time = types.InlineKeyboardButton("Задать тему", callback_data="topic")
        markup.add(btn_post, btn_time)
        self.bot.send_message(message.chat.id, "Выбери следующий шаг:", reply_markup=markup)

    def add_text_commands(self, message: str):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Сгенерировать еще раз", callback_data="text")
        btn_preview = types.InlineKeyboardButton("Посмотреть готовый пост", callback_data="preview")
        markup.add( btn_preview, btn_post)
        self.bot.send_message(message.chat.id, "Выбери следующий шаг:", reply_markup=markup)

    def add_preview_commands(self, message: str):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Опубликовать", callback_data="publish")
        btn_text = types.InlineKeyboardButton("Сгенерировать текст еще раз", callback_data="text")
        markup.add(btn_post, btn_text)
        self.bot.send_message(message.chat.id, "Выбери следующий шаг:", reply_markup=markup)

    def add_set_start_time(self, message):
        chat_id = message.chat.id
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_time = types.InlineKeyboardButton("Установить время", callback_data="set_time")
        markup.add(btn_time)
        
        self.bot.send_message(chat_id, "Установи время старта публикации:", reply_markup=markup)

    def add_set_interval(self, message):
        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_interval = types.InlineKeyboardButton("Установить интервал", callback_data="set_interval")
        markup.add(btn_interval)
        self.bot.send_message(chat_id, "Теперь установи частоту публикаций: ", reply_markup=markup)    

    def add_start_scheduler(self, message):
        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_start = types.InlineKeyboardButton("Запустить расписание", callback_data="start_schedule")
        markup.add(btn_start)
        self.bot.send_message(chat_id, "Запускаем? ", reply_markup=markup)   

    def add_new_scheduler(self, message):
        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_time = types.InlineKeyboardButton("Задать расписание", callback_data="timer")
        markup.add(btn_time)
        self.bot.send_message(chat_id, "Задать новое расписание? ", reply_markup=markup)

