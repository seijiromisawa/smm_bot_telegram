from openai import OpenAI
import make_integration.prompts as prompts

class PostGenerator:
    tone = None
    topic = None

    def __init__(self, openai_key: str, tone: str, topic: str):
        self.client = OpenAI(api_key=openai_key)
        self.tone = tone
        self.topic = topic

    def generate_post(self, additional_topic: str = "") -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompts.post_assistant_instructions},
                {"role": "user", "content": prompts.user_prompt(self.topic, self.tone, additional_topic)}
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    
    def generate_post_image_description(self, post_content: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[  
                {"role": "system", "content": prompts.image_assistant_instaructions },
				{"role": "user", "content": prompts.user_image_prompt(self.topic, post_content) }
            ]
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content