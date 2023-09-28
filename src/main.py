from WebScrapper.store import Store
from WebScrapper.scrapper import Scrappers 
from Configs.selenium_config import driver
from EmailController.personalized_email_sender import Emails 



def main():
    print("\n<=== MENU ===>\n1 - EXTRACT DATASET\n2 - SHOW DATASET\n3 - TRANSFER DATASET TO SHEET\n4 - GENERATE AND SEND PERSONALIZED EMAILS\n5 - PRODUCTION MODE (It'll do All 4 steps)\n0 - Exit the script \n<=== END ===>\n")
    emails = Emails()
    scrapper = Scrappers()
    store = Store()
    mode = int(input())

    try:
        if mode == 0:
            print("\n<== Terminated ==>\n")
            driver.close()
        elif mode == 1:
            print("\n<== EXTRACTION STARTED ==>\n")

            business_name = input("Enter the Business Name: ")
            location = input("Enter the Location: ")
            scrapper.scrape(business_name, location)
            
            print("\n<== EXTRACTED COMPLETED ==>\n")
            main()
        elif mode == 2:
            print("\n<== EXTRACTED DATASET ==>\n")
            
            store.get_all_dataset()
            
            print("\n<== EXTRACTED DATASET ==>\n")
            main()
        elif mode == 3:
            print("\n<== TRANSFERING ==>\n")
            store.append_all_data_to_sheet()
            print("\n<== TRANSFER COMPLETED ==>\n")
            main()
        elif mode == 4:
            print("\n<== GENERATE PERSONALIZED MAILS ==>\n")
            
            emails.send()
            
            print("\n<== FINISHED SENDING PERSONALIZED MAILS ==>\n")
            main()
        elif mode == 5:
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
        else:
            print("<== DEVELOPMENT MODE - STARTED ==>")
            
            store.remove_sheet_duplicates()
            
            print("<== DEVELOPMENT MODE - FINISHED ==>")
            main()
    except Exception as error:
        print(error)

main()
