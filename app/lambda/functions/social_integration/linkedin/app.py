"""
    This function will share content to the LinkedIn page.
"""

# Import system modules
import json

# Import custom modules
from publish import PublishLinkedIn


def main(event, context):
    """ Lambda Handler for LinkedIn content publish """
    
    # Create the LinkedIn object
    linkedin = PublishLinkedIn()

    # Get the payload from event
    payload = linkedin.get_payload(event)

    # Share content to LinkedIn page.
    linkedin.post_content(payload)


def parse_event(sqs_payload):
    """ Parse the SQS payload and return the event message. """
    
    try:
        event = sqs_payload['Records'][0]['body']
        event = event.replace("\'", "\"")
        event = json.loads(event)
        print(event)
    except:
        event = False

    return event


if __name__ == '__main__':
    """ Execute the main function from the local runtime. """

    # Import test lambda_event_context module
    import lambda_event_context

    # Get the test SQS payload for Lambda function
    sqs_payload = lambda_event_context.get_lambda_event()

    # Parse the SQS payload and return event
    event = parse_event(sqs_payload)
    context = ''
    
    # Trigger the main function
    if(event):
        main(event, context)
