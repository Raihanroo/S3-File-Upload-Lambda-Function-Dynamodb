"""AWS Lambda demo: fetch JSONPlaceholder users and save them to DynamoDB.

Required Lambda environment variable: TABLE_NAME=jsonplaceholder-users
Required IAM permission: dynamodb:PutItem on the table ARN.
"""

import json
import os
import urllib.request

import boto3

API_URL = "https://jsonplaceholder.typicode.com/users"
DEFAULT_TABLE_NAME = "jsonplaceholder-users"

dynamodb = boto3.resource("dynamodb")


def _get_table_name():
    table_name = os.getenv("TABLE_NAME", DEFAULT_TABLE_NAME)
    if not table_name:
        raise RuntimeError("TABLE_NAME environment variable is required")
    return table_name


def lambda_handler(event, context):
    table_name = _get_table_name()
    table = dynamodb.Table(table_name)
    print("Fetching users from JSONPlaceholder API...")

    request = urllib.request.Request(
        API_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "lambda-users-demo/1.0",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            users = json.load(response)

        if not isinstance(users, list):
            raise ValueError("API response was not a list of users")

        for user in users:
            if not isinstance(user, dict):
                raise ValueError("Each user record must be an object")
            if "id" not in user:
                raise ValueError("Each user record must include an 'id'")

            table.put_item(Item=user)
            print(f"Saved user ID={user['id']}: {user.get('name', 'Unknown user')}")

        print(f"Successfully saved {len(users)} users to DynamoDB table {table_name}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Users saved to DynamoDB",
                "table": table_name,
                "saved_count": len(users),
            }),
        }

    except Exception as error:
        print(f"ERROR: Failed to fetch or save users: {error}")
        raise
