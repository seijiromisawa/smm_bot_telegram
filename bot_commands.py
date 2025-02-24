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
    bot = None

    def __init__(self, bot: telebot):
        self.bot = bot

    def create_commands(self, message: str):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Сгенерировать пост", callback_data="post")
        btn_time = types.InlineKeyboardButton("Задать время", callback_data="time")
        markup.add(btn_post, btn_time)
        self.bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)
    
    def add_post_commands(self, message: str):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_post = types.InlineKeyboardButton("Опубликовать пост", callback_data="publish")
        btn_time = types.InlineKeyboardButton("Сгенерировать заново", callback_data="post")
        markup.add(btn_post, btn_time)
        self.bot.send_message(message.chat.id, "Что хочешь сделать с постом:", reply_markup=markup)