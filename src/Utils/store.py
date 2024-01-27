import json

from dotenv import load_dotenv

from Configs.database import get_database_connection

load_dotenv()


def insert_all_data_into_database():
    try:
        with open("../assets/data.json", 'r') as json_file:
            data_to_insert = json.loads(json_file.read())
            connection = get_database_connection()
            cursor = connection.cursor()
            for item in data_to_insert:
                columns = ', '.join(item.keys())
                values = ', '.join(["%s"] * len(item))
                insert_query = f"INSERT INTO leads ({columns}) VALUES ({values})"

                cursor.execute(insert_query, list(item.values()))
                if cursor.rowcount == 1:
                    print("Data inserted successfully")
                else:
                    print("Failed to insert data")
                    return False
            cursor.close()
            connection.commit()
            connection.close()
            json_file.close()
            return True
    except Exception as error:
        print(error)


def get_all_data_from_database():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM leads")
        result = cursor.fetchall()
        return result
    except Exception as error:
        print(error)


def get_details_for_emails():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id,business_email,personalized_email_subject,personalized_email_content,status FROM leads")
        result = cursor.fetchall()
        return result
    except Exception as error:
        print(error)


def generate_json(data):
    try:
        with open('../assets/data.json', 'w+') as json_file:
            json.dump(data, json_file)
            json_file.close()
    except Exception as error:
        print(error)


def get_all_data_from_json_file():
    try:
        with open("../assets/data.json", 'r') as json_file:
            data = json.loads(json_file.read())
            print(json.dumps(data, indent=4))
    except Exception as error:
        print(error)


def get_sweden_dataset():
    try:
        with open("../assets/SwedenCitiesDatabase.json", 'r') as json_file:
            data = json.loads(json_file.read())
            print(json.dumps(data, indent=4))
    except Exception as error:
        print(error)
