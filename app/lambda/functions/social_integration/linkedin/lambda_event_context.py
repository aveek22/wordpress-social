"""
    Prepare the event for lambda function.
    Only used to create events in local machine.
"""

import json
import logging as log

log.basicConfig(level=log.DEBUG)


def get_lambda_event():
    """ Read linkedin_event.json file and return a mock SQS event payload. """

    try:
        with open('app/lambda/functions/social_integration/linkedin/linkedin_event.json', 'r') as f:
            data = json.load(f)
        log.debug(f'Reading from JSON event file successful.')
    except Exception as e:
        log.error(f'Error in reading JSON event file. {e}')
    
    sqs_event = {
        "Records": [
            {
                "body": json.dumps(data)
            }
        ]
    }
    log.debug(f'Returning SQS payload. {sqs_event}')

    return sqs_event