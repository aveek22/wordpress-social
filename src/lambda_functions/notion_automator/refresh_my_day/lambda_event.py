"""
    Prepare the event for lambda function.
    Only used to create events in local machine.
"""

import json
import logging as log

log.basicConfig(level=log.DEBUG)


def get_lambda_event():
    """ Read event.json file and return a mock event payload. """

    try:
        with open('app/lambda_functions/notion_automator/refresh_my_day/event.json', 'r') as f:
            data = json.load(f)
        log.debug(f'Reading from JSON event file successful.')
    except Exception as e:
        data = False
        log.error(f'Error in reading JSON event file. {e}')
    
    if(data):
        # sqs_event = {
        #     "Records": [
        #         {
        #             "body": json.dumps(data)
        #         }
        #     ]
        # }
        event = json.dumps(data)
        log.debug(f'Returning SQS payload. {event}')
    else:
        event = False

    return event