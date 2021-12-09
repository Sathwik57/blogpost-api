import requests
import pprint

x = requests.get('http://127.0.0.1:8000/api/users/')

sat_headers = {'Authorization': 'Token c388a63aee146155b43651d7bbf2f33342036b7b'}
test_headers = {'Authorization': 'Token 8f63bc6fe0dea7b269483b81c470cbf25dabadff'}
body = {'username':'test2user' ,'password': 'V!cky1121'}

# z = requests.get('http://127.0.0.1:8000/api/blog/9a4eb6d4-f494-4504-a2e1-110fd293e27d/reviews/',headers = headers)

y = requests.get(
    'http://127.0.0.1:8000/api/users/profile/513fdaa0-4040-4bf4-b0ca-acc92f75f902e/update/',
    headers=sat_headers
)

pprint.pprint(y.text )

print(y.status_code)