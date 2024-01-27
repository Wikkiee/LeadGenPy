import os
import ssl
import time
import smtplib
import datetime
import traceback
from Utils.store import Store
from email.message import EmailMessage
from email.message import EmailMessage
from Configs.database_config import get_database_connection
from ChatGPT.content_generator import EmailContentGenerator


class PersonalizedContents:
    time_stamp = datetime.datetime.now().strftime("%H:%M:%S")

    def personalized_email_content_generator(self):
            try:
                store = Store()
                business_data_list = store.get_all_data_from_database()
                delay = 3
                connection = get_database_connection()
                cursor = connection.cursor()
                print(business_data_list)
                for business_data in business_data_list:
                    id = business_data[0]
                    if business_data[-2]=='null'  and business_data[-3] == 'null' and business_data[3] != "null" and business_data[-1] == "PENDING":
                        print(id)
                        data_to_feed_chatgpt = {}
                        keys =  [ "business_name","business_address","business_email","mobile_number","website_url","business_category","ratings","review_counts","top_review_1","top_review_2","top_review_3","google_map_url"]
                        for key in keys:
                            data_to_feed_chatgpt[key] = business_data[keys.index(key)+1]
                        emailContentGenerator = EmailContentGenerator()                     
                        print("Generating content")
                        personalized_email_content = emailContentGenerator.generate(data_to_feed_chatgpt)
                        personalized_email_subject =personalized_email_content[0].replace("'", "\\'")
                        personalized_email_content =personalized_email_content[1].replace("'", "\\'")
                        
                        cursor.execute(f"""UPDATE leads SET personalized_email_subject = '{personalized_email_subject}' , personalized_email_content = '{personalized_email_content}' WHERE lead_id={id}""")
                        print(cursor.rowcount)
                        connection.commit()
                        time.sleep(3)
                            
                cursor.close()
                connection.close()
            except Exception as error:
                 traceback.print_exc()
                 print(error)


    def send_personalized_emails(self):
        store = Store()
        HOST = "smtp.gmail.com"
        data_list = store.get_details_for_emails()
        sender_email = os.environ.get("EMAIL_ADDRESS")
        PASSWORD = os.environ.get("EMAIL_PASSWORD")
        try:
                connection = get_database_connection()
                cursor = connection.cursor()
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context)as smtp:
                    smtp.login(sender_email,password=PASSWORD)
                    
                    for (id,reciever_email,subject,content,status) in data_list:
                        if "null" in [id,reciever_email,subject,content] or status == "SUCCESS" and status == "PENDING":
                            print("Null found in the data set")
                            continue
                        em = EmailMessage()
                        em["From"] = sender_email
                        em["To"] = "vigneshrgm962950@gmail.com"
                        em["Subject"] = subject
                        em.set_content(content)

                        res = smtp.sendmail(sender_email,"vigneshrgm962950@gmail.com",em.as_string())
                        print(res)
                        cursor.execute(f"UPDATE leads SET status = 'SUCCESS' WHERE id={id}")
                        connection.commit()
                        if cursor.rowcount==1:
                            print(f"Updated {id} successfully ")
                        else:
                            print(f'Updated {id} failed ')
                    cursor.close()
                    connection.close()
                print("All the mails are sent successfully")
        except Exception as error:
                cursor.close()
                connection.close()
                print(error)