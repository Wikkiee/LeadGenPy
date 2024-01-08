import json
import os
import datetime
import traceback
from Configs.google_api_config import service
from dotenv import load_dotenv
from rich.console import Console

load_dotenv()


class Store:

    time_stamp = datetime.datetime.now().strftime("%H:%M:%S")
    __SPREADSHEET_ID = os.getenv("SPREADSHEET_ID") 
    sheet = service["sheet"]

    def generate_json(self,data):
        try:
            log_file = open('../assets/logs.txt',"a")
            log_file.write(f"[{self.time_stamp}] - Generating JSON Data\n")            
            with open('../assets/data.json','w+') as json_file:
                json.dump(data,json_file)
                json_file.close()
            log_file.close()
        except Exception as error:
            print(error)

    def get_all_sheet_data(self):
        try:
            store = Store()
            store.remove_sheet_duplicates()
            result = self.sheet.values().get(spreadsheetId=self.__SPREADSHEET_ID,range="Sheet1").execute()
            return result.get('values',[])
        except Exception as error:
            print(error)
    def update_personalized_email_status(self,identifier,action):
            try:
                log_file = open('../assets/logs.txt',"a")
                log_file.write(f"[{self.time_stamp}] - Updating Personalized Email Status\n")  
                values = service["sheet"].values().get(spreadsheetId=self.__SPREADSHEET_ID, range="sheet1").execute()
                data = values.get('values', []) 
                if not data:
                    print(f"[Red][LOG] - No data found in sheet1[/Red]\n")
                    log_file.write(f"[{self.time_stamp}] - No data found in sheet1 \n")  
                    log_file.close()
                    return
                
                for row in data:
                    if row[0] == identifier:  
                        row[-1] = action  
                        update_request = {
                            'range': f"sheet1!A{data.index(row) + 1}:J{data.index(row) + 1}",
                            'values': [row]
                        }
                        
                        try:
                            response = service["sheet"].values().update(
                                spreadsheetId=self.__SPREADSHEET_ID, range=update_request['range'],valueInputOption="USER_ENTERED", body=update_request).execute()
                            log_file.write(f"[{self.time_stamp}] - Updated Personalized Email Status\n")
                            log_file.close()  
                        except Exception as error:
                            print(f'[Red]Error updating user: {error}[/Red]')
                            log_file.write(f"[{self.time_stamp}] - Error updating user: {error}\n")  
                            log_file.close()
                        break
                else:
                    log_file.write(f"[{self.time_stamp}] - User '{identifier}' not found in sheet1\n")  
                    log_file.close()
                    print(f"[Green][LOG] - User '{identifier}' not found in sheet1[/Green]")
            except Exception as error:
                print(error)

    def insert_one(self,values):
        result = self.sheet.values().append(spreadsheetId=self.__SPREADSHEET_ID,range="Sheet1!A2:I2",valueInputOption="USER_ENTERED",body={
            'values':values
        }).execute()

    def get_all_dataset(self):
        try:
            with open("../assets/data.json",'r') as json_file:
                data = json.loads(json_file.read())
                print(json.dumps(data,indent=4))
        except Exception as error:
            print(error)
    
    def append_all_data_to_sheet(self):
        try:
            with open("../assets/data.json",'r') as json_file:
                data = json.loads(json_file.read())
                store = Store()
                for item in data:
                    store.insert_one([list(item.values())])
                json_file.close()
        except Exception as error:
            print(error)
    def remove_sheet_duplicates(self):
        try:

            log_file = open('../assets/logs.txt',"a")
            log_file.write(f"[{self.time_stamp}] - REMOVING DUPLICATE ROWS\n")    
            request = {
            'requests': [
                {
                    'deleteDuplicates': {
                        'range': {
                            'sheetId':0,
                        }
                    }
                }
            ]
            }
            response = service["sheet"].batchUpdate(spreadsheetId=self.__SPREADSHEET_ID, body=request).execute()
            log_file.write(f"[{self.time_stamp}] - DUPLICATE ROWS REMOVED\n")    
            log_file.close()
        except Exception as error:
            print(f'[Red][LOG] - Error removing duplicates: {error}[/Red]\n')
            log_file.write(f"[{self.time_stamp}] - Error removing duplicates: {error}\n")    
            log_file.close()

    def get_sweden_dataset(self):
        try:
            with open("../assets/SwedenCitiesDatabase.json",'r') as json_file:
                data = json.loads(json_file.read())
                print(json.dumps(data,indent=4))
        except Exception as error:
            print(error)