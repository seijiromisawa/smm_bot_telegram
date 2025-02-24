from dotenv import load_dotenv
import os

from bot_commands import CommandId
from post_generator import PostGenerator

class FlowController:
  command_id = CommandId.NONE
  post_generator = None

  def init(self):
    load_dotenv() # Load the .env file
    openai_key = os.getenv('OPENAI_API_KEY')
    self.post_generator = PostGenerator(openai_key, tone="Профессиональный травел блогер, котороый делиться своим опытом", topic="Путишествия. Травел блог.")

  def set_command(self, command_id):
    self.command_id = command_id

  def get_command_id(self) -> CommandId:
    return self.command_id
  
  def next_step(self, command_id) -> CommandId:
    return CommandId.NONE

  def generate_post(self) -> str:
    return self.post_generator.generate_post()
