import re
import time
import traceback

import requests
from bs4 import BeautifulSoup

from Configs.database import get_database_connection
from Utils.resource_calculator import get_network_usage
from rich.console import Console

def scrape_business_email(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    try:
        connections = get_database_connection()
        cursor = connections.cursor()
        cursor.execute(
            "SELECT lead_id,business_name,website_url from leads WHERE website_url != 'null' AND business_email = 'null'  ")
        web_url_list = cursor.fetchall()

        email_scrape_set = {'items_found': 0, 'total_searched_items': 0}

        for index,item in enumerate(web_url_list):
            lead_id, business_name, url = item
            console.print(f'[yellow]🌐 Sending request to {url} -[reset] [blue][bold][{business_name}]')
            email_scrape_set['total_searched_items'] += 1
            # response = requests.get(url)
            try:
                response = requests.get(f"https://{url}")
                soup = BeautifulSoup(response.text, 'lxml')
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                emails = re.findall(email_pattern, soup.text)
                if emails:
                    email_scrape_set['items_found'] += 1
                    _result = re.sub(r'\d', '', emails[0])
                    if console:
                        console.print(
                            f"[green]✅ [bold]{business_name}[reset] [green]Email Scraped successfully [bold]{_result}[reset] [yellow]({email_found}/{len(web_url_list)})")
                    cursor.execute("""
                        UPDATE leads
                        SET business_email = %s
                        WHERE lead_id = %s
                    """, (_result, lead_id))
                else:
                    if console:
                        console.print(
                            f"[red]❌ [bold]{business_name}[reset] [red]Email Not Found! [yellow]({email_scrape_set['items_found']}/{len(web_url_list)})")
                if status:
                    status.update(
                        f"[bold yellow]Scrapping Business Email... [green]({index+1}/{len(web_url_list)}) done:{email_found}")
            except Exception:
                pass

        connections.commit()
        cursor.close()
        connections.close()

        cursor.execute("SELECT COUNT(lead_id) as result FROM leads")
        web_url_not_found_list = cursor.fetchall()
        console.print(f"[blue]🗃️ Total Emails Found : {email_scrape_set['items_found']} | Items searched : {email_scrape_set['total_searched_items']} | Ignored Items (Check DB) : {web_url_not_found_list[0][0] - email_scrape_set['total_searched_items']}")
        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result
    except Exception as error:
        traceback.print_exc()
        print(error)

        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result

if __name__ == '__main__':
    console = Console()
    scrape_business_email(console)