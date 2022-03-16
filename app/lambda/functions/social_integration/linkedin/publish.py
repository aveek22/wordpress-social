# Import system libraries
import boto3            # To interact with the AWS resources
import requests         # Use REST API calls to interact with services
import logging          # Log messages for debugging


# Setup Logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class PublishLinkedIn:
    """ Publish content to LinkedIn page. """


    def __init__(self):
        log.info(f'Initiate ShareLinkedIn')
        self.share_url = "https://api.linkedin.com/v2/shares"
        self.header = self._get_header()
        self._get_linkedin_profile_details()


    def _get_header(self):
        """ Prepare the header object with Authorization as Bearer Token. """
        
        # Get the access token from Parameter Store
        access_token = self._get_access_token_from_parameter_store()

        # Prepare the header object
        if(access_token):
            log.info(f'Setting up the header information.')
            headers = {
                'Authorization' : f'Bearer {access_token}',
                'Content-Type' : 'application/json'
            }
            return headers
        else:
            return False


    def _get_access_token_from_parameter_store(self):
        """ Get the Access Token from AWS Parameter store. """

        # Create the boto client
        try:
            client = boto3.client('ssm')
        except Exception as e:
            log.error(f'Error cretaing SSM client Boto3. {e}')

        # Get the Parameter details from AWS
        try:
            response = client.get_parameter(
                Name = "/social_integration/linkedin/access_token",
                WithDecryption = False
            )
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
            username_position_length = {
                'position' : text.find(username),
                'length' : len(username)
            }
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
                response = requests.post(url=url, headers=headers, json = payload)
                log.debug(f'Response Status Code: {response.status_code}')
                log.debug(f'Response Content: {response.json()}')
            except Exception as e:
                log.error(f'Error in sending POST request. {e}')

    
    def get_payload(self,event):
        """ Prepare the content payload to share. """
        
        organization_id = self.organization_id
        username = self.username
        linkedin_user_id = self.linkedin_user_id
        
        share_text = event['li_share_text']
        share_title = event['li_share_title']
        share_url = event['li_share_url']
        share_thumbnail = event['li_share_thumbnail']
        
        linkedin_username_position_length = self._get_linkedin_username_position_length(share_text, username)
        linkedin_user_id_start = linkedin_username_position_length['position']
        linkedin_user_id_length = linkedin_username_position_length['length']


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

        return payload