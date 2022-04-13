"""
    This function will share content to the LinkedIn page.
"""

# Import system modules
import json         # Deal with JSON data
import logging      # Log messages for debugging
import os           # Get environment variables

# Import custom modules
from notion import NotionMyDay


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

    # Parse the event payload and return event
    parsed_event = parse_event(event)
    
    if(parsed_event):
        # Create the Notion object
        notion = NotionMyDay()

    if(notion):
        # Get the MyDay tasks with ID
        my_day_tasks = notion.get_my_day(parsed_event)
        log.debug(f'MyDay task list: {my_day_tasks}')

    if(my_day_tasks):
        # Refresh MyDay Tasks.
        notion.refresh_my_day(my_day_tasks)

    log.info(f'*************************** Application execution completed. ***************************')


def parse_event(event):
    """ Parse the event payload and return the database_id. """
    
    log.info(f'Received message from SQS: {event}')

    try:
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
    payload = lambda_event.get_lambda_event()
    
    # Trigger the main function
    if(payload):
        main(payload, '')
