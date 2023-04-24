import os

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

  def get_model_response(self, prompt, num_results=1, max_tokens=64, temperature=0.7, top_k_return=0):
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

if __name__ == "__main__":
  api_key = get_api_key()
  api_endpoint = get_api_endpoint()
  model = ai21_model(api_key, api_endpoint)
  print(f'api_key')
  print(f'api_endpoint')
