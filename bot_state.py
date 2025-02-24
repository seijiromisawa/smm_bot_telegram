
from typing import Tuple

class BotState:
  
    GROUP_CHAT_ID = -4617512472
    post = None
    image_url = None

    def set_group_id(self, id: int):
        self.GROUP_CHAT_ID = id

    def get_group_id(self) -> int:
        return self.GROUP_CHAT_ID

    def set_post(self, post: str, image_url: str):
        self.post = post
        self.image_url = image_url

    def get_post(self) -> Tuple[str, str]:
        return self.post, self.image_url
    
    def clear_state(self):
        self.image_url = None
        self.post = None
   
