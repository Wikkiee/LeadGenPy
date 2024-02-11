import csv
import json
import traceback
import time
from datetime import datetime
from itertools import cycle

from dotenv import load_dotenv
from rich import print_json
from Configs.database import get_database_connection
from Utils.resource_calculator import get_network_usage


load_dotenv()


def insert_all_data_into_database(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    try:
        with open("../assets/data.json", 'r') as json_file:
            data_to_insert = json.loads(json_file.read())

            connection = get_database_connection()
            cursor = connection.cursor()

            inserted = 0
            for index,item in enumerate(data_to_insert):
                columns = ', '.join(item.keys())
                values = ', '.join(["%s"] * len(item))
                insert_query = f"INSERT INTO leads ({columns}) VALUES ({values})"
                try:
                    cursor.execute(insert_query, list(item.values()))
                    if cursor.rowcount == 1:
                        inserted += 1
                        if console:
                            console.print(
                                f"[green]🎉 [bold]{item['business_name']}[reset] [green]Data inserted successfully [yellow]({inserted}/{len(data_to_insert)})")
                except Exception as error:
                    print(error)
                    if console:
                        console.print(
                            f"[red]🚨 [bold]{item['business_name']}[reset] [red]Data insertion Failed! [yellow]({inserted}/{len(data_to_insert)})")

                if status:
                    status.update(
                        f"[bold yellow]Inserting Data Into Database... [green]({index + 1}/{len(data_to_insert)}) done:{inserted}")

            cursor.close()
            connection.commit()
            connection.close()
            json_file.close()

            result['time_taken'] = time.time() - result['time_taken']
            result["network_usage"] = get_network_usage() - result["network_usage"]
            return result
    except Exception as error:
        print(error)
        traceback.print_exc()

        result['status'] = False
        result['error'] = error
        return result





def get_details_for_emails():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute(
            "SELECT lead_id,business_email,personalized_email_subject,personalized_email_content,status,business_name FROM leads")
        result = cursor.fetchall()
        return result
    except Exception as error:
        print(error)


def generate_json(data):
    try:
        with open('../assets/data.json', 'w+') as json_file:
            json.dump(list(data), json_file)
            json_file.close()
    except Exception as error:
        print(error)


def get_all_data_from_json_file():
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}
    try:
        with open("../assets/data.json", 'r') as json_file:
            data = json.loads(json_file.read())
            print_json(json.dumps(data, indent=4))
        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result
    except Exception as error:

        result['status'] = False
        result['error'] = error
        return result

def export_database_into_csv_dataset(console=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    try:
        conn = get_database_connection()
        cursor = conn.cursor()


        try:
            query ="""
                    SELECT 
                    Leads.*, 
                    Allabolag.organization_number, 
                    Allabolag.registered_name, 
                    Allabolag.ceo_name, 
                    Allabolag.type_of_business, 
                    Allabolag.revenue, 
                    Allabolag.number_of_employees, 
                    Allabolag.year_of_registeration, 
                    headcounts.headcount_2022, 
                    headcounts.headcount_2021, 
                    headcounts.headcount_2020, 
                    headcounts.headcount_2019, 
                    headcounts.headcount_2018, 
                    headcounts.headcount_2017, 
                    revenue_track.revenue_track_2022, 
                    revenue_track.revenue_track_2021, 
                    revenue_track.revenue_track_2020, 
                    revenue_track.revenue_track_2019, 
                    revenue_track.revenue_track_2018, 
                    revenue_track.revenue_track_2017 
                    
                    FROM Leads 
                    LEFT JOIN Allabolag ON Leads.lead_id = Allabolag.lead_id 
                    LEFT JOIN Headcounts ON Allabolag.allabolag_id = Headcounts.allabolag_id 
                    LEFT JOIN revenue_track ON Allabolag.allabolag_id = revenue_track.allabolag_id
            """
            cursor.execute(query)
            column_names = [name[0] for name in cursor.description]
            rows_data = cursor.fetchall()

            for index,data in enumerate(rows_data):
                temp_tupe_to_list = list(data)
                if temp_tupe_to_list[16]:
                    temp_tupe_to_list[16] = f'{temp_tupe_to_list[16][:6]}-{temp_tupe_to_list[16][6:]}'
                rows_data[index] = tuple(temp_tupe_to_list)
            time_stamp = str(datetime.fromtimestamp(time.time()))[:-7].replace(" ","_").replace(":","_")
            fp = open(f'../exports/leads_dataset_{time_stamp}.csv', 'w', encoding='utf-8')
            my_file = csv.writer(fp,lineterminator='\n')
            my_file.writerow(column_names)
            my_file.writerows(rows_data)
            fp.close()
            if console:
                console.print(
                    f"[green]🎉 [bold]Leads Data[reset] [green] has been exported successfully")
        except:
            traceback.print_exc()
            if console:
                console.print(
                    f"[red]🚨 [bold]Leads Data[reset] [red]Table into CSV Generation is Failed !")
        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result
    except Exception as error:
        result['status'] = False
        result['error'] = error
        return result


def get_sweden_dataset():
    try:
        with open("../assets/SwedenCitiesDatabase.json", 'r') as json_file:
            data = json.loads(json_file.read())
            print(json.dumps(data, indent=4))
    except Exception as error:
        print(error)



