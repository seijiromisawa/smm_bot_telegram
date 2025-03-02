from datetime import datetime
import make_integration.prompts as prompts

class SchedulerData:
    time: datetime
    frequency: str
    interval: int

    def to_dict(self):
        return {
            'time': self.time.isoformat() if self.time else None,
            'frequency': self.frequency,
            "interval": self.interval
        }

class PromptData:
    instructions: str
    user: str

    def to_dict(self):
        return {
            'instructions': self.instructions,
            'user': self.user
        }

class PromptsData:
    post: PromptData = PromptData()
    image: PromptData = PromptData()

    def __init__(self):
        self.post.instructions = prompts.post_assistant_instructions
        self.post.user = prompts.user_prompt(prompts.topic, prompts.tone, "")
        self.image.instructions = prompts.image_assistant_instaructions
        self.image.user = prompts.user_image_prompt(prompts.topic, "")
        
    def to_dict(self):
        return {
            'post': self.post.to_dict(),
            'image': self.image.to_dict()
        }

class Data:
    userId: int
    schedule: SchedulerData = SchedulerData()
    prompts: PromptsData = PromptsData()

    def to_dict(self):
        return {
            'userId': 1,
            'schedule': self.schedule.to_dict(),
            'prompts': self.prompts.to_dict()
        }