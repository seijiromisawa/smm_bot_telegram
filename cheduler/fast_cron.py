from datetime import datetime
import requests
import json

class FastCron:

  base_url = "https://app.fastcron.com/api/v1/"
  key = None

  def __init__(self, key: str):
    self.key = key

  def get_cron_list(self):
    url = f"{self.base_url}cron_list?token={self.key}"
    response = requests.get(url)
    return self.__decode_response(response)

  def cron_create(self, callback: str, start_time: datetime, expression: str, data: dict = {}):
    url = f"{self.base_url}cron_add"
    
    # data для повторяющейся задачи крона
    interval_post_data = {
      "token": self.key,
      "expression": expression,
      "url": callback,
      "postData": json.dumps(data),
      "httpMethod": "POST"
    }

    # Создание крон задачи, которая запуститься 1 раз создаст крон задачу с интервалом 
    time_expression = f"{start_time.minute} {start_time.hour} {start_time.day - 1 } {start_time.month} *"
    # data на создание одноразовой задачи.
    json_data = json.dumps(interval_post_data)
    time_data = {
      "token": self.key,
      "expression": time_expression,
      "url": url,
      "postData": json_data,
      "httpMethod": "POST"
    }

    response = requests.post(url, json=time_data)
    return self.__decode_response(response)


  def cron_disable(self, id:int):
    url = f"{self.base_url}cron_disable?token={self.key}&id={id}"
    response = requests.get(url)
    return self.__decode_response(response)

  def cron_enable(self, id:int):
    url = f"{self.base_url}cron_enable?token={self.key}&id={id}"
    response = requests.get(url)
    return self.__decode_response(response)

  def cron_delete(self, id:int):
    url = f"{self.base_url}cron_delete?token={self.key}&id={id}"
    response = requests.get(url)
    return self.__decode_response(response)
  
  def __decode_response(self, response: requests.Response) -> str:
    decoded = response.content.decode()
    data = json.loads(decoded)
    return data
