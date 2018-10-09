# reddit-wallpaper-changer
This is a simple script to pull a random image from imgur for a given list of subreddits and set it as the background on a machine running MacOS Mojave. Only a single image is cached at a time. This is only compatible with [python3](https://docs.python-guide.org/starting/install3/osx/).

## How to install
1. Go to [https://api.imgur.com/oauth2/addclient](https://api.imgur.com/oauth2/addclient) to register a new client.

2. Clone this repository
```
git clone https://github.com/curbro/reddit-wallpaper-changer.git
```

3. Update config.json with the client api and client secret provided at imgur client registration.
```
{
  "client_id":"YOUR CLIENT ID",
  "client_secret":"YOUR CLIENT SECRET"
}
```

4. Update subreddits.txt with a comma-delimited list of subreddits from which to pull images.

5. Run the script.
```
python3 ~/wallpaper-changer/driver.py
```

6. Follow the instructions.
