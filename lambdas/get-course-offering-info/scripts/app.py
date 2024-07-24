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
        
        data = json.loads(event['body'])

        if not data:
            raise AttributeError("Missing data")
        
        if 'course_offering_id' not in data:
            raise AttributeError("Missing course_offering_id")
        
        course_offering_id = data['course_offering_id']

        connection = get_db_connector(
            os.environ["RDS_HOSTNAME"], 
            os.environ["RDS_PORT"], 
            os.environ["RDS_REGION"],
            os.environ["RDS_USERNAME"],
            os.environ["RDS_PASSWORD"],
            os.environ["RDS_DB_NAME"]
        )
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("USE `university-thing-database`")
        # Execute queries
        query = f"SELECT course_offering_id, term_id, course_name, course_code, category_code, category_name, school_name, school_id, category_id, campus_id, instructor_id FROM course_offering INNER JOIN course USING (course_id) INNER JOIN category USING (category_id) INNER JOIN school using (school_id) WHERE course_offering.course_offering_id = \"{course_offering_id}\""
        cursor.execute(query)
        result = cursor.fetchone()

        if not result:
            raise AttributeError("No course offering found by that ID!")
        
        body = {
            "message": f"Successfully fetched a course offering.",
            "course_offering_id": result["course_offering_id"],
            "term_id": result["term_id"],
            "course_name": result["course_name"],
            "course_code": result["course_code"],
            "category_code": result["category_code"],
            "category_name": result["category_name"],
            "school_name": result["school_name"],
            "school_id": result["school_id"],
            "category_id": result["category_id"],
        }
        
        if result["campus_id"] is not None:
            query = f"SELECT campus_name FROM campus WHERE campus_id = \"{result['campus_id']}\""
            cursor.execute(query)
            result_campus = cursor.fetchone()
            body["campus_name"] = result_campus["campus_name"]

        if result["instructor_id"] is not None:
            query = f"SELECT instructor_name, instructor_rmp_link FROM instructor WHERE instructor_id = \"{result['instructor_id']}\""
            cursor.execute(query)
            result_instructor = cursor.fetchone()
            body["instructor_name"] = result_instructor["instructor_name"]
            body["instructor_rmp_link"] = result_instructor["instructor_rmp_link"]

        connection.close()

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
