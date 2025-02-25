
from typing import Tuple

class BotState:
  
    GROUP_CHAT_ID = -4617512472
    post = None
    image_url = None
    is_topic_await = False
    schedule_data = {} # {'time': datetime, 'frequency': int}

    def set_group_id(self, id: int):
        self.GROUP_CHAT_ID = id

    def get_group_id(self) -> int:
        return self.GROUP_CHAT_ID

    def set_post(self, post: str, image_url: str):
        self.post = post
        self.image_url = image_url

    def set_image(self, image_url: str):
        self.image_url = image_url

    def set_text(self, text: str):
        self.post = text

    def get_post(self) -> Tuple[str, str]:
        return self.post, self.image_url
    
    def clear_state(self):
        self.image_url = None
        self.post = None

    def set_is_topic_await(self, v: bool):
        self.is_topic_await = v

    def get_is_topic_await(self):
        return self.is_topic_await

    def set_schedule(self, schedule):
        self.schedule_data = schedule
    
    def get_schedule(self):
        return self.schedule_data

   


