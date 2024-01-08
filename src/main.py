import time
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
    while True:
        mode = select(["[1] - Extract Data","[2] - Show extracted data","[3] - Transfer datset to Google Sheet","[4] - Generate and Send Personalized Emails","[5] - Production Mode (It'll do all 4 steps)","[6] - Clear the Terminal","[7] - Development Mode","[8] - Sweden Dataset (For Daniel)","[9] - Exit the script"],return_index=True)
        try:
            if mode == 0:
                spinner = Spinner(ARC,"Extracting data ...")
                spinner.start()
                business_name = prompt("Enter the Business Name: ")
                location = prompt("Enter the Location: ")
                spinner.stop()
                if business_name != None and location != None:
                    scrapper.scrape(business_name, location)
                    if confirm("Do you want to clear the logs ?"):
                        os.system('cls||clear')

            elif mode == 1:
                console.print("\n[blue]<== EXTRACTED DATASET ==>[/blue]\n")
                store.get_all_dataset()
                console.print("\n[blue]<== EXTRACTED DATASET ==>[/blue]\n")

            elif mode == 2:
                spinner = Spinner(ARC,"Transfering data to Google Sheet ...")
                spinner.start()
                store.append_all_data_to_sheet()
                spinner.stop()
                spinner = Spinner(DIAMOND,"Transfer completed...")
                spinner.start()
                time.sleep(1)
                spinner.stop()
            elif mode == 3:
                emails.send()
            elif mode == 4:
                spinner = Spinner(ARC,"Production Mode Finished...")
                spinner.start()
                time.sleep(3)
                spinner.stop()
                if confirm("Are you sure want to continue production mode ?"):     
                    spinner = Spinner(ARC,"Extracting data ...")
                    spinner.start()
                    business_name = prompt("Enter the Business Name: ")
                    location = prompt("Enter the Location: ")
                    spinner.stop()
                    if business_name != None and location != None:
                        scrapper.scrape(business_name, location)
                    
                    spinner = Spinner(ARC,"Transfering data to Google Sheet ...")
                    spinner.start()
                    store.append_all_data_to_sheet()
                    spinner.stop()
                    spinner = Spinner(DIAMOND,"Transfer completed...")
                    spinner.start()
                    time.sleep(1)
                    spinner.stop()
                    emails.send()
                spinner = Spinner(ARC,"Production Mode Finished...")
                spinner.start()
                time.sleep(3)
                spinner.stop()
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
                spinner = Spinner(ARC,"Shutting Down...")
                spinner.start()
                driver.close()
                time.sleep(2)
                spinner.stop()
                spinner = Spinner(DIAMOND,"LeadGenPy Says: Bye...")
                spinner.start()
                time.sleep(3)
                spinner.stop()
                break
        except Exception as error:
            print(error)

main()
