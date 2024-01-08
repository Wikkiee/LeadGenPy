import base64
import os
import time
import datetime
import traceback
from email.message import EmailMessage
from Configs.google_api_config import service
from WebScrapper.store import Store
from ChatGPT.content_generator import EmailContentGenerator
from beaupy.spinners import *
class Emails:
    time_stamp = datetime.datetime.now().strftime("%H:%M:%S")
    def send(self):
            try:
                spinner = Spinner(DIAMOND,"Generating personalized Emails...")
                spinner.start()
                log_file = open('../assets/logs.txt',"a")
                log_file.write(f"[{self.time_stamp}] - GENERATING PERSONALIZED CONTENT\n") 
                store = Store()
                data = store.get_all_sheet_data()
                delay = 3
                spinner.stop()
                for rows in data:
                    try:
                        if rows[-2] != "null" and rows[-1] == "null" or rows[-1] == "FAILED":
                            log_file.write(f"[{self.time_stamp}] - GENERATING FOR -{rows[0]}\n") 
                            spinner = Spinner(DIAMOND,f"GENERATING FOR -{rows[0]}...")
                            spinner.start()
                            time.sleep(1)
                            emailContentGenerator = EmailContentGenerator()
                            spinner.stop()
                            content = emailContentGenerator.generate({
                                "BusinessName": rows[0],
                                "Address": rows[1],
                                "PhoneNumber": rows[2],
                                "Website": rows[3],
                                "Category": rows[4],
                                "Rating": rows[5],
                                "ReviewCount": rows[6],
                                "google_map_link": [7]
                            })

                            gmail = service["gmail"]
                            message = EmailMessage()
                            email_address = 'wikkiedev@gmail.com' 
                            #email_address = rows[-2] - uncomment this to send the mail to extracted mail address
                            spinner = Spinner(DIAMOND,f"Sending mail to {email_address}...")
                            spinner.start()
                            log_file.write(f"[{self.time_stamp}] -  SENDING MAIL TO {email_address}\n") 
                            message['To'] = email_address
                            message['From'] = os.getenv("EMAIL_ADDRESS")
                            message['Subject'] = content[0]
                            message.set_content(content[1])

                            # encoded message
                            encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
                                .decode()

                            create_message = {
                                'raw': encoded_message
                            }
                            send_message = (gmail.users().messages().send
                                            (userId="me", body=create_message).execute())
                            spinner.stop()
                            spinner = Spinner(DIAMOND,f"Personalized email successfully sent - [MESSAGE ID: {send_message['id']}]...")
                            spinner.start()
                            log_file.write(f"[{self.time_stamp}] - PERSONALIZED EMAIL SEND SUCCESSFULLY\nMESSAGE ID: {send_message['id']}\n") 
                            store.update_personalized_email_status(rows[0],"SUCCESS")
                            spinner.stop()
                            spinner = Spinner(DIAMOND,f"Stopped for {delay} Sec to prevent ChatGPT from continuous request error...")
                            spinner.start()
                            log_file.write(f"[{self.time_stamp}] - Stopped for {delay} Sec to prevent ChatGPT from continuous request error\n") 
                            spinner.stop()
                            time.sleep(delay)
                    except Exception as error:
                        log_file.write(f"[{self.time_stamp}] - PERSONALIZED EMAIL: FAILED\n") 
                        log_file.close()
                        spinner.stop()
                        traceback.print_exc()
                        print(error)
                        store.update_personalized_email_status(rows[0],"FAILED")
                log_file.close()
            except Exception as error:

                 traceback.print_exc()
                 print(error)
