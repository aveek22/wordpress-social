"""
    This function will share content to the LinkedIn page.
"""

# Import custom modules
from share_linkedin import ShareLinkedIn


def main(event, context):
    
    
    share_linkedin = ShareLinkedIn()

    payload = share_linkedin.get_payload()

    share_linkedin.post_content(payload)


if __name__ == '__main__':
    """ Execute the main function from the local runtime. """

    import json
    
    with open('app/lambda/functions/social_integration/linkedin/linkedin_event.json', 'r') as f:
        data = json.load(f)
    
    event = {
        "Records": [
            {
                "body": json.dumps(data)
            }
        ]
    }
    context = ''
    
    main(event, context)
