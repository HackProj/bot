import json

import requests


API_PATH = "http://localhost:6001/api/"

friend_url = "https://steamcommunity.com/id/IaEbalMeniaSosaliNahui/"
game_url = "https://store.steampowered.com/app/570/Dota_2/"

print(f"{API_PATH}/Users/subscribe?TelegramId={1}&FriendUrl={friend_url}&AppUrl={game_url}")
data = {
  "telegramId": 1,
  "friendUrl": friend_url,
  "appUrl": game_url
}
# ?TelegramId={1}&FriendUrl={friend_url}&AppUrl={game_url}
print(json.dumps(data))
post_data = requests.post(f"{API_PATH}Users/subscribe" , data=json.dumps(data) )
print(post_data.status_code)
print(post_data.url)
print(post_data.text)