import os
import smtplib
import ssl
import time
import traceback
from email.message import EmailMessage
from rich.console import Console


import rich

from content_generator.personalized_content_generator import get_personalized_email_content_using_chatgpt
from Configs.database import get_database_connection
from Utils.store import get_all_data_from_database, get_details_for_emails


def generatore_personalized_email_contents(console:Console=None):
    console.print("*note:It may take a while to generate the content")
    try:
        business_data_list = get_all_data_from_database()

        connection = get_database_connection()
        cursor = connection.cursor()
        count = 0

        with console.status("[bold cyan]Generating Content...") as status:

            for business_data in business_data_list:

                item_id = business_data[0]

                if business_data[-2] == 'null' and business_data[-3] == 'null' and business_data[3] != "null" and business_data[-1] == "PENDING":

                    data_to_feed_chatgpt = {}
                    keys = ["business_name", "business_address", "business_email", "mobile_number", "website_url",
                            "business_category", "ratings", "review_counts", "top_review_1", "top_review_2", "top_review_3",
                            "google_map_url"]

                    for key in keys:
                        data_to_feed_chatgpt[key] = business_data[keys.index(key) + 1]

                    status.update(f"Generating Content For [green]{data_to_feed_chatgpt['business_name']}[reset] [yellow]rem:({len(business_data_list)-count})")
                    try:
                        personalized_email_content = get_personalized_email_content_using_chatgpt(data_to_feed_chatgpt)
                        personalized_email_subject = personalized_email_content[0].replace("'", "\\'")
                        personalized_email_content = personalized_email_content[1].replace("'", "\\'")
                    except Exception as error:
                        console.print(f"[red]❌ {data_to_feed_chatgpt['business_name']}'s Email Content Generation Failed!")
                        continue

                    cursor.execute(f"""UPDATE leads SET personalized_email_subject = '{personalized_email_subject}' , personalized_email_content = '{personalized_email_content}' WHERE lead_id={item_id}""")
                    console.print(f"[green]✅ {data_to_feed_chatgpt['business_name']}'s Email Content Generated")
                    connection.commit()
                    count += 1
                    time.sleep(3)

        cursor.close()
        connection.close()
    except Exception as error:
        traceback.print_exc()
        print(error)


def send_personalized_emails(console=None):
    data_list = get_details_for_emails()
    sender_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")
    connection = get_database_connection()
    cursor = connection.cursor()
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, password=password)
            c = 0
            for (item_id, reciever_email, subject, content, status, business_name) in data_list:
                if "null" in [item_id, reciever_email, subject, content] or status == "SUCCESS" and status == "PENDING":
                    console.print(f"[cyan]⚠ Not Enough Data For [yellow]{business_name}")
                    continue
                em = EmailMessage()
                em["From"] = sender_email
                em["To"] = "manoj.thunderviz@gmail.com"
                em["Subject"] = subject
                em.set_content(content)

                # res = smtp.sendmail(sender_email, "manoj.thunderviz@gmail.com", em.as_string())
                # cursor.execute(f"UPDATE leads SET status = 'SUCCESS' WHERE lead_id={item_id}")
                # connection.commit()
                if c < 1:
                    console.print(f"[green]✅  Personalized Email Successfully Sent To {reciever_email} - [yellow]{business_name}")
                else:
                    console.print(f"[red]❌  Personalized Email Faild To Sent To {reciever_email} - [yellow]{business_name}")
                c += 1
            cursor.close()
            connection.close()
    except Exception as error:
        cursor.close()
        connection.close()
        traceback.print_exc()
        print(error)

