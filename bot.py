# read env
from dotenv import load_dotenv
import os
from flows.scheduler_flow import SchedulerFlow
from make_integration.data import Data
import telebot
from bot_commands import BotCommands
from bot_state import BotState
from make_integration.make import Make
from cheduler.fast_cron import FastCron
from generators.post_generator import PostGenerator
from generators.image_generator import ImageGenerator
import make_integration.prompts as prompts

 
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
bot_commands = BotCommands(bot)
bot_state = BotState()
make = Make()
fast_cron_key = os.getenv('FAST_CRON_KEY')
fast_cron = FastCron(fast_cron_key)
scheduler_flow = SchedulerFlow(bot, fast_cron, Data(), make.webhook_url, bot_commands)

openai_key = os.getenv('OPENAI_API_KEY')
post_generator = PostGenerator(openai_key, prompts.tone, prompts.topic)
image_generator = ImageGenerator(openai_key)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, text = (
        "Привет! Я бот для создания контента для травел блогеров. Я помогу тебе создать " 
        "посты для твоего блога. Просто загрузи сюда картинку и опиши пост. Если не знаешь "
        "что писать, просто нажми 'сгенерировать пост' и я пришлю тебе вариант готового поста.")
    )
    count = scheduler_flow.get_flow_count()
    show_stop_timer = False
    if (count > 0):
        show_stop_timer = True

    bot_commands.create_commands(message, show_stop_timer)

@bot.callback_query_handler(func=lambda call: call.data == "timer")
def callback_timer_handler(call):
    bot_commands.add_set_start_time(call.message)

@bot.callback_query_handler(func=lambda call: call.data in ["set_time", "set_interval", "start_schedule"])
def callback_schedule(call):
    chat_id = call.message.chat.id
    data = Data()
    scheduler_flow.setup_flow(call, chat_id, data.schedule)

@bot.callback_query_handler(func=lambda call: call.data == "stop_schedule")
def callback_schedule(call):
    scheduler_flow.remove_flow(call)

@bot.callback_query_handler(func=lambda call: call.data == "post")
def callback_post_handler(call):
    bot.send_message(call.message.chat.id, "Генерирую, пожалуйста подождите...")
    bot.answer_callback_query(call.id)
    # To tread?
    post = post_generator.generate_post()
    imagePrompt = post_generator.generate_post_image_description(post)
    image_url = image_generator.generate_image(imagePrompt)
    bot.send_photo(call.message.chat.id, image_url, post)
    bot_state.set_post(post, image_url)
    bot_commands.add_post_commands(call.message)
		
@bot.callback_query_handler(func=lambda call: call.data == "text")
def callback_post_handler(call):
    bot.send_message(call.message.chat.id, "Генерирую текст, пожалуйста подождите...")
    bot.answer_callback_query(call.id)
    # To tread?
    text = post_generator.generate_post()
    bot.send_message(call.message.chat.id, text)
    bot_state.set_text(text)
    bot_commands.add_text_commands(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "preview")
def callback_preview_handler(call):
    text, image = bot_state.get_post()
    bot.send_photo(call.message.chat.id, image, text)
    bot_commands.add_preview_commands(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "publish")
def callback_publish_handler(call):
    bot.send_message(call.message.chat.id, "Публикую...")
    post, image = bot_state.get_post()
    if post is None: 
        bot.send_message(call.message.chat.id, "Сообщение не может быть отправлено в группу из за того, что пост не сохранен.")
        bot.answer_callback_query(call.id)
        return
    
    group_id = bot_state.get_group_id()
    bot.send_photo(group_id, image, post)
    bot.send_message(call.message.chat.id, "Сообщение отправлено в группу.")
    bot.answer_callback_query(call.id)
    bot_state.clear_state()

@bot.callback_query_handler(func=lambda call: call.data == "photo")
def callback_photo_handler(call):
    bot.send_message(call.message.chat.id, "Загрузи свои фото")
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data == "topic")
def callback_topic_handler(call):
    bot.send_message(call.message.chat.id, "Задай тему и я сгенерирую тебе пост")
    bot_state.set_is_topic_await(True)
    bot.answer_callback_query(call.id)
		
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Берём последний элемент для максимального качества
    file_id = message.photo[-1].file_id
    bot_state.set_image(file_id)
    bot_commands.add_image_commands(message)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    is_topic_await = bot_state.get_is_topic_await()
    if is_topic_await == False:
         return
         
    bot_state.set_is_topic_await(False)
    bot.send_message(message.chat.id, "Генерирую текст, пожалуйста подождите...")

    text = post_generator.generate_post(additional_topic=message) #todo может добавить фильтрацию?
    bot.send_message(message.chat.id, text)
    bot_state.set_text(text)
    bot_commands.add_text_commands(message)  

if __name__ == '__main__':
	bot.polling(none_stop=True)