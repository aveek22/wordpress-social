# Import system libraries
import boto3            # To interact with the AWS resources
import tweepy           # Use Tweepy to interact with Twitter
import logging          # Log messages for debugging
import os               # Get environment variables


# Import custom libraries
from credentials import TwitterCredentials

# Setup Logger
log = logging.getLogger(__name__)

class PublishTwitter:
    """ Publish content to Twitter profile. """


    def __init__(self):
        """Initiate the PublishTwitter object."""
        log.debug(f'Initiate PublishTwitter object.')
        
        self.tweepy_client = self._create_tweepy_client()
        log.info(f'PublishLinkedIn object initiated.')


    def _create_tweepy_client(self):
        """ Create the Tweepy Client object. """
        
        # Get the twitter credentials from Parameter Store
        log.debug(f'Get twitter credentials from AWS parameter store.')
        twitter_credentials = self._get_credentials_from_parameter_store()
        log.debug(f'Twitter credentials fetched.')

        # Prepare the twitter client
        if(twitter_credentials):
            
            try:
                log.debug(f'Creating Tweepy Client.')
                client = tweepy.Client(
                    consumer_key        = twitter_credentials.CONSUMER_KEY,
                    consumer_secret     = twitter_credentials.CONSUMER_KEY_SECRET,
                    access_token        = twitter_credentials.ACCESS_TOKEN,
                    access_token_secret = twitter_credentials.ACCESS_TOKEN_SECRET
                )
                log.debug(f'Tweepy Client created.')
            except Exception as e:
                log.error(f'Unable to create Tweepy client. Error: {e}')
                client = False
            
        else:
            client = False
            log.warning(f'Tweepy client not created. Application will quit..')

        return client
            

    def _get_credentials_from_parameter_store(self):
        """ Get the Twitter Credentials. """

        # Create the credentials object
        twitter_credentials = TwitterCredentials()

        # Fetch Twitter credentials from parameter store
        twitter_credentials.get_twitter_credentials_from_parameter_store()

        return twitter_credentials
            
  
    def get_payload_from_event(self, event):
        """Prepare payload text from event."""

        try:
            log.debug(f'Preparing payload from event.')

            share_text  = event['twitter']['tw_share_text']
            hashtags    = event['twitter']['tw_hashtags']
            share_url   = event['twitter']['tw_share_url']

            payload = f"{share_text}\n{hashtags}\n{share_url}"
            log.info(f'Tweet text prepared. {payload}')
        except Exception as e:
            payload = False
            log.error(f'Unable to prepare tweet text. Error: {e}')

        return payload
    
    
    def post_content(self, payload):
        """ Share the content on Twitter Profile. """

        # Set control vaariables.
        client = False
        
        client = self.tweepy_client

        if(payload):
            try:
                log.debug(f'Sharing post to Twitter.')
                response = client.create_tweet(text=payload)
                log.debug(f'Response Content: {response.text}')
                
                if(len(response.data['text']) > 0):
                    log.info(f'Post shared to Twitter successfully.')
                else:
                    log.warning(f'Unable to share content to Twitter. Run in debug mode to view detailed error.')
            except Exception as e:
                log.error(f'Error in sharing post to Twitter. Error: {e}')

    
