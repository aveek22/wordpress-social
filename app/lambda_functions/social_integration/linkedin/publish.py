# Import system libraries
import boto3            # To interact with the AWS resources
import requests         # Use REST API calls to interact with services
import logging          # Log messages for debugging
import os               # Get environment variables


# Setup Logger
log = logging.getLogger(__name__)

class PublishLinkedIn:
    """ Publish content to LinkedIn page. """


    def __init__(self):
        log.debug(f'Initiate ShareLinkedIn')
        
        self.share_url = "https://api.linkedin.com/v2/shares"
        log.debug(f'LinkedIn Share URL set: {self.share_url}')

        self.header = self._get_header()
        log.debug(f'Header Set: {self.header}')

        self._get_linkedin_profile_details()
        log.debug(f'LinkedIn profile details fetched.')

        log.info(f'PublishLinkedIn object initiated.')


    def _get_header(self):
        """ Prepare the header object with Authorization as Bearer Token. """
        
        # Get the access token from Parameter Store
        log.debug(f'Get access token from AWS parameter store.')
        access_token = self._get_access_token_from_parameter_store()
        log.debug(f'Access token fetched.')

        # Prepare the header object
        if(access_token):
            log.debug(f'Setting up the header information.')
            headers = {
                'Authorization' : f'Bearer {access_token}',
                'Content-Type' : 'application/json'
            }
            log.info(f'Header information set.')
            return headers
        else:
            log.warn(f'Header information not set. Application may not work as expected.')
            return False


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
                Name = "/social_integration/linkedin/access_token",
                WithDecryption = False
            )
            log.info(f'Access token obtained from parameter store.')
            # Return the parameter value
            return response['Parameter']['Value']
        except Exception as e:
            log.error(f'Error fetching parameter from Parameter Store. {e}')
            return False


    def _get_linkedin_username_position_length(self, text, username):
        """
            Returns the start position and length of username in the text.

            e.g. text = "Learn how to refactor code with Aveek Das."
            start = 32
            length = 9
        """
        try:
            log.debug(f'Get LinkedIn username length and position.')
            username_position_length = {
                'position' : text.find(username),
                'length' : len(username)
            }
            log.info(f'LinkedIn username found at {username_position_length}.')
            return username_position_length
        except Exception as e:
            log.error(f'Error in getting username position and length. {e}')


    def _get_linkedin_profile_details(self):
        """ Get LinkedIn data from database. """

        self.organization_id = "79377523"
        self.username = "Aveek Das"
        self.linkedin_user_id = "urn:li:person:G0CopwI-SP"

    
    def post_content(self, payload):
        """ Share the content on LinkedIn Page. """
        
        url = self.share_url
        headers = self.header

        if(headers):
            try:
                log.debug(f'Sharing post to LinkedIn.')
                response = requests.post(url=url, headers=headers, json = payload)
                log.debug(f'Response Status Code: {response.status_code}')
                log.debug(f'Response Content: {response.json()}')
                
                if(response.status_code == 201):
                    log.info(f'Post shared to LinkedIn successfully.')
                elif(response.status_code == 422):
                    log.info(f'Unable to share content to LinkedIn. Duplicate post detected.')
                else:
                    log.warn(f'Unable to share content to LinkedIn. Run in debug mode to view detailed error.')
            except Exception as e:
                log.error(f'Error in sharing post to LinkedIn. Error: {e}')

    
    def get_payload(self,event):
        """ Prepare the content payload to share. """
        
        organization_id = self.organization_id
        username = self.username
        linkedin_user_id = self.linkedin_user_id
        
        if('linkedin' in event):
            """Generate payload only if data available for linkedin"""

            share_text = event['linkedin']['li_share_text']
            share_title = event['linkedin']['li_share_title']
            share_url = event['linkedin']['li_share_url']
            share_thumbnail = event['linkedin']['li_share_thumbnail']
            
            linkedin_username_position_length = self._get_linkedin_username_position_length(share_text, username)
            linkedin_user_id_start = linkedin_username_position_length['position']
            linkedin_user_id_length = linkedin_username_position_length['length']

            log.info(f'Preparing payload for LinkedIn.')

            payload = {
                "content": {
                    "contentEntities": [
                        {
                            "entityLocation": share_url,
                            "thumbnails": [
                                {
                                    "resolvedUrl": share_thumbnail
                                }
                            ]
                        }
                    ],
                    "title": share_title
                },
                'distribution': {
                    'linkedInDistributionTarget': {}
                },
                'owner': f'urn:li:organization:{organization_id}',
                'text': {
                    'text': share_text,
                    'annotations': [
                        {
                            'entity' : linkedin_user_id,
                            'length' : linkedin_user_id_length,
                            'start' : linkedin_user_id_start
                        }
                    ]
                }
            }
            log.info(f'Payload prepared.')
        else:
            payload = False
            log.info(f'Event for LinkedIn not found. Payload not generated. Application will quit.')

        return payload