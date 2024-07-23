import json
from scripts.app import lambda_handler

DUMMY_FIRST_NAME = "John"
DUMMY_LAST_NAME = "Doe"

def test_returns_200():
    # Prepare a sample event
    event = {
        "body": json.dumps({
            "first_name": DUMMY_FIRST_NAME,
            "last_name": DUMMY_LAST_NAME
        })
    }

    # Call the lambda_handler function with the sample event
    response = lambda_handler(event, None)

    # Perform assertions on the response
    assert response['statusCode'] == 200
    assert json.loads(response['body'])['message'] == f"Hello {DUMMY_FIRST_NAME} {DUMMY_LAST_NAME}!"

def test_returns_400_because_no_event():
    # Prepare a sample event
    event = None

    # Call the lambda_handler function with the sample event
    response = lambda_handler(event, None)

    # Perform assertions on the response
    assert response['statusCode'] == 400
    assert json.loads(response['body'])['message'] == "No event"

def test_returns_400_because_no_event_body():
    # Prepare a sample event
    event1 = {
        "body": None
    }

    event2 = {
        "something": "else"
    }

    # Call the lambda_handler function with the sample event
    response1 = lambda_handler(event1, None)
    response2 = lambda_handler(event2, None)

    # Perform assertions on the response
    assert response1['statusCode'] == 400
    assert json.loads(response1['body'])['message'] == "Missing event body"
    assert response2['statusCode'] == 400
    assert json.loads(response2['body'])['message'] == "Missing event body"

def test_returns_400_because_no_last_name():
    # Prepare a sample event
    event = {
        "body": json.dumps({
            "first_name": DUMMY_FIRST_NAME
        })
    }

    # Call the lambda_handler function with the sample event
    response = lambda_handler(event, None)

    # Perform assertions on the response
    assert response['statusCode'] == 400
    assert json.loads(response['body'])['message'] == "Missing last_name"

def test_returns_400_because_no_first_name():
    # Prepare a sample event
    event = {
        "body": json.dumps({
            "last_name": DUMMY_LAST_NAME
        })
    }

    # Call the lambda_handler function with the sample event
    response = lambda_handler(event, None)

    # Perform assertions on the response
    assert response['statusCode'] == 400
    assert json.loads(response['body'])['message'] == "Missing first_name"