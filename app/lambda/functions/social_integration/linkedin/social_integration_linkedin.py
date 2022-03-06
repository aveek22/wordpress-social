"""
    This function will share content to the LinkedIn page.
"""

# Import custom modules
from share_linkedin import ShareLinkedIn


def main(event, context):
    
    
    share_linkedin = ShareLinkedIn()

    payload = share_linkedin.get_payload()


if __name__ == '__main__':
    """ Execute the main function from the local runtime. """

    event = ''
    context = ''
    
    main(event, context)
