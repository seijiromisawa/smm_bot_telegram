from openai import OpenAI

class PostGenerator:
    tone = None
    topic = None

    def __init__(self, openai_key: str, tone: str, topic: str):
        self.client = OpenAI(api_key=openai_key)
        self.tone = tone
        self.topic = topic

    def generate_post(self) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты высококвалифицированный SMM специалист, который будет помогать в генерации текста для постов с заданной теме и заданным тоном."},
                {"role": "user", "content": f"Сгенерируй пост для соцсетей с темой {self.topic}, используя тон: {self.tone}. Уложись в одно предложение. Не используй темы о политике, религии и экстремизме."}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    
    def generate_post_image_description(self, post_content: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[  
                {"role": "system", "content": "Ты ассистент, который составит промпт для нейросети, которая будет генерировать изображения. Ты должен составлять промпт на заданную тематику."},
				{"role": "user", "content": f"Сгенерируй изображение для соцсетей с темой {self.topic} и учетом теста {post_content}. Не используй текст в изображениях. Только изображение. Используй фотореалистичные изображения. Генерируй только одну картинку."}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content