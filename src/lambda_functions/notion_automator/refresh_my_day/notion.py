# Import system libraries
import boto3  # To interact with the AWS resources
import requests  # Use REST API calls to interact with services
import logging  # Log messages for debugging
import os  # Get environment variables

# Setup Logger
log = logging.getLogger(__name__)


class NotionMyDay:
    """ Refresh MyDay Tasks. """

    def __init__(self):
        log.debug(f'Initiate NotionMyDay')

        self.header = self._get_header()
        log.debug(f'Header Set: {self.header}')

        self.filter_payload = self._get_filter_payload()
        log.debug(f'Filter Payload Set: {self.header}')

        log.info(f'NotionMyDay object initiated.')

    def _get_header(self):
        """ Prepare the header object with Authorization as Bearer Token. """

        # Get the access token from Parameter Store
        log.debug(f'Get access token from AWS parameter store.')
        access_token = self._get_access_token_from_parameter_store()
        log.debug(f'Access token fetched.')

        # Prepare the header object
        if (access_token):
            log.debug(f'Setting up the header information.')
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'Notion-Version': '2021-05-13'
            }
            log.info(f'Header information set.')
            return headers
        else:
            log.warn(f'Header information not set. Application may not work as expected.')
            return False

    def _get_filter_payload(self):
        """ Prepare the Filter payload. """

        log.debug(f'Setting up the Filter Payload.')
        filter_payload = {
            "filter": {
                "property": "Day",
                "checkbox": {
                    "equals": True
                }
            }
        }
        log.info(f'Filter Payload set.')

        return filter_payload

    def _get_access_token_from_parameter_store(self):
        """ Get the Access Token from AWS Parameter store. """

        # Create the boto client
        try:
            log.debug(f'Creating boto3 client for parameter store.')
            client = boto3.client('ssm')
        except Exception as e:
            log.error(f'Error cretaing SSM client Boto3. {e}')

        # Get the Parameter details from AWS
        try:
            response = client.get_parameter(
                Name="/notion_automator/datacloudmag/access_token",
                WithDecryption=False
            )
            log.info(f'Access token obtained from parameter store.')
            # Return the parameter value
            return response['Parameter']['Value']
        except Exception as e:
            log.error(f'Error fetching parameter from Parameter Store. {e}')
            return False

    def _clean_my_day_response(self, response_json):
        """ Clean the JSON response and return Task Name and ID. """

        log.debug(f"Cleaning JSON reponse for MyDay")

        # Create an empty list to store dictionary values.
        list_my_day = []

        try:
            for task in response_json:
                task_title = task['properties']['Name']['title'][0]['plain_text']
                task_id = task['id']

                task_detail = {
                    "task_title": task_title,
                    "task_id": task_id
                }

                log.info(f"Adding task detail: {task_detail}")
                list_my_day.append(task_detail)

            log.debug(f"Added task details to list. {list_my_day}")
        except Exception as e:
            log.error(f"Error in fetching task details from JSON response. Error: {e}")

        return list_my_day

    def get_my_day(self, event):
        """ Get MyDay tasks. """

        log.info(f"Received event payload. {event}")
        database_id = event['database_id']
        database_url = f"https://api.notion.com/v1/databases/{database_id}/query"
        my_day_tasks = False

        if self.header:
            try:
                log.debug(f'Fetching MyDay tasks.')
                response = requests.post(
                    url=database_url,
                    headers=self.header,
                    json=self.filter_payload
                )
                log.debug(f'Response Status Code: {response.status_code}')

                response_json = response.json()
                log.debug(f'Response Content: {response_json}')

                if response.status_code == 200:
                    log.info(f'Fetched MyDay from Notion successfully.')
                    my_day_tasks = self._clean_my_day_response(response_json['results'])
                elif response.status_code == 404:
                    log.info(
                        f'Unable to fetch MyDay from database. Database does not exist or no access provided to '
                        f'integration.')
                else:
                    log.warn(f'Unable to fetch tasks from MyDay. Run in debug mode to view detailed error.')
            except Exception as e:
                log.error(f'Error in fetching content from Notion. Error: {e}')

        return my_day_tasks

    def refresh_my_day(self, my_day_tasks):
        """ Refresh MyDay tasks. """

        # For each task, need to change the MyDay status

        my_day_refresh_payload = {"properties": {"Day": False}}

        for task in my_day_tasks:

            page_id = task['task_id']
            page_url = f"https://api.notion.com/v1/pages/{page_id}"

            if (self.header):
                try:
                    log.debug(f'Updating MyDay task - {task}.')
                    response = requests.request(
                        "PATCH",
                        url=page_url,
                        headers=self.header,
                        json=my_day_refresh_payload
                    )
                    log.debug(f'Response Status Code: {response.status_code}')

                    if (response.status_code == 200):
                        log.info(f'Updated MyDay - {task}.')
                    else:
                        log.warn(f'Unable to update tasks from MyDay. Run in debug mode to view detailed error.')
                except Exception as e:
                    log.error(f'Error in fetching content from Notion. Error: {e}')
