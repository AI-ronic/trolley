import os

#import pandas as pd

class ai21_model:

def get_api_key():
  api_key = os.environ.get('api_key')

  if api_key is None:
      print('The environment variable api_key is not set.')
  else:
      print('The value of the environment variable api_key is:', api_key)
  return api_key

if __name__ == "__main__":
  api_key = get_api_key()
  print(f'api_key')
