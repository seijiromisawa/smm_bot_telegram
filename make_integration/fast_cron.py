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
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)
    return response.content

  def cron_disable(self, id:int):
    url = f"{self.base_url}cron_disable?token={self.key}&id={id}"
    response = requests.get(url)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

  def cron_enable(self, id:int):
    url = f"{self.base_url}cron_enable?token={self.key}&id={id}"
    response = requests.get(url)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

  def cron_delete(self, id:int):
    url = f"{self.base_url}cron_delete?token={self.key}&id={id}"
    response = requests.get(url)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

