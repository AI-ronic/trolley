import os
import re

#import pandas as pd
import requests

# requests.post(
#     "https://api.ai21.com/studio/v1/MODEL_TYPE/MODEL_NAME/complete",
#     headers={"Authorization": "Bearer YOUR_API_KEY"},
#     json={
#         "prompt": "YOUR_PROMPT_TEXT",
#         "numResults": 1,
#         "maxTokens": 64,
#         "temperature": 0.7,
#         "topKReturn": 0
#     }
# )


class ai21_model:
  def __init__(self, api_key, api_endpoint, model_type="j2-jumbo-instruct"):
    self.api_endpoint = api_endpoint.format(model_type=model_type)
    self.api_key = api_key
    print(f'Using API endpoint: {self.api_endpoint}')

  def get_raw_model_response(self, prompt, num_results=1, max_tokens=64, temperature=0.7, top_k_return=0):
    response = requests.post(
      self.api_endpoint,
      headers={"Authorization": f"Bearer {self.api_key}"},
      json={
        "prompt": prompt,
        "numResults": num_results,
        "maxTokens": max_tokens,
        "temperature": temperature,
        "topKReturn": top_k_return
      }
    )
    return response['completions'][0]['data']['text']

  @staticmethod
  def parse_raw_response(raw_response):
    interested_in = ['1', '2']
    # Find all occurrences of 1 and 2 in raw_response
    for answer in interested_in:
    matches = re.findall("[12]", raw_response)

    # Count the number of occurrences of 1 and 2
    count_1 = matches.count("1")
    count_2 = matches.count("2")

    print(f"Number of 1's: {count_1}")
    print(f"Number of 2's: {count_2}")



  def get_model_response(self, prompt, num_results=1, max_tokens=64, temperature=0.7, top_k_return=0):
    raw_response = self.get_raw_model_response(prompt, num_results, max_tokens, temperature, top_k_return)
    response = parse_raw_response(raw_response)
    return response.json()
  


# Helper functions
def get_api_key():
  api_key = os.environ.get('api_key')

  if api_key is None:
      raise RuntimeError('The environment variable api_key is not set.')
  else:
      print('The value of the environment variable api_key is:', api_key)
  return api_key

def get_api_endpoint(model_type="j2-jumbo-instruct"):
  api_endpoint = os.environ.get(f'api_endpoint')

  if api_endpoint is None:
      raise RuntimeError('The environment variable api_endpoint is not set.')
  else:
      print('The value of the environment variable api_endpoint is:', api_endpoint)
  return api_endpoint

def run():
  api_key = get_api_key()
  api_endpoint = get_api_endpoint()
  model = ai21_model(api_key, api_endpoint)
  print(f'api_key')
  print(f'api_endpoint')
  return model

if __name__ == "__main__":
  run()