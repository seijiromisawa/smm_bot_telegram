import requests
import json
from make_integration.data import Data 

class Make:
  webhook_url = "https://hook.us1.make.com/bc2bfcuvvq057ttm464snwzt7niz6pcf"
  
  def make_hook(self, data: Data):
    # Convert data to JSON and print it
    json_data = data.to_dict()
    print("JSON Payload:", json.dumps(json_data, indent=4))
    
    # Send the POST request with JSON data
    response = requests.post(self.webhook_url, json=json_data)
    
    # Print the response status and content for debugging
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)
    
    # Check for errors
    if response.status_code != 200:
        print("Error:", response.status_code, response.content)
    else:
        print("Success:", response.status_code, response.content)