import requests
import json

def main(event, context):
    print(f"Printing from main handler...")

    # Extract code and state from request
    response_body = {
        'code'  : event['queryStringParameters']['code'],
        'state' : event['queryStringParameters']['state']
    }

    print(f"Printing from Lambda.")

    return {
        'statusCode': 200,
        'body': json.dumps(response_body)
    }