# Introduction to LinkedIn REST API

[LinkedIn](https://www.linkedin.com/) is a popular social media platform that allows users to connect to each other and maintain professional network. You can manage your profile and also create a company profile for your organization. An interesting feature of LinkedIn is the ability to share posts on your feed or on your organization’s feed. You can embed URLs, provide hashtags and emojis and also share images and videos in your post. Although the primary way of sharing content on LinkedIn is by using the web application, you can also do it programmatically using the [REST APIs](https://docs.microsoft.com/en-us/linkedin/) provided by LinkedIn and a programming language of your choice.

## Pre-requisites

In order to proceed further, we need to have the following pre-requisites.

1. **LinkedIn Account** - You need to have a LinkedIn account, if you do not have one, please head over to [https://www.linkedin.com/](https://www.linkedin.com/) and create one.
2. **REST APIs** - Some basic knowledge of using REST APIs.
3. **Python** - General programming knowledge of using python and using REST APIs in python.

Apart from the above-mentioned, I am going to use Jupyter notebooks to create the codebase and make it available using GitHub. At any point in time, you can choose to refer to the official documentation of LinkedIn from Microsoft, however, I will try to explain the process in simple terms.

## Create the LinkedIn Company Page.

Let’s create a company page from your LinkedIn account. You can think of any dummy name for your company to proceed forward. I am going to use my company as “*TheDataScholar*”.

***Step 1***: Open LinkedIn account. Click on **Work** and select **Create a Company Page**. Click on **Company** and enter the details and click on **Create Page**. 

![https://i.imgur.com/bI4wFaj.png](https://i.imgur.com/bI4wFaj.png)

***Step 2***: You need to provide the following details for your company page to be created.

1. **Name** - The name of your company. I am using *TheDataScholar*.
2. **Company** **URL** - The LinkedIn username of your company.
3. **Website** - The website your company is hosted on. I am going to use “*https://thedatascholar.com*”.
4. **Industry** - Select as *Software*.

Once you submit the form, it might take up to 2 business days to get an answer by email. You will then notice the app has been added to your product list.

> 💡 The ***Marketing Developer Platform*** allows you to post content from your company page. Without adding it, you can still post content from your personal LinkedIn profile.

## Get your LinkedIn profile ID

In order to post content from your LinkedIn profile, you need to obtain your profile ID. This can be done by querying the LinkedIn REST API directly.

```python
# Get LinkedIn user ID
url = "https://api.linkedin.com/v2/me"

header = {
    'Authorization' : f'Bearer {access_token}'
}

response = requests.get(url=url, headers=header)
response_json_li_person = response.json()

person_id = response_json_li_person['id']

# https://gist.github.com/aveek22/de44ea0d5a0d322a0ce98c2e26ea4502
```

Notice that I have passed the `access_token` as a bearer token in the authorization header. Also, I have stored the LinkedIn profile ID in a variable called `person_id`.

<script src="https://gist.github.com/aveek22/89b1b6d2423cdeefff59779b30ede7f6.js"></script>

![https://i.imgur.com/LZmWo6s.png](https://i.imgur.com/LZmWo6s.png)

## Conclusion

In this article, we have focused on how to use the LinkedIn REST APIs and share content from a personal profile as well as from an organization’s profile. This is just a beginner level introduction to using the LinkedIn REST APIs. Apart from sharing content, you can also use other [products](https://developer.linkedin.com/product-catalog) to interact with LinkedIn Ads, and Campaign Management Tools.

### Resources

If you want to learn more about LinkedIn REST APIs, I would recommend reading through the following.

- [https://docs.microsoft.com/en-us/linkedin/shared/authentication/authentication](https://docs.microsoft.com/en-us/linkedin/shared/authentication/authentication)
- [https://docs.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/share-api](https://docs.microsoft.com/en-us/linkedin/marketing/integrations/community-management/shares/share-api)
- [https://developer.linkedin.com/product-catalog](https://developer.linkedin.com/product-catalog)