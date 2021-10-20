import requests
import json

user = "LittleChakChakChak"
url = "https://api.github.com/users/" + user + "/repos"

response = requests.get(url)
reposts = response.json()

list_reposts = []
print(f'Репозитории пользователя {user}:')
for rep in reposts:
    list_reposts.append(rep['name'])
    print(f"\t {rep['name']}")

with open('files/file_1.json', 'w') as file_1:
    json.dump(list_reposts, file_1)