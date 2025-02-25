# read env
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import telebot
from bot_commands import BotCommands
from bot_state import BotState
from flow_controller import FlowController
from post_generator import PostGenerator
from image_generator import ImageGenerator

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)
bot_commands = BotCommands(bot)
bot_state = BotState()

flow_controller = FlowController()
openai_key = os.getenv('OPENAI_API_KEY')
post_generator = PostGenerator(openai_key, tone="Профессиональный травел блогер, котороый делиться своим опытом", topic="Путишествия. Травел блог.")
image_generator = ImageGenerator(openai_key)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, text = (
		"Привет! Я бот для создания контента для травел блогеров. Я помогу тебе создать" 
		"посты для твоего блога. Просто загрузи сюда картинку и опиши пост. Если не знаешь "
		"что писать просто задай мне тему для поста и я пришлю тебе варианты для поста.")
	)
	bot_commands.create_commands(message)

@bot.callback_query_handler(func=lambda call: call.data == "timer")
def callback_timer_handler(call):
    bot.send_message(call.message.chat.id, "Установи время и частоту публикаций")
    bot_commands.add_scheduler(call.message)

@bot.callback_query_handler(func=lambda call: call.data in ["set_time", "set_interval", "start_schedule"])
def callback_schedule(call):
    chat_id = call.message.chat.id

    if call.data == "set_time":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, "Введите время для первой публикации в формате ЧЧ:ММ (например, 15:30):")
        bot.register_next_step_handler(msg, process_time_input)
    elif call.data == "set_interval":
        bot.answer_callback_query(call.id)
        msg = bot.send_message(chat_id, "Введите интервал публикаций в минутах (например, 60):")
        bot.register_next_step_handler(msg, process_interval_input)
    elif call.data == "start_schedule":
        bot.answer_callback_query(call.id)
        user_schedule = bot_state.get_schedule()
        if 'time' not in user_schedule or 'frequency' not in user_schedule:
            bot.send_message(chat_id, "Сначала установите и время, и интервал публикаций.")
            return
        scheduled_time = user_schedule['time']
        frequency = user_schedule['frequency']
        #schedule_post(chat_id, scheduled_time, frequency)
        #TODO go to make
        bot.send_message(chat_id, f"Расписание установлено.\nПервая публикация в {scheduled_time.strftime('%H:%M')}, затем каждые {frequency} минут.")

def process_time_input(message):
    chat_id = message.chat.id
    try:
        now = datetime.now()
        input_time = datetime.strptime(message.text, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
        # Если введённое время уже прошло, берем время следующего дня
        if input_time < now:
            input_time += timedelta(days=1)
        schedule_data = bot_state.get_schedule()
        schedule_data['time'] = input_time
        bot.send_message(chat_id, f"Время установлено на {input_time.strftime('%H:%M')}.")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка ввода времени: {e}. Попробуйте снова.")

def process_interval_input(message):
    chat_id = message.chat.id
    try:
        interval = int(message.text)
        schedule_data = bot_state.get_schedule()
        schedule_data['frequency'] = interval
        bot.send_message(chat_id, f"Интервал публикаций установлен на {interval} минут.")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка ввода интервала: {e}. Попробуйте снова.")


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