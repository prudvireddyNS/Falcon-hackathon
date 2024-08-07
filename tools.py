from crewai_tools import ScrapeWebsiteTool
from langchain.tools import tool
import requests
import json
import tempfile
import requests
import os
import tweepy

def post_on_twitter(tweet, consumer_key, consumer_secret, access_token, access_token_secret):

    try:
        client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, 
                        access_token=access_token, access_token_secret=access_token_secret)
    
        tweet = tweet.strip('"')
        res = client.create_tweet(text=tweet)
        return 'Twitter tweet generated and posted to user twitter account successfully'
    except Exception as e:
        return Exception(f"Failed to tweet: {e}")

def generate_image(text):
  
  temp_output_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
  output_image = temp_output_file.name

  response = requests.post(
    f"https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
        "authorization": f"sk-6iUj0Jg2eeKDOpRJuDmCDSvPJdUJ6oP6qrQY3sujqR8h4ycF",
        "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": text,
        "output_format": "png",
        'aspect_ratio': "3:2"
    },
  )

  print(response.status_code)
  if response.status_code == 200:
      with open(output_image, 'wb') as file:
          file.write(response.content)
  else:
      raise Exception(str(response.json()))
  return output_image

def replace_i_with_you(text):
    # Replace different forms of 'I' with 'you'
    text = text.replace(' I ', ' you ')
    text = text.replace(' I.', ' you.')
    text = text.replace(' I,', ' you,')
    text = text.replace(' I\'m ', ' you\'re ')
    text = text.replace(' I\'m', ' you\'re')
    text = text.replace(' I am ', ' you are ')
    text = text.replace(' I am', ' you are')
    
    return text

def scrape_website(website_url):
    """Scrapes all the information from the given website.       
    Args:
        website_url: A url of a company website.
    Returns:
        Scraped information from the given website.
    """
    scrapper = ScrapeWebsiteTool()
    data = scrapper.run(website_url=website_url)
    print(data)
    if not data =='':
        return data
    return 'unable to scrape data'


def escape_text(text):
    chars = ["\\", "|", "{", "}", "@", "[", "]", "(", ")", "<", ">", "#", "*", "_", "~"]
    for char in chars:
        text = text.replace(char, "\\"+char)
    return text

def get_urn(token):
    url = 'https://api.linkedin.com/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        return user_info['sub']
    else:
        raise Exception(f'Failed to fetch user info: {response.status_code}, {response.text}')

def post_on_linkedin(token, title, text_content, image_path=None):
    """
    Posts an article on LinkedIn with an optional image.

    Args:
    token: LinkedIn OAuth token.
    title: LinkedIn post title.
    text_content: LinkedIn post content.
    image_path: file path of the image (optional).
    """
    text_content = escape_text(text_content)
    owner = get_urn(token)

    headers = {
        "LinkedIn-Version": "202401",
        "X-RestLi-Protocol-Version": "2.0.0",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    image_urn = None
    if image_path:
        if image_path.startswith('sandbox'):
            image_path = image_path.split(':')[1]
        image_path = image_path.strip()
        
        # Initialize image upload
        init_url = "https://api.linkedin.com/rest/images?action=initializeUpload"
        init_data = json.dumps({"initializeUploadRequest": {"owner": f'urn:li:person:{owner}'}})
        init_response = requests.post(init_url, headers=headers, data=init_data)
        if init_response.status_code != 200:
            raise Exception(f"Failed to initialize upload: {init_response.text}")

        init_response_data = init_response.json()["value"]
        upload_url = init_response_data["uploadUrl"]
        image_urn = init_response_data["image"]

        # Upload the file
        with open(image_path, "rb") as f:
            upload_response = requests.post(upload_url, files={"file": f})
            if upload_response.status_code not in [200, 201]:
                raise Exception(f"Failed to upload file: {upload_response.text}")

    # Create the post
    post_url = "https://api.linkedin.com/rest/posts"
    post_data = {
        "author": f'urn:li:person:{owner}',
        "commentary": text_content,
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }

    if image_urn:
        post_data["content"] = {
            "media": {
                "title": title,
                "id": image_urn,
            }
        }

    post_data_json = json.dumps(post_data)
    post_response = requests.post(post_url, headers=headers, data=post_data_json)
    if post_response.status_code in [200, 201]:
        return "LinkedIn post generated and posted to user LinkedIn account successfully!"
    else:
        raise Exception(f"Failed to post article: {post_response.text}")
