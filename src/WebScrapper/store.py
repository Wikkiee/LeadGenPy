import json
import os
from Configs.google_api_config import service
from dotenv import load_dotenv
load_dotenv()


class Store:
    __SPREADSHEET_ID = os.getenv("SPREADSHEET_ID") 
    sheet = service["sheet"]
    def generate_json(self,data):
        with open('../assets/data.json','w+') as json_file:
            json.dump(data,json_file)
            json_file.close()

    def get_all_sheet_data(self):
        store = Store()
        store.remove_sheet_duplicates()
        result = self.sheet.values().get(spreadsheetId=self.__SPREADSHEET_ID,range="Sheet1").execute()
        return result.get('values',[])
    def update_personalized_email_status(self,identifier,action):
            values = service["sheet"].values().get(spreadsheetId=self.__SPREADSHEET_ID, range="sheet1").execute()
            data = values.get('values', []) 
            if not data:
                print(f"[LOG] - No data found in sheet1")
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
                        print(f'[LOG] - UPDATE LOG SAVED:\nRESPONSE: {response}')
                    except Exception as error:
                        print(f'Error updating user: {error}')
                    break
            else:
                print(f"[LOG] - User '{identifier}' not found in sheet1")
    def insert_one(self,values):
        result = self.sheet.values().append(spreadsheetId=self.__SPREADSHEET_ID,range="Sheet1!A2:I2",valueInputOption="USER_ENTERED",body={
            'values':values
        }).execute()

    def get_all_dataset(self):
        with open("../assets/data.json",'r') as json_file:
            data = json.loads(json_file.read())
            print(json.dumps(data,indent=4))
    
    def append_all_data_to_sheet(self):
        with open("../assets/data.json",'r') as json_file:
            data = json.loads(json_file.read())
            store = Store()
            for item in data:
                store.insert_one([list(item.values())])
            json_file.close()
    def remove_sheet_duplicates(self):
        print("[LOG] - REMOVING DUPLICATE ROWS")
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
        try:
            response = service["sheet"].batchUpdate(spreadsheetId=self.__SPREADSHEET_ID, body=request).execute()
            print(f'[LOG] - DUPLICATE ROWS REMOVED\nRESPONSE: {response}')
        except Exception as error:
            print(f'[LOG] - Error removing duplicates: {error}')