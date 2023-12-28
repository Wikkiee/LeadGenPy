import base64
import os
import time
from email.message import EmailMessage
from Configs.google_api_config import service
from WebScrapper.store import Store
from ChatGPT.content_generator import EmailContentGenerator

class Emails:
    def send(self):
            print("\n[LOG] - GENERATING PERSONALIZED CONTENT\n")
            store = Store()
            data = store.get_all_sheet_data()
            delay = 3
            for rows in data:
                try:
                    if rows[-2] != "null" and rows[-1] == "null" or rows[-1] == "FAILED":
                        print(f"\n[LOG] - GENERATING FOR -{rows[0]}\n")
                        emailContentGenerator = EmailContentGenerator()
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
                        print(f"\n[LOG] - SENDING MAIL TO {email_address}\n")
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
                        print(F'[LOG] PERSONALIZED EMAIL SEND SUCCESSFULLY\nMESSAGE ID: {send_message["id"]}')
                        store.update_personalized_email_status(rows[0],"SUCCESS")
                        print(f"[LOG] - Stopped for {delay} sec to prevent Chatgpt continuous request error")
                        time.sleep(delay)
                except Exception as error:
                     print(F'[LOG] - PERSONALIZED EMAIL: FAILED')
                     print(error)
                     store.update_personalized_email_status(rows[0],"FAILED")
