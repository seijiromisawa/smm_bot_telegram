# read env
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

if __name__ == '__main__':
	bot.polling(none_stop=True)