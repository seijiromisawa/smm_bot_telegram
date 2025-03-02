
tone = "Профессиональный травел блогер, котороый делиться своим опытом"
topic = "Путишествия. Травел блог. Советы для путешественников"

post_assistant_instructions = """
 	Ты высококвалифицированный SMM специалист, который будет помогать в генерации текста для постов с заданной теме и заданным тоном.
	"""

image_assistant_instaructions = """
	Цель:
		Ты невероятно крутой промпт-игженер. Ты умеешь составлять промпты для нейросети, которая умеет генерировать 
		изображения.
	Действие:
  		Ты должен составлять промпт на заданную тематику.
	"""

def user_prompt(topic: str, tone: str, additional_topic: str):
  prompt = f"""Сгенерируй пост для соцсетей с темой {topic} и 
  		используй эти уточнения {additional_topic}, используя тон: {tone}. 
      Уложись в 2 предложения. Не используй темы о политике, религии и экстремизме.
    """
  return prompt

def user_image_prompt(topic: str, post_content: str):
    prompt = f"""Сгенерируй изображение для соцсетей с темой {topic} и учетом теста {post_content}. 
  		Не используй текст в изображениях. Только изображение. Используй фотореалистичные изображения. 
      Генерируй только одну картинку.
    """
    return prompt