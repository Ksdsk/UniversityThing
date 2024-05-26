import json
import boto3
import os
import mysql.connector
from botocore.exceptions import ClientError

def get_db_creds(session, secret_name, region_name):
    
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        print(e)
        raise Exception(e)
    
    creds = json.loads(get_secret_value_response["SecretString"])
    return creds["username"], creds["password"]

def lambda_handler(event, context):
    
    try:
        if not event:
            raise AttributeError("No event")
        
        if 'body' not in event or not event['body']:
            raise AttributeError("Missing event body")

        # Set up DB information
        session = boto3.session.Session()

        db_username, db_password = get_db_creds(session, os.environ["RDS_SECRET_NAME"], "us-east-1")
        db_hostname = os.environ["RDS_HOSTNAME"]
        db_port = int(os.environ["RDS_PORT"])
        db_name = os.environ["RDS_DB_NAME"]

        connection = mysql.connector.connect(host=db_hostname, user=db_username, password=db_password, port=db_port)
        cursor = connection.cursor()

        with open("databases/model.sql", "r") as sql_file:
            setup_query = sql_file.read()

        with open("databases/model_init_mod.sql", "r") as insert_sql_file:
            insert_query = insert_sql_file.read()
        
        # Execute queries
        for statement in setup_query.split(";"):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        print("DB Setup Complete")

        for statement in insert_query.split(";"):
            if statement.strip():
                cursor.execute(statement)
        
        connection.commit()
        print("DB Insert Complete")

        cursor.execute("SELECT * FROM school")
        result = cursor.fetchall()
        connection.close()
        

        body = {
            "message": f"DB successfully created and reset to default.",
            "schools": result
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