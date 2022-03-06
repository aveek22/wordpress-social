# Import system libraries
import boto3            # To interact with the AWS resources
import requests         # Use REST API calls to interact with services
import logging as log   # Log messages for debugging


class ShareLinkedIn:
    """ Publish content to LinkedIn page. """


    def __init__(self):
        self.share_url = "https://api.linkedin.com/v2/shares"
        self.header = self._get_header()


    def _get_header(self):
        """ Prepare the header object with Authorization as Bearer Token. """
        
        # Get the access token from Parameter Store
        access_token = self._get_access_token_from_parameter_store()

        # Prepare the header object
        log.info(f'Setting up the header information.')
        headers = {
            'Authorization' : f'Bearer {access_token}',
            'Content-Type' : 'application/json'
        }

        return headers


    def get_payload(self):
        """ Prepare the content payload to share. """
        
        organization_id = "79377523"
        linkedin_user_id = "urn:li:person:G0CopwI-SP"
        share_text = "Code Refactoring by Aveek Das - Solving the Gilded Rose Refactoring Kata \n#python #sql"
        share_url = "https://datacloudmag.com/solving-the-gilded-rose-refactoring-kata/"
        share_thumbnail = "https://i0.wp.com/datacloudmag.com/wp-content/uploads/2022/02/pexels-photo-169573.jpeg"
        share_title = "Test Share"
        linkedin_user_id.length = 9
        linkedin_user_id.start = 20


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
                        'length' : linkedin_user_id.length,
                        'start' : linkedin_user_id.start
                    }
                ]
            }
        }

        return payload


    def _get_linkedin_user_name_position(username, text):
        """
            Returns the start position and length of username in the text.

            e.g. text = "Learn how to refactor code with Aveek Das."
            start = 32
            length = 9
        """
        pass

    
    def post_content(self):
        """ Share the content on LinkedIn Page. """
        pass

    
    def _get_access_token_from_parameter_store(self):
        """ Get the Access Token from AWS Parameter store. """

        # Create the boto client
        client = boto3.client('ssm')

        # Get the Parameter details from AWS
        response = client.get_parameter(
            Name = "/social_integration/linkedin/access_token",
            WithDecryption = False
        )

        # Return the parameter value
        return response['Parameter']['Value']