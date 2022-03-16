"""
    This function will share content to the LinkedIn page.
"""

# Import system modules
import json
import logging

# Import custom modules
from publish import PublishLinkedIn


# Setup Logger
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def main(event, context):
    """ Lambda Handler for LinkedIn content publish """

    log.info(f'Received event from SQS: {event}')

    # Parse the SQS payload and return event
    parsed_event = parse_event(event)
    log.info(f'Parsed Event: {parsed_event}')
    
    # Create the LinkedIn object
    linkedin = PublishLinkedIn()

    # Get the payload from event
    payload = linkedin.get_payload(parsed_event)
    log.info(f'Payload: {payload}')

    # Share content to LinkedIn page.
    linkedin.post_content(payload)


def parse_event(sqs_payload):
    """ Parse the SQS payload and return the event message. """
    
    try:
        event = sqs_payload['Records'][0]['body']
        event = event.replace("\'", "\"")
        event = json.loads(event)
        # log.debug(f'Parsed event from SQS: {event}')
    except:
        event = False

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
