# Exchange the short lived token by a long one

import requests
from config import Facebook

# https://medium.com/nerd-for-tech/automate-facebook-posts-with-python-and-facebook-graph-api-858a03d2b142
# https://www.youtube.com/watch?v=tfjmW0LEb64

page_id = Facebook.PAGE_ID
user_access_token = Facebook.USER_ACCESS_TOKEN
user_id = Facebook.USER_ID

get_url = f"https://graph.facebook.com/v13.0/{page_id}"

payload = {
    'fields': 'access_token',
    'access_token': user_access_token
}
r = requests.get(get_url, params=payload)

print(r.text)