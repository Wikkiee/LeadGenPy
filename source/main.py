import time
from EmailController.personalized_email_sender import PersonalizedContents 
from Utils.store import Store
from WebScrapper.scrapper import Scrappers  
from Configs.selenium_config import driver
from Configs.database_config import get_database_connection
from beaupy import confirm, select,prompt
from rich.console import Console
from beaupy.spinners import *

import os

def main():
    personalized_content = PersonalizedContents()
    scrapper = Scrappers()
    store = Store()
    console = Console()
    while True:

        mode = int(input("\n[0] - Extract Data\n[1] - Show extracted data\n[2] - Transfer datset to Google Sheet\n[3] - Generate and Send Personalized Emails\n[4] - Production Mode (It'll do all 4 steps)\n[5] - Clear the Terminal\n[6] - Development Mode\n[7] - Sweden Dataset (For Daniel)\n[9] - Exit the script"))
        
        try:
            if mode == 0:
                # business_name = input("Enter the Business Name: ")
                # location = input("Enter the Location: ")
                business_name,location = "Restaurants","Sweden"
                if business_name != None and location != None:
                    get_data_from_google_map(business_name, location)
                    break
                    # if confirm("Do you want to clear the logs ?"):
                    #     os.system('cls||clear')

            elif mode == 1:
                console.print("\n[blue]<== EXTRACTED DATASET ==>[/blue]\n")
                store.get_all_data_from_json_file()
                console.print("\n[blue]<== EXTRACTED DATASET ==>[/blue]\n")

            elif mode == 2:
                store.insert_all_data_into_database()
            
            
            
            elif mode == 8:
                get_business_email()
            elif mode == 9:
                get_organization_number()
            elif mode == 10:
                get_allabolag_details()
                




            elif mode == 3:
                content = personalized_content.personalized_email_content_generator()
            elif mode == 4:                   
                print("Production mode")
            elif mode == 5:
                os.system('cls||clear')
            elif mode == 6:
                print("<== DEVELOPMENT MODE - STARTED ==>")
                
                # store.remove_sheet_duplicates()
                
                print("<== DEVELOPMENT MODE - FINISHED ==>")
            elif mode == 7:
                console.print("\n[blue]<== Sweden Dataset ==>[/blue]\n")
                store.get_sweden_dataset()
                console.print("\n[blue]<== Sweden Dataset ==>[/blue]\n")
            else :
                break
        except Exception as error:
            print(error)

    
main()
