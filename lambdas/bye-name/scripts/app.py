import json

def lambda_handler(event, context):
    
    try:
        if not event:
            raise AttributeError("No event")
        
        if 'body' not in event or not event['body']:
            raise AttributeError("Missing event body")
        
        data = json.loads(event['body'])

        if not data:
            raise AttributeError("Missing data")
        
        if 'first_name' not in data:
            raise AttributeError("Missing first_name")
        
        if 'last_name' not in data:
            raise AttributeError("Missing last_name")
        
        first_name = data['first_name']
        last_name = data['last_name']

        body = {
            "message": f"Bye {first_name} {last_name}!"  
        }

        return { 
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(body)
        }
    except AttributeError as e:
        print(f"Attribute Error: {str(e)}") # Log Error
        body = {
            "message": str(e)
        }
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(body)
        }
    except Exception as e:
        print(f"Error: {str(e)}") # Log Error
        body = {
            "message": str(e)
        }

        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(body)
        }
    
