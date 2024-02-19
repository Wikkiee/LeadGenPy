import os
import smtplib
import ssl
import time
import traceback
from email.message import EmailMessage
from rich.console import Console
from configs.database import get_database_connection
from Utils.embed_content_generator import  generate_embedded_email_content
from Utils.resource_calculator import get_network_usage
from Utils.store import  get_details_for_emails
from content_generator.personalized_content_generator import get_personalized_email_content_using_chatgpt


def generatore_personalized_email_contents_with_status(business_data_list, cursor, connection, console=None,
                                                       status=None,_status=None):
    count = 0
    for index,business_data in enumerate(business_data_list):
        if _status:
            _status.update(f"[bold yellow]Generating Personalized Email... [green]({index}\{len(business_data_list)}) done:{count}")

        item_id = business_data[0]

        data_to_feed_chatgpt = {}
        keys = ["business_name", "business_address", "business_email", "mobile_number", "website_url",
                "business_category", "ratings", "review_counts", "top_review_1", "top_review_2", "top_review_3",
                "google_map_url"]
        for key in keys:
            data_to_feed_chatgpt[key] = business_data[keys.index(key) + 1]
        if status:
            status.update(
                f"Generating Content For [green]{data_to_feed_chatgpt['business_name']}[reset] [yellow]rem:({len(business_data_list) - count})")
        try:
            personalized_email_content = get_personalized_email_content_using_chatgpt(data_to_feed_chatgpt)
            personalized_email_subject = personalized_email_content[0].replace("'", "\\'")
            personalized_email_content = personalized_email_content[1].replace("'", "\\'")
        except Exception:
            if console:
                console.print(f"[red]🚨 {data_to_feed_chatgpt['business_name']}'s Email Content Generation Failed!")
            continue
        cursor.execute(
            f"""UPDATE leads SET personalized_email_subject = '{personalized_email_subject}' , personalized_email_content = '{personalized_email_content}' WHERE lead_id={item_id}""")
        if console:
            console.print(f"[green]🎉 {data_to_feed_chatgpt['business_name']}'s Email Content Generated")
        connection.commit()
        count += 1
        time.sleep(3)

def generatore_personalized_email_contents(console: Console = None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    if console:
        console.print("*note:It may take a while to generate the content")
    try:

        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM leads WHERE business_email != 'null' AND personalized_email_content='null' AND personalized_email_subject ='null' ")
        business_data_list = cursor.fetchall()
        if console:
            with console.status("[bold cyan]Generating Content...") as status:
                generatore_personalized_email_contents_with_status(business_data_list, cursor, connection, console,
                                                                   status)
        else:
            generatore_personalized_email_contents_with_status(business_data_list, cursor, connection,_status=status)

        cursor.close()
        connection.close()

        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result
    except Exception as error:
        traceback.print_exc()
        print(error)

        result['status'] = False
        result['error'] = error
        return result


def send_personalized_emails(console=None, progress_status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    data_list = get_details_for_emails()
    sender_email = os.environ.get("EMAIL_ADDRESS")
    password = os.environ.get("EMAIL_PASSWORD")
    connection = get_database_connection()
    cursor = connection.cursor()
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, password=password)
            email_sent = 0
            index = 0
            for (item_id, reciever_email, subject, content, status, business_name) in data_list:
                if "null" in [item_id, reciever_email, subject, content] :
                    if console:
                        console.print(f"[cyan]⚠ Not Enough Data For [yellow]{business_name}")
                    continue
                elif status == "SUCCESS":
                    if console:
                        console.print(f"[cyan]⚠ Personalized Mail Is Already Sent To [yellow]{business_name}[cyan].")
                    continue
                em = EmailMessage()
                em["From"] = sender_email
                #em["To"] = "manoj.thunderviz@gmail.com,vigneshrgm962950@gmail.com"
                em["To"] = "vigneshrgm962950@gmail.com"

                em["Subject"] = subject

                embedded_email_content = generate_embedded_email_content(content)
                em.set_content(embedded_email_content, subtype='html')
                res = smtp.send_message(em)

                if len(res) == 0:  # check
                    email_sent+=1
                    cursor.execute(f"UPDATE leads SET status = 'SUCCESS' WHERE lead_id={item_id}")
                    connection.commit()
                    if console:
                        console.print(
                            f"[green]🎉  Personalized Email Successfully Sent To {reciever_email} - [yellow]{business_name}")
                else:
                    if console:
                        console.print(
                            f"[red]🚨  Personalized Email Faild To Sent To {reciever_email} - [yellow]{business_name}")
                if progress_status:
                    progress_status.update(
                        f"[bold yellow]Sending Personalized Email... [green]({index + 1}\{len(data_list)}) done:{email_sent}")
                index += 1
            cursor.close()
            connection.close()

            result['time_taken'] = time.time() - result['time_taken']
            result["network_usage"] = get_network_usage() - result["network_usage"]
            return result
    except Exception as error:
        cursor.close()
        connection.close()
        traceback.print_exc()
        print(error)

        result['status'] = False
        result['error'] = error
        return result
