# Test module for LinkedIn

# Import system libraries
import pytest

# Import application modules
from src.lambda_functions.social_integration.linkedin.publish import PublishLinkedIn



# Unit Tests Cases here

def test_check_organization_id():
    """Checks the organization_id generated."""
    li = PublishLinkedIn()
    assert li.organization_id == '79377523'


def test_check_user_name():
    """Checks the user name generated."""
    li = PublishLinkedIn()
    assert li.username == 'Aveek Das'


def test_check_linkedin_user_id():
    """Checks the LinkedIn userID generated."""
    li = PublishLinkedIn()
    assert li.linkedin_user_id == 'urn:li:person:G0CopwI-SP'

