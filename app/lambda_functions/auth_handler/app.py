import requests

def main(event, context):
    print(f"Printing from main handler...")

    print(f"{event}")

    return {
        "statusCode": 200,
        "body": {"foo": "bar"},
        "headers": {
            "Content-Type": "application/json"
        }
    }