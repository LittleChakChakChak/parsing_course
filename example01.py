import requests
import json

# 1 Загрузка репозиториев из git --------------------------------------
"""
user = "LittleChakChakChak"
url = "https://api.github.com/users/" + user + "/repos"
i = 1

response = requests.get(url)
reposts = response.json()

while i < 3:
    if response.status_code == 200:
        list_reposts = []
        print(f'Репозитории пользователя {user}:')
        for rep in reposts:
            list_reposts.append(rep['name'])
            print(f"\t {rep['name']}")
    
        with open('files/file_1.json', 'w') as file_1:
            json.dump(list_reposts, file_1)
    else:
        print(f'Не удачное соединение, код ошибки: {response.status_code}')
        i += 1
"""
# 2 Список песен из vk --------------------------------------

user_id = "51331440"
#method = "users.get"
method = "friends.get"
access_token = "my_little_secret"

url = "https://api.vk.com/method/" + method + "?user_id=" + user_id + "&access_token=" + access_token + "&v=5.81"

response = requests.get(url)
reposts = response.json()
rep = reposts['response']

print('Список друзей')
list_friend = []
for user in rep['items']:
    res = requests.get("https://api.vk.com/method/users.get?user_id=" + str(user) + "&access_token=" + access_token + "&v=5.81")
    list_friend.append(res.json())
    print(res.json())

with open('files/file_2.json', 'w') as file_2:
    json.dump(list_friend, file_2)