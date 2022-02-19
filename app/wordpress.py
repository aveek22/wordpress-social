import requests
from config import Config

WORDPRESS_URL = 'https://public-api.wordpress.com/'
AUTH_TOKEN_URL = f'{WORDPRESS_URL}oauth2/token'


POSTS_URL = f'{WORDPRESS_URL}rest/v1.1/sites/{Config.SITE_ID}/posts/{Config.POST_ID}'


auth_message_body = {
    'client_id' : Config.CLIENT_ID,
    'client_secret' : Config.CLIENT_SECRET,
    'grant_type' : Config.GRANT_TYPE,
    'username' : Config.USERNAME,
    'password' : Config.APP_PASSWORD
}

content = requests.post(AUTH_TOKEN_URL, data=auth_message_body)

response = content.json()

ACCESS_TOKEN = response['access_token']


headers = {
    'Authorization' : f'Bearer {ACCESS_TOKEN}'
}

posts = requests.get(POSTS_URL, headers=headers)

response = posts.json()

print(response)





