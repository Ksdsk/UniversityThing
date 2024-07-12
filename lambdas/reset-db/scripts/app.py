import json
import boto3
import os
import mysql.connector

def get_db_connector(db_hostname, db_port, db_region, db_username, db_password, db_name):

    try:
        print(f"Attempting to connect to DB at {db_hostname}:{db_port} with user {db_username}")

        connection = mysql.connector.connect(
            host=db_hostname,
            user=db_username,
            password=db_password,
            port=db_port
        )

        print("DB Connection Successful")
        return connection
    
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        raise

    except Exception as e:
        print(f"Exception: {e}")
        raise

def lambda_handler(event, context):

    try:
        if not event:
            raise AttributeError("No event")
        
        if 'body' not in event or not event['body']:
            raise AttributeError("Missing event body")

        connection = get_db_connector(
            os.environ["RDS_HOSTNAME"], 
            os.environ["RDS_PORT"], 
            os.environ["RDS_REGION"],
            os.environ["RDS_USERNAME"],
            os.environ["RDS_PASSWORD"],
            os.environ["RDS_DB_NAME"]
        )
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
