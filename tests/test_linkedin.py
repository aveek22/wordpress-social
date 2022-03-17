# Test module for LinkedIn

# Import system libraries
import pytest

# Import application modules
from app.lambda_functions.social_integration.linkedin.publish import PublishLinkedIn



# Unit Tests Cases here

def test_create_instance_publish_linkedin():
    li = PublishLinkedIn()
    assert li.organization_id == '79377523'