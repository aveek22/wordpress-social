# Import system libraries
from enum import Flag
import profile
import boto3            # To interact with the AWS resources
import requests         # Use REST API calls to interact with services
import logging          # Log messages for debugging
import os               # Get environment variables


# Setup Logger
log = logging.getLogger(__name__)

class PublishInstagram:
    """ Publish content to Instagram page. """


    def __init__(self):
        log.debug(f'Initiate PublishInstagram')
        
        self._get_instagram_profile_details()
        log.debug(f'LinkedIn profile details fetched.')
        
        base_api_url = f"https://graph.facebook.com/v13.0/{self.business_account_id}"
        self.media_api_url          = f"{base_api_url}/media"
        self.media_publish_api_url  = f"{base_api_url}/media_publish"
        log.debug(f'API URLs set: {self.media_publish_api_url}')

        self.access_token = self._get_access_token()
        log.debug(f'Access Token obtained from short-lived user access token.')

        log.info(f'PublishInstagram object initiated.')


    def _get_access_token(self):
        """ Prepare Access Token from short-lived User Access Token """
        
        # Get the user access token from Parameter Store
        log.debug(f'Get user access token from AWS parameter store.')
        user_access_token = self._get_user_access_token_from_parameter_store()
        log.debug(f'User Access token fetched.')

        # Prepare the Access Token
        if(user_access_token):
            log.debug(f'Preparing Access Token from short-lived User Access Token.')
            oauth_url = f"https://graph.facebook.com/v13.0/oauth/access_token"
            oauth_params = {
                'grant_type' : 'fb_exchange_token',
                'client_id' : self.app_id,
                'client_secret' : self.app_secret,
                'fb_exchange_token': user_access_token
            }
            try:
                response = requests.post(url=oauth_url, params=oauth_params)
                response_json = response.json()
                access_token = response_json['access_token']
            except Exception as e:
                access_token = False
                log.error(f"Unable to prepare access token. Error: {e}")
            
            log.info(f'Access Token obtained from User Access Token.')
            return access_token
        else:
            log.warn(f'Access Token not set. Application will quit.')
            return False


    def _get_user_access_token_from_parameter_store(self):
        """ Get the User Access Token from AWS Parameter store. """

        # Create the boto client
        try:
            log.debug(f'Creating boto3 client for parameter store.')
            # session = boto3.Session(profile_name="aveek2021")
            client = boto3.client('ssm')
        except Exception as e:
            log.error(f'Error cretaing SSM client Boto3. {e}')

        # Get the Parameter details from AWS
        try:
            response = client.get_parameter(
                Name = "/social_integration/facebook/user_access_token",
                WithDecryption = False
            )
            log.info(f'User Access token obtained from parameter store.')
            # Return the parameter value
            return response['Parameter']['Value']
        except Exception as e:
            log.error(f'Error fetching parameter from Parameter Store. {e}')
            return False


    def _get_instagram_profile_details(self):
        """ Get LinkedIn data from database. """

        self.app_id                 = ""
        self.app_secret             = ""
        self.business_account_id    = "17841451612144935"


    def _upload_media(self, payload):
        """Upload media to Instagram"""

        media_id = False

        if(self.access_token):
            try:
                log.debug(f'Uploading media to Instagram.')
                response_media = requests.post(url=self.media_api_url, params = payload)
                log.debug(f'Response Status Code: {response_media.status_code}')
                
                if(response_media.status_code == 200):
                    response_media_json = response_media.json()
                    media_id = response_media_json['id']
                    log.debug(f'Response Media ID: {media_id}')
                else:
                    log.warn(f'Unable to upload media to Instagram. Run in debug mode to view detailed error.')
            except Exception as e:
                log.error(f'Error in uploading media to Instagram. Error: {e}')

        return media_id


    def _publish_media(self):
        """Publish media to Instagram"""

        if(self.media_id):
            try:
                log.debug(f'Publishing media to Instagram.')
                publish_media_payload = {
                    'creation_id' : f"{self.media_id}",
                    'access_token': f'{self.access_token}'
                }
                response_media = requests.post(url=self.media_publish_api_url, params = publish_media_payload)
                log.debug(f'Response Status Code: {response_media.status_code}')
                
                if(response_media.status_code == 200):
                    log.info(f'Content shared on Instagram successfully.')
                else:
                    log.warn(f'Unable to upload media to Instagram. Run in debug mode to view detailed error.')
            except Exception as e:
                log.error(f'Error in uploading media to Instagram. Error: {e}')

    
    def post_content(self, payload):
        """ Share the content on LinkedIn Page. """
        
        log.debug(f"Uploading media to Instagram")
        self.media_id = self._upload_media(payload)

        log.debug(f"Publish media on Instagram.")
        self._publish_media()

    
    def get_payload(self,event):
        """ Prepare the content payload to share. """
        
        if('instagram' in event):
            """Generate payload only if data available for instagram"""

            image_url   = event['instagram']['ig_image_url']
            caption     = event['instagram']['ig_caption']
            hashtags    = event['instagram']['ig_hashtags']
            share_url   = event['instagram']['ig_share_url']
            
            log.info(f'Preparing payload for Instagram.')

            payload = {
                'image_url' : image_url,
                'caption' : f"{caption} \n {hashtags} \n {share_url}",
                'access_token': f'{self.access_token}'
            }
            log.info(f'Payload prepared.')
        else:
            payload = False
            log.info(f'Event for Instagram not found. Payload not generated. Application will quit.')

        return payload