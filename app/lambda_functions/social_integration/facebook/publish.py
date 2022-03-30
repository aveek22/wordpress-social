# Import system libraries
import boto3            # To interact with the AWS resources
import requests         # Use REST API calls to interact with services
import logging          # Log messages for debugging
import os               # Get environment variables

from config import Facebook


# Setup Logger
log = logging.getLogger(__name__)

class PublishFacebook:
    """ Publish content to Facebook page. """


    def __init__(self):
        log.debug(f'Initiate Facebook sharing object')
        self._get_facebook_page_details()
        
        self.base_api_url = f"https://graph.facebook.com/v13.0/{self.page_id}/feed"
        log.debug(f'Facebook Share URL set: {self.base_api_url}')

        # self.page_access_token = self._get_access_token_from_parameter_store()
        self.page_access_token = Facebook.PAGE_ACCESS_TOKEN
        log.debug(f'Access Token fetched from Parameter Store')

        log.info(f'PublishFacebook object initiated.')


    def _get_access_token_from_parameter_store(self):
        """ Get the Access Token from AWS Parameter store. """

        # Create the boto client
        try:
            log.debug(f'Creating boto3 client for parameter store.')
            client = boto3.client('ssm')
        except Exception as e:
            log.error(f'Error cretaing SSM client Boto3. {e}')

        # Get the Parameter details from AWS
        try:
            response = client.get_parameter(
                Name = "/social_integration/facebook/page_access_token",
                WithDecryption = False
            )
            log.info(f'Access token obtained from parameter store.')
            # Return the parameter value
            return response['Parameter']['Value']
        except Exception as e:
            log.error(f'Error fetching parameter from Parameter Store. {e}')
            return False


    def _get_facebook_page_details(self):
        """ Get Facebook data from database. """

        self.page_id = "117513500859231"  #@datacloudmag - Facebook Page
        self.user_id = "5448281398515514" #@avikoleum

    
    def post_content(self, payload):
        """ Share the content on Facebook Page. """
        
        url = self.base_api_url

        if(self.page_access_token):
            try:
                log.debug(f'Sharing post to Facebook.')
                response = requests.post(url=url, params=payload)
                log.debug(f'Response Status Code: {response.status_code}')
                log.debug(f'Response Content: {response.json()}')
                
                if(response.status_code == 200):
                    log.info(f'Post shared to Facebook successfully.')
                elif(response.status_code == 400):
                    log.info(f'Unable to share content to Facebook. Invalid Access Token.')
                elif(response.status_code == 422):
                    log.info(f'Unable to share content to Facebook. Duplicate post detected.')
                else:
                    log.warn(f'Unable to share content to Facebook. Run in debug mode to view detailed error.')
            except Exception as e:
                log.error(f'Error in sharing post to Facebook. Error: {e}')

    
    def get_payload(self,event):
        """ Prepare the content payload to share. """
        
        if('facebook' in event):
            """Generate payload only if data available for Facebook"""

            share_text  = event['facebook']['fb_share_text']
            hashtags    = event['facebook']['fb_hashtags']
            share_url   = event['facebook']['fb_share_url']
            
            log.info(f'Preparing content for Facebook.')
            post_content = f"{share_text}\n{hashtags}"

            payload = {
                'message'       : post_content,
                'link'          : share_url,
                'access_token'  : self.page_access_token
            }
            log.info(f'Payload prepared.')
        else:
            payload = False
            log.info(f'Event for Facebook not found. Payload not generated. Application will quit.')

        return payload