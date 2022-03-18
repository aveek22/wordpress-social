# Import the system libraries
import boto3
import logging


# Setup Logger
log = logging.getLogger(__name__)


class TwitterCredentials:
    """This class will store the Twitter credentials."""

    def __init__(self):
        self.CONSUMER_KEY = ""
        self.CONSUMER_KEY_SECRET = ""
        self.ACCESS_TOKEN = ""
        self.ACCESS_TOKEN_SECRET = ""


    def _get_twitter_consumer_key(self):
        """ Get the Consumer Key from AWS Parameter store. """

        # Create the boto client
        try:
            log.debug(f'Creating boto3 client for parameter store.')
            client = boto3.client('ssm')
        except Exception as e:
            log.error(f'Error cretaing SSM client Boto3. {e}')

        # Get the Parameter details from AWS
        try:
            response = client.get_parameter(
                Name = "/social_integration/twitter/consumer_key",
                WithDecryption = False
            )
            log.info(f'Twitter consumer key obtained from parameter store.')
            # Set parameter value to object
            self.CONSUMER_KEY = response['Parameter']['Value']

        except Exception as e:
            log.error(f'Error fetching Twitter consumer key from Parameter Store. {e}')


    def _get_twitter_consumer_key_secret(self):
        """ Get the Consumer Key Secret from AWS Parameter store. """

        # Create the boto client
        try:
            log.debug(f'Creating boto3 client for parameter store.')
            client = boto3.client('ssm')
        except Exception as e:
            log.error(f'Error cretaing SSM client Boto3. {e}')

        # Get the Parameter details from AWS
        try:
            response = client.get_parameter(
                Name = "/social_integration/twitter/consumer_key_secret",
                WithDecryption = False
            )
            log.info(f'Twitter consumer key secret obtained from parameter store.')
            # Set parameter value to object
            self.CONSUMER_KEY_SECRET = response['Parameter']['Value']

        except Exception as e:
            log.error(f'Error fetching Twitter consumer key secret from Parameter Store. {e}')


    def _get_twitter_access_token(self):
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
                Name = "/social_integration/twitter/access_token",
                WithDecryption = False
            )
            log.info(f'Twitter access token obtained from parameter store.')
            # Set parameter value to object
            self.ACCESS_TOKEN = response['Parameter']['Value']

        except Exception as e:
            log.error(f'Error fetching Twitter access token from Parameter Store. {e}')


    def _get_twitter_access_token_secret(self):
        """ Get the Access Token Secret from AWS Parameter store. """

        # Create the boto client
        try:
            log.debug(f'Creating boto3 client for parameter store.')
            client = boto3.client('ssm')
        except Exception as e:
            log.error(f'Error cretaing SSM client Boto3. {e}')

        # Get the Parameter details from AWS
        try:
            response = client.get_parameter(
                Name = "/social_integration/twitter/access_token_secret",
                WithDecryption = False
            )
            log.info(f'Twitter access token secret obtained from parameter store.')
            # Set parameter value to object
            self.ACCESS_TOKEN_SECRET = response['Parameter']['Value']

        except Exception as e:
            log.error(f'Error fetching Twitter access token secret from Parameter Store. {e}')


    def get_twitter_credentials_from_parameter_store(self):
        """Get the Twitter credentials by invoking individual methods."""
        
        log.info(f'Fetching Twitter Credentials.')
        
        self._get_twitter_consumer_key()
        self._get_twitter_consumer_key_secret()
        self._get_twitter_access_token()
        self._get_twitter_access_token_secret()
