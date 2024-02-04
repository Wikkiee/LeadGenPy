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






async def scrape_organization_number(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    connections = get_database_connection()
    cursor = connections.cursor()
    cursor.execute("SELECT lead_id,website_url,business_name from leads WHERE website_url != 'null' and leads.lead_id not in (select allabolag.lead_id from allabolag) ")
    lead_data_list = cursor.fetchall()

    org_no_scrape_set = {'items_found':0,"total_items_visited":0}

    if not lead_data_list:
        console.print(f'[yellow]🗃️  The leads Table Is Empty !.')
        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result
    async def scrape_organization_number_asynchronously(url,lead_id,business_name):
        console.print(f'[yellow]🌐 Sending request to {url} -[reset] [blue][bold][{business_name}]')
        org_no_scrape_set["total_items_visited"] += 1

        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
            , 'Accept-Language': 'en-US,en;q=0.9'
        }
        try:

            async with session.get(url=f'https://{url}', headers=headers, ssl=False) as response:
                if response.status != 200:
                    print(
                        f"[ {business_name} ] Got status code other than the 200: -> status code : {response.status} -> link : {url}")
                    return
                response = await response.text()
                home_page_source = BeautifulSoup(response, 'lxml')

                # Pattern for XXXXXX-XXXX format
                def extract_org_number(page):
                    org_number_pattern = r'\b\d{6}-\d{4}\b'
                    matches = re.findall(org_number_pattern, page.text)
                    return matches

                org_number = extract_org_number(home_page_source)
                if org_number:
                    org_no_scrape_set['items_found'] += 1
                    if console:
                        console.print(
                            f"[green]🎉 [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({org_no_scrape_set['items_found']}/{len(lead_data_list)})")
                    if status:
                        status.update(
                            f"[bold yellow]Scrapping Organization Number... [green]({index + 1}\{len(lead_data_list)}) done:{org_no_scrape_set['items_found']}")
                    cursor.execute(f"""
                                    INSERT INTO 
                                    allabolag(lead_id,organization_number	)
                                    VALUES({lead_id},{org_number[0].replace('-', '')})
        
                            """)
                    return

                links_list = []
                for i in home_page_source.find_all("a", href=True):
                    links_list.append(i['href'])
                ending_words = ['privacy', 'policy', 'terms', 'Integritetspolicy']
                pattern_links = re.compile(r'https?://\S*?(' + '|'.join(ending_words) + r')\S*', re.IGNORECASE)
                matches_links = [link for link in links_list if pattern_links.search(link)]

                for link in matches_links:
                    try:
                        url_pattern = re.compile(r'^(https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:(?!\.pdf|\.docx|\.jpg|\.png|\.gif)\S)*$')
                        if not url_pattern.match(link):
                            continue
                        if not link.startswith("http://") and not link.startswith("https://"):
                            link = "https://" + link
                        async with session.get(url=link, headers=headers, ssl=False) as res:
                            if res.status != 200:
                                print(f"[ {business_name} ] Got status code other than the 200: -> status code : {res.status} -> link : {link}")
                                break
                            res = await res.text()

                            soup = BeautifulSoup(res, 'lxml')
                            org_number = extract_org_number(soup)
                            if org_number:
                                org_no_scrape_set['items_found'] += 1
                                if console:
                                    console.print(
                                        f"[green]🎉 [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({org_no_scrape_set['items_found']}/{len(lead_data_list)})")
                                if status:
                                    status.update(
                                        f"[bold yellow]Scrapping Organization Number... [green]({index}\{len(lead_data_list)}) done:{org_no_scrape_set['items_found']}")
                                cursor.execute(f"""
                                            INSERT INTO 
                                            allabolag(lead_id,organization_number	)
                                            VALUES({lead_id},{org_number[0].replace('-', '')})
                                            """)
                                break

                    except Exception as eror:
                        print(f"[ {business_name} ] Got an error on inner try block: -> error : {eror} -> {link}")
                        traceback.print_exc()
                else:
                    if console:
                        console.print(
                            f"[red]🚨 [bold]{business_name}[reset] [red]Organization Number Not Found! [yellow]({org_no_scrape_set['items_found']}/{len(lead_data_list)})")


        except aiohttp.ClientConnectionError as connection_error:
            if console:
                console.print(
                    f"🚨 [yellow][Connection Error][reset] [red][bold]{business_name}[reset] [red]Failed to scrape email - Error: {connection_error}! -> {url}")
                return
        except Exception as e:
            if console:
                console.print(
                    f"🚨 [yellow][Exception][reset] [red][bold]{business_name}[reset] [red]Failed to scrape email - Error: {e}! -> {url}")
                return


    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120), trust_env=True) as session:
        tasks = []
        for index,url in enumerate(lead_data_list):
            lead_id, url, business_name = url[0], url[1], url[2]
            task = asyncio.create_task(scrape_organization_number_asynchronously(url ,lead_id,business_name))
            tasks.append(task)
        await asyncio.gather(*tasks)
        if status:
            status.update(
                f"[bold yellow]Scrapping Organization Number... [green]({index}\{len(lead_data_list)}) done:{org_found}")
    cursor.execute("SELECT COUNT(lead_id) as result FROM leads")
    web_url_not_found_list = cursor.fetchall()
    console.print(f"\n[blue]🗃️ Total Organiztion Numbers Found : {org_no_scrape_set['items_found']} | Items searched : {org_no_scrape_set['total_items_visited']} | Ignored Items (Check DB) : {web_url_not_found_list[0][0] - org_no_scrape_set['total_items_visited']}")

    connections.commit()
    cursor.close()
    connections.close()
    result['time_taken'] = time.time() - result['time_taken']
    result["network_usage"] = get_network_usage() - result["network_usage"]
    return result

if __name__ == '__main__':
    console = Console()
    result = asyncio.run(scrape_organization_number(console))
    console.print(f"[green]🎉 Completed scrape_organization_number! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")














async def scrape_organization_number1(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    connections = get_database_connection()
    cursor = connections.cursor()
    cursor.execute("SELECT lead_id,website_url,business_name from leads WHERE website_url != 'null' ")
    url_list = cursor.fetchall()

    org_found = 0
    for index,url in enumerate(url_list):
        lead_id, url, business_name = url[0], url[1], url[2]
        response = requests.get(f"https://{url}")
        home_page_source = BeautifulSoup(response.text, 'lxml')

        # Pattern for XXXXXX-XXXX format
        def extract_org_number(page):
            org_number_pattern = r'\b\d{6}-\d{4}\b'
            matches = re.findall(org_number_pattern, page.text)
            return matches

        org_number = extract_org_number(home_page_source)
        if org_number:
            org_found += 1
            if console:
                console.print(
                    f"[green]🎉 [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({org_found}/{len(url_list)})")
            if status:
                status.update(f"[bold yellow]Scrapping Organization Number... [green]({index+1}\{len(url_list)}) done:{org_found}")
            cursor.execute(f"""
                    INSERT INTO 
                    allabolag(lead_id,organization_number	)
                    VALUES({lead_id},{org_number[0].replace('-', '')})

            """)
            connections.commit()
            continue

        links_list = []
        for i in home_page_source.find_all("a", href=True):
            links_list.append(i['href'])
        ending_words = ['privacy', 'policy', 'terms', 'Integritetspolicy']
        pattern_links = re.compile(r'https?://\S*?(' + '|'.join(ending_words) + r')\S*', re.IGNORECASE)
        matches_links = [link for link in links_list if pattern_links.search(link)]

        for link in matches_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'lxml')
            org_number = extract_org_number(soup)
            if org_number:
                org_found += 1
                if console:
                    console.print(
                        f"[green]🎉 [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({org_found}/{len(url_list)})")
                if status:
                    status.update(
                        f"[bold yellow]Scrapping Organization Number... [green]({index}\{len(url_list)}) done:{org_found}")
                cursor.execute(f"""
                    INSERT INTO 
                    allabolag(lead_id,organization_number	)
                    VALUES({lead_id},{org_number[0].replace('-', '')})
                    """)
                break
        else:
            if console:
                console.print(
                    f"[red]🚨 [bold]{business_name}[reset] [red]Organization Number Not Found! [yellow]({org_found}/{len(url_list)})")

        if status:
            status.update(
                f"[bold yellow]Scrapping Organization Number... [green]({index}\{len(url_list)}) done:{org_found}")
    connections.commit()
    cursor.close()
    connections.close()

    result['time_taken'] = time.time() - result['time_taken']
    result["network_usage"] = get_network_usage() - result["network_usage"]
    return result










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
#         email_found = 0
#
#         async def t(url,business_name):
#             console.print(f'[yellow] Sending request to {url}')
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(url=f'https://{url}') as response:
#                     text =  await response.text()
#                     soup = BeautifulSoup(text, 'lxml')
#                     email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
#                     emails = re.findall(email_pattern, soup.text)
#                     if emails:
#                         _result = re.sub(r'\d', '', emails[0])
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
#             task = asyncio.create_task(t(url,business_name))
#             tasks.append(task)
#
#         await asyncio.gather(*tasks)
#             # response = requests.get(url)
#
#                 # cursor.execute("""
#                 #     UPDATE leads
#                 #     SET business_email = %s
#                 #     WHERE lead_id = %s
#                 # """, (_result, lead_id))
#
#         if status:
#                 status.update(
#                     f"[bold yellow]Scrapping Business Email... [green]({index+1}/{len(web_url_list)}) done:{email_found}")
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
#     console = Console(width=40)
#     result = asyncio.run( scrape_business_email(console))
#     console.print(
#         f"[green]🎉 Completed scrape_business_email! [yellow]timeTaken:[reset]{result['time_taken']:.2f}sec [yellow]networkUsage:[reset]{(result['network_usage'] / 1000):.2f}kilobytes")
#
#
#
#
#










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

