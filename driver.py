#!/usr/local/bin/python3
import json
import requests
import os
import random
import shutil
import subprocess

work_directory = os.path.dirname(__file__)
#auth_url = "https://api.imgur.com/oauth2/authorize"
token_url = "https://api.imgur.com/oauth2/token"
api_url = "https://api.imgur.com/3"


def delete_images():
  image_path = os.getcwd() + '/wallpaper-changer/wallpapers'
  for root, dirs, files in os.walk(image_path):
    for file in files:
        os.remove(os.path.join(root, file))

def save_image(image_url):
  wallpaper_dir = os.getcwd() + '/wallpaper-changer/wallpapers'
  r = requests.get(image_url, stream=True)
  if not os.path.exists(wallpaper_dir):
    os.makedirs(wallpaper_dir)
  image_name = image_url.rsplit('/',1)[-1]
  image_path = wallpaper_dir + '/' + image_name
  image_path_raw = '~' + wallpaper_dir + '/' + image_name
  if r.status_code == 200:
    delete_images()
    with open(image_path, 'wb') as f:
      for chunk in r:
        f.write(chunk)
    
    subprocess.call(["osascript", "-e",
                         'tell application "System Events"\n'
                         'set theDesktops to a reference to every desktop\n'
                         'repeat with aDesktop in theDesktops\n'
                         'set the picture of aDesktop to \"' + image_path + '"\nend repeat\nend tell'])

def get_image(subreddits):
  subreddit = random.choice(subreddits)
  print('Randomly choosing the subreddit: ' + subreddit)
  request_url = api_url + '/gallery/r/' + subreddit
  token = get_token()
  headers = {"Authorization":"Bearer " + token['access_token']}
  response = requests.get(request_url, headers=headers)
  data = response.json()['data']
  selected_data = random.choice([i for i in data if i['is_album'] == False])
  return selected_data['link']

def get_subreddits():
  with open(work_directory + '/subreddits.txt','r') as subreddits_file:
    subreddits = subreddits_file.read().strip().split(',')
    return subreddits

def get_token():
  cache = {}
  config = {}

  # Read config
  with open(work_directory + '/config.json','r') as config_file:
    config = json.load(config_file)
    if os.path.exists(work_directory + '/token.json'):
      # Check for existing token
      with open(work_directory + '/token.json','r') as token_file:
        token_data = json.load(token_file)
        return token_data
    
    # Check for existing pin
    auth_url = "https://api.imgur.com/oauth2/authorize?client_id=" + config['client_id'] + "&response_type=pin"                              
    print("No pin found. Get a new one at: " + auth_url)
    pin = input('Enter your pin here:')

    # Convert pin to tokens
    body = {}
    body['client_id'] = config['client_id']
    body['client_secret'] = config['client_secret']
    body['grant_type'] = 'pin'
    body['pin'] = pin

    token_response = requests.post(url = token_url, data = body)
    response = token_response.json()
    print(response)
    if('data' in response and 'error' in response['data']):
      os.remove(work_directory + '/cache.json')
    else:
      with open(work_directory + '/token.json','w') as token_file:
        json.dump(response,token_file)
        return response
  
if __name__ == "__main__":
  print(get_token())
  subreddits = get_subreddits()
  image_url = get_image(subreddits)
  print(image_url)
  save_image(image_url)
