import requests
from config import Facebook

# https://medium.com/nerd-for-tech/automate-facebook-posts-with-python-and-facebook-graph-api-858a03d2b142
# https://www.youtube.com/watch?v=tfjmW0LEb64

page_id = Facebook.PAGE_ID
access_token = Facebook.ACCESS_TOKEN
user_id = Facebook.USER_ID


text = f"Solving the Gilded Rose Refactoring Kata by @[{user_id}]."
url = "https://datacloudmag.com/solving-the-gilded-rose-refactoring-kata/"
hashtags = "#python #refactoring"


post_content = f"{text} \n\n{hashtags}"



post_url = f"https://graph.facebook.com/v13.0/{page_id}/feed"


payload = {
    'message': post_content,
    'access_token': access_token,
    'link': url
}
r = requests.post(post_url, params=payload)

print(r.text)