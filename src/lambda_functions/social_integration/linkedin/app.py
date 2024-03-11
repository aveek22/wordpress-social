"""
    This function will share content to the LinkedIn page.
"""

# Import system modules
import json         # Deal with JSON data
import logging      # Log messages for debugging
import os           # Get environment variables

# Import custom modules
from publish import PublishLinkedIn


# Setup Logger
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
log_level = os.environ.get('WORDPRESS_SOCIAL_LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=log_level, format='%(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def main(event, context):
    """ Lambda Handler for LinkedIn content publish """

    log.info(f'*************************** Application execution started. ***************************')

    # Setting control flow variables as False
    log.debug(f'Setting control flow variables as False.')
    parsed_event = False
    linkedin = False
    payload = False

    # Parse the SQS payload and return event
    parsed_event = parse_event(event)
    
    if parsed_event:
        # Create the LinkedIn object
        linkedin = PublishLinkedIn()

    if linkedin:
        # Get the payload from event
        payload = linkedin.get_payload(parsed_event)
        log.debug(f'Payload: {payload}')

    if payload:
        # Share content to LinkedIn page.
        linkedin.post_content(payload)

    log.info(f'*************************** Application execution completed. ***************************')


def parse_event(sqs_payload):
    """ Parse the SQS payload and return the event message. """
    
    log.info(f'Received message from SQS: {sqs_payload}')

    try:
        event = sqs_payload['Records'][0]['body']
        event = event.replace("\'", "\"")
        event = json.loads(event)
        log.debug(f'Parsed event from SQS: {event}')
    except Exception as e:
        event = False
        log.error(f'Unable to parse SQS payload. Error: {e}')

    return event


if __name__ == '__main__':
    """ Execute the main function from the local runtime. """

    # Import test lambda_event module
    import lambda_event

    # Get the test SQS payload for Lambda function
    sqs_payload = lambda_event.get_lambda_event()
    
    # Trigger the main function
    if(sqs_payload):
        main(sqs_payload, '')
