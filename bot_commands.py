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

    def create_commands(self, message: str):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Сгенерировать пост", callback_data="post")
        btn_time = types.InlineKeyboardButton("Задать время", callback_data="time")
        btn_photo = types.InlineKeyboardButton("Загрузить фото", callback_data="photo")
        markup.add(btn_post, btn_photo, btn_time)
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
        btn_edit = types.InlineKeyboardButton("Отредактировать", callback_data="edit_text")
        btn_preview = types.InlineKeyboardButton("Посмотреть готовый пост", callback_data="preview")
        markup.add( btn_preview, btn_post)
        self.bot.send_message(message.chat.id, "Выбери следующий шаг:", reply_markup=markup)

    def add_preview_commands(self, message: str):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Опубликовать", callback_data="publish")
        btn_text = types.InlineKeyboardButton("Сгенерировать текст еще раз", callback_data="text")
        markup.add(btn_post, btn_text)
        self.bot.send_message(message.chat.id, "Выбери следующий шаг:", reply_markup=markup)

