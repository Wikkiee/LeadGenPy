import asyncio
import re
import time
import traceback

import aiohttp
import requests
from bs4 import BeautifulSoup

from Configs.database import get_database_connection
from Utils.resource_calculator import get_network_usage
from rich.console import Console

async def scrape_business_email(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    try:
        connections = get_database_connection()
        cursor = connections.cursor()
        cursor.execute(
            "SELECT lead_id,business_name,website_url from leads WHERE website_url != 'null' AND business_email = 'null'  ")
        web_url_list = cursor.fetchall()

        email_found = 0

        async def t(url,business_name):
            console.print(f'[yellow] Sending request to {url}')
            async with aiohttp.ClientSession() as session:
                async with session.get(url=f'https://{url}') as response:
                    text =  await response.text()
                    soup = BeautifulSoup(text, 'lxml')
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                    emails = re.findall(email_pattern, soup.text)
                    if emails:
                        _result = re.sub(r'\d', '', emails[0])
                        if console:
                            console.print(
                                f"[green]🎉 [bold]{business_name}[reset] [green]Email Scraped successfully [bold]{_result}[reset] [yellow]")
                    else:
                        if console:
                            console.print(
                                    f"[red]🚨 [bold]{business_name}[reset] [red]Email Not Found! ")
        tasks = []
        for index,item in enumerate(web_url_list):
            lead_id, business_name, url = item

            task = asyncio.create_task(t(url,business_name))
            tasks.append(task)

        await asyncio.gather(*tasks)
            # response = requests.get(url)

                # cursor.execute("""
                #     UPDATE leads
                #     SET business_email = %s
                #     WHERE lead_id = %s
                # """, (_result, lead_id))

        if status:
                status.update(
                    f"[bold yellow]Scrapping Business Email... [green]({index+1}/{len(web_url_list)}) done:{email_found}")

        connections.commit()
        cursor.close()
        connections.close()

        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result
    except Exception as error:
        traceback.print_exc()
        print(error)

        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result


if __name__ == "__main__":
    console = Console(width=40)
    result = asyncio.run( scrape_business_email(console))
    console.print(
        f"[green]🎉 Completed scrape_business_email! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")


#
#
#
# import asyncio
# import re
# import time
# import traceback
#
# import aiohttp
# import requests
# from bs4 import BeautifulSoup
#
# from Configs.database import get_database_connection
# from Utils.resource_calculator import get_network_usage
# from rich.console import Console
#
# async def scrape_business_email(console=None, status=None):
#     result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}
#
#     try:
#         connections = get_database_connection()
#         cursor = connections.cursor()
#         cursor.execute(
#             "SELECT lead_id,business_name,website_url from leads WHERE website_url != 'null' AND business_email = 'null'  ")
#         web_url_list = cursor.fetchall()
#
#         email_scrape_set = {'items_found':0}
#         async def scrape_email(url,business_name):
#             console.print(f'[yellow]🌐 Sending request to {url}')
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url=f'https://{url}') as response:
#                     text =  await response.text()
#                     soup = BeautifulSoup(text, 'lxml')
#                     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
#                     emails = re.findall(email_pattern, soup.text)
#
#                     if emails:
#                         email_scrape_set['items_found'] += 1
#                         _result = re.sub(r'\d', '', emails[0])
#                         cursor.execute("""
#                             UPDATE leads
#                             SET business_email = %s
#                             WHERE lead_id = %s
#                         """, (_result, lead_id))
#                         if console:
#                             console.print(
#                                 f"[green]🎉 [bold]{business_name}[reset] [green]Email Scraped successfully [bold]{_result}[reset] [yellow]")
#                     else:
#                         if console:
#                             console.print(
#                                     f"[red]🚨 [bold]{business_name}[reset] [red]Email Not Found! ")
#         tasks = []
#         for index,item in enumerate(web_url_list):
#             lead_id, business_name, url = item
#
#             task = asyncio.create_task(scrape_email(url,business_name))
#             tasks.append(task)
#
#
#         await asyncio.gather(*tasks)
#         console.print(f"[blue]🗃️ Total Emails Found : {email_scrape_set['items_found']}")
#
#                 # cursor.execute("""
#                 #     UPDATE leads
#                 #     SET business_email = %s
#                 #     WHERE lead_id = %s
#                 # """, (_result, lead_id))
#
#
#
#         connections.commit()
#         cursor.close()
#         connections.close()
#
#         result['time_taken'] = time.time() - result['time_taken']
#         result["network_usage"] = get_network_usage() - result["network_usage"]
#         return result
#     except Exception as error:
#         traceback.print_exc()
#         print(error)
#
#         result['time_taken'] = time.time() - result['time_taken']
#         result["network_usage"] = get_network_usage() - result["network_usage"]
#         return result
#
#
# if __name__ == "__main__":
#     console = Console(width=100)
#     result = asyncio.run( scrape_business_email(console))
#     console.print(
#         f"[green]🎉 Completed scrape_business_email! -  \n[yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
#
#

