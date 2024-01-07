from EmailController.personalized_email_sender import Emails 
from WebScrapper.store import Store
from WebScrapper.scrapper import Scrappers 
from Configs.selenium_config import driver
from beaupy import confirm, select,prompt
from rich.console import Console
from beaupy.spinners import *

import os

def main():
    emails = Emails()
    scrapper = Scrappers()
    store = Store()
    console = Console()
    mode = select(["[1] - Extract Data","[2] - Show extracted data","[3] - Transfer datset to Google Sheet","[4] - Generate and Send Personalized Emails","[5] - Production Mode (It'll do all 4 steps)","[6] - Clear the Terminal","[7] - Exit the script","[8] - Development Mode"],return_index=True)
    print(mode)
    try:

        if mode == 0:
            spinner = Spinner(BARS,"Extracting data ...")
            spinner.start()
            business_name = prompt("Enter the Business Name: ")
            location = prompt("Enter the Location: ")
            scrapper.scrape(business_name, location)
            if confirm("Do you want to clear the logs ?"):
                os.system('cls||clear')
            spinner.stop()
            main()
        elif mode == 1:
            print("\n<== EXTRACTED DATASET ==>\n")
            
            store.get_all_dataset()
            
            print("\n<== EXTRACTED DATASET ==>\n")
            main()
        elif mode == 2:
            print("\n<== TRANSFERING ==>\n")
            store.append_all_data_to_sheet()
            print("\n<== TRANSFER COMPLETED ==>\n")
            main()
        elif mode == 3:
            print("\n<== GENERATE PERSONALIZED MAILS ==>\n")
            
            emails.send()
            
            print("\n<== FINISHED SENDING PERSONALIZED MAILS ==>\n")
            main()
        elif mode == 4:
            print("<== PRODUCTION MODE - STARTED ==>")
            
            business_name = input("Enter the Business name: ")
            location = input("Enter the Location: ")
            scrapper.scrape(business_name, location)
            
            print("\n DATASET LOADED")
            print("\n TRANSFERING DATASET")
            
            store.append_all_data_to_sheet()
            
            print("\n SENDING PERSONALIZED EMAILS")
            
            emails.send()
            
            mode()
            print("<== PRODUCTION MODE - FINISHED ==>")
        elif mode == 5:
            os.system('cls||clear')
            main()
        elif mode == 6:
            console.print("[red]<== Terminated ==>[/red]")
            driver.close()
        else:
            print("<== DEVELOPMENT MODE - STARTED ==>")
            
            # store.remove_sheet_duplicates()
            
            print("<== DEVELOPMENT MODE - FINISHED ==>")
            main()
    except Exception as error:
        print(error)

main()
