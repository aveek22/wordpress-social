import requests
from config import Wordpress

WORDPRESS_URL = 'https://public-api.wordpress.com/'
AUTH_TOKEN_URL = f'{WORDPRESS_URL}oauth2/token'
POSTS_URL = f'{WORDPRESS_URL}rest/v1.1/sites/{Wordpress.SITE_ID}/posts/{Wordpress.POST_ID}'
auth_message_body = {
    'client_id': Wordpress.CLIENT_ID,
    'client_secret': Wordpress.CLIENT_SECRET,
    'grant_type': Wordpress.GRANT_TYPE,
    'username': Wordpress.USERNAME,
    'password': Wordpress.APP_PASSWORD
}

content = requests.post(AUTH_TOKEN_URL, data=auth_message_body)

response = content.json()

ACCESS_TOKEN = response['access_token']


headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}


posts = requests.get(POSTS_URL, headers=headers)

response = posts.json()

print(response)

