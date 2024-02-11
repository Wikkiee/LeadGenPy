import asyncio
import os
import re
import threading
import time
import traceback

import multiprocessing
import aiohttp
import requests
import selenium.common.exceptions
from bs4 import BeautifulSoup
from rich.markdown import Markdown
from rich.table import Table
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from Configs.database import get_database_connection
from Utils.create_driver import createDriver
from Utils.resource_calculator import get_network_usage
from Utils.store import generate_json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_each_item_parallely(index,link,extracted_data_list,google_data_stats):
    # options = webdriver.ChromeOptions()
    # driver = webdriver.Remote(command_executor='http://localhost:4444', options=options)
    driver = createDriver()
    driver.get(link)
    page_down_selection_element = driver.find_element(By.CSS_SELECTOR,
                            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf")
    page_down_selection_element.send_keys(Keys.PAGE_DOWN)
    home_page_source = driver.page_source
    home_page_soup: BeautifulSoup = BeautifulSoup(home_page_source, 'lxml')

    business_data = get_business_details(home_page_soup, driver)
    business_data["google_map_url"] = link

    extracted_data_list.append(business_data)
    with google_data_stats.get_lock():
        google_data_stats.value += 1
    driver.close()
def scrape_data_from_google_map(industry_name="restaurant", location="sweden", limit=2, task_bar=None, progress=None,
                                console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    query = f'{industry_name} in {location}' if industry_name and location else f'{industry_name} {location}'
    try:
        driver = createDriver()
        if status:
            status.update("[bold yellow]Scrapping Data From The Google Map... [green](opening GoogleMap)")
        driver.get(f'https://www.google.com/maps/search/{query}')
        scrollable_table = driver.find_element(By.CSS_SELECTOR,"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")
        loop_breaker = 0

        if status:
            status.update("[bold yellow]Scrapping Data From The Google Map... [green](Fetching Business In GoogleMap)")
        while True:
            if loop_breaker == 2:
                break
            loop_breaker += 1
            scrollable_table.send_keys(Keys.END)  # MAX - 120 Items
            if driver.find_elements(By.CSS_SELECTOR,
                                    "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t > div.m6QErb.tLjsW.eKbjU > div > p > span > span"):
                if driver.find_elements(
                        By.CSS_SELECTOR,
                        "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.RiRi5e.Hk4XGb.Yt0HSb > div > button"):
                    driver.find_element(
                        By.CSS_SELECTOR,
                        "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.RiRi5e.Hk4XGb.Yt0HSb > div > button").click()
                break

        soup = BeautifulSoup(driver.page_source, 'lxml')
        res = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div:not(.TFQHme):not(.m6QErb) > div > a")

        links = [link.attrs['href'] for link in res]
    except Exception as error:
        traceback.print_exc()
        print(error)

        result['status'] = False
        result['error'] = error
        return result

    manager = multiprocessing.Manager()
    google_data_stats = multiprocessing.Value('i',0)
    shared_extracted_data_list = manager.list()

    driver.close()

    processes = []
    total_links = len(links)
    print('Total No.Of Links:',total_links)
    for index,link in enumerate(links):
        if index == limit:
            break
        try:

            while len(processes) >= 4:
                    processes = [process for process in processes if process.is_alive()]

                    if (len(processes)>=4):
                        continue
                    break

            if status:
                    status.update(f"[yellow]🚨 [bold]Scraping data from google map \n[green]Completed: [{index+1}] | Remaining: [{total_links - (index + 1)}]")

            process = multiprocessing.Process(target=scrape_each_item_parallely,args=(index,link,shared_extracted_data_list,google_data_stats))
            process.start()

            processes.append(process)


            # if status: status.update(f"[bold yellow]Scrapping Data From The Google Map... [green]({google_data_stats.value}/{len(links)}) done:{len(shared_extracted_data_list)}")
        except Exception as error:
            traceback.print_exc()
            print(error)

            result['status'] = False
            result['error'] = error
            return result


        if progress:
            progress.update(task_bar, advance=1)
    for process in processes:
        process.join()

    generate_json(shared_extracted_data_list)
    if progress:
        progress.stop()
    if console:
        console.print(
            f"[green]Scraped [cyan bold]{len(shared_extracted_data_list)}[reset] [green]{industry_name} Data Successfully!\n")
    result['time_taken'] = time.time() - result['time_taken']
    result["network_usage"] = get_network_usage() - result["network_usage"]
    return result


def get_business_details(home_page_soup: BeautifulSoup, driver: webdriver.Chrome):
    business_data = {
        "business_name": "null",
        "business_address": "null",
        "business_email": "null",
        "mobile_number": "null",
        "website_url": "null",
        "business_category": "null",
        "ratings": "null",
        "review_counts": "null",
        "top_review_1": "null",
        "top_review_2": "null",
        "top_review_3": "null",
        "google_map_url": "null",
        "personalized_email_subject": "null",
        "personalized_email_content": "null",
        "status": "PENDING",
    }
    base_selector = 9

    try:
        for i in range(7, 10):
            if len(home_page_soup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({i}) > div')) > 1:
                base_selector = i
                break

        length = home_page_soup.select(
            f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div')
        name_selector = home_page_soup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1")
        category_selector = home_page_soup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div:nth-child(2) > span > span > button")
        ratings_selector = home_page_soup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(1) > span:nth-child(1)")
        reviews_selector = home_page_soup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(2) > span > span")
        business_data["business_name"] = name_selector[0].text if name_selector else "null"

        for i in range(3, len(length)):
            if home_page_soup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') or home_page_soup.select(
                f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img'):
                src_link = home_page_soup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img')[
                    0].attrs['src'] if home_page_soup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') else \
                    home_page_soup.select(
                        f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img')[
                        0].attrs['src']
                if src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png":

                    business_data["business_address"] = home_page_soup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[
                        0].text if home_page_soup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else \
                        home_page_soup.select(
                            f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[
                            0].text
                elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png":

                    business_data["website_url"] = home_page_soup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[
                        0].text if home_page_soup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else \
                        home_page_soup.select(
                            f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[
                            0].text
                elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png":

                    business_data["mobile_number"] = home_page_soup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[
                        0].text if home_page_soup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else \
                        home_page_soup.select(
                            f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[
                            0].text

        business_data["business_category"] = category_selector[0].text if category_selector else "null"
        business_data["ratings"] = ratings_selector[0].text if ratings_selector else "null"
        business_data["review_counts"] = reviews_selector[0].text[1:-1] if reviews_selector else "null"

        top_three_review_loop_break_index = 1
        for i in range(30, 60):
            if top_three_review_loop_break_index > 3:
                break

            reviewer_name = home_page_soup.select(
                f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div > div > div:nth-child(2) > div > button > div")

            if len(reviewer_name) > 0:
                try:

                    try:
                        try:
                            load_full_review_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR,f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div > span > button ")))
                            load_full_review_button.click()
                            home_page_soup = BeautifulSoup(driver.page_source, 'lxml')
                        except:
                            t = driver.find_element(By.CSS_SELECTOR,
                                                    "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf")
                            t.send_keys(Keys.PAGE_DOWN)
                            load_full_review_button = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((
                                                                                                                By.CSS_SELECTOR,
                                                                                                                f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div > span > button ")))
                            load_full_review_button.click()
                            home_page_soup = BeautifulSoup(driver.page_source, 'lxml')
                    except Exception as e:
                        print(f"{reviewer_name} - More not found")

                    review_content = home_page_soup.select(f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div > span ")
                    business_data[f"top_review_{top_three_review_loop_break_index}"] = f"Review by {reviewer_name[0].text} \n{review_content[0].text}"
                    top_three_review_loop_break_index += 1
                except selenium.common.exceptions.ElementNotInteractableException as error:
                    print("Error - From scrapper.py")

        return business_data
    except Exception as error:
        traceback.print_exc()
        print(error)

        return business_data



async def scrape_business_email(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    try:
        connections = get_database_connection()
        cursor = connections.cursor()
        cursor.execute(
            "SELECT lead_id,business_name,website_url from leads WHERE website_url != 'null' AND business_email = 'null'  ")
        web_url_list = cursor.fetchall()

        email_scrape_set = {'items_found':0,'total_searched_items':0}
        async def scrape_email_asynchronously(session,url,lead_id,business_name):
            console.print(f'[yellow]🌐 Sending request to {url} -[reset] [blue][bold][{business_name}]')
            email_scrape_set['total_searched_items'] += 1
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
                    , 'Accept-Language': 'en-US,en;q=0.9'
                }
                async with session.get(url=f'https://{url}',headers=headers,ssl=False) as response:

                    if response.status != 200:
                        print(f"FAILED 404 -> {url}")
                        return
                    text =  await response.text()

                    soup = BeautifulSoup(text, 'lxml')
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
                    emails = re.findall(email_pattern, soup.text)
                    if emails:
                        email_scrape_set['items_found'] += 1
                        _result = re.sub(r'\d', '', emails[0])
                        cursor.execute("""
                            UPDATE leads
                            SET business_email = %s
                            WHERE lead_id = %s
                        """, (_result, lead_id))
                        if console:
                            console.print(
                                f"[green]🎉 [bold]{business_name}[reset] [green]Email Scraped successfully [bold]{_result}[reset] [yellow] -> Found:{email_scrape_set['items_found']}")
                            return
                    else:
                        if console:
                            console.print(f"[red]🚨 [bold]{business_name}[reset] [red]Email Not Found! -> {url}")
                            return
            except Exception as connection_error:
                if console:
                    console.print(f"[red]🚨 [bold]{business_name}[reset] [red]Failed to scrape email - Error: {connection_error}! -> {url}")
                    return

        tasks = []

        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120),trust_env=True) as session:
            for index,item in enumerate(web_url_list):
                lead_id, business_name, url = item
                try:
                    task = asyncio.create_task(scrape_email_asynchronously(session,url,lead_id,business_name))
                    tasks.append(task)
                except Exception as err:
                    print("for loop error")
                    print(err)

            await asyncio.gather(*tasks)
        cursor.execute("SELECT COUNT(lead_id) as result FROM leads")
        web_url_not_found_list = cursor.fetchall()
        console.print(f"[blue]🗃️ Total Emails Found : {email_scrape_set['items_found']} | Items searched : {email_scrape_set['total_searched_items']} | Ignored Items (Check DB) : {web_url_not_found_list[0][0] - email_scrape_set['total_searched_items']}")
        if status:
                status.update(
                    f"[bold yellow]Scrapping Business Email... [green]({index+1}/{len(web_url_list)}) done:{email_scrape_set['items_found']}")

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


async def scrape_organization_number(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    connections = get_database_connection()
    cursor = connections.cursor()
    cursor.execute(
        "SELECT lead_id,website_url,business_name from leads WHERE website_url != 'null' and leads.lead_id not in (select allabolag.lead_id from allabolag) ")
    lead_data_list = cursor.fetchall()

    org_no_scrape_set = {'items_found': 0, "total_items_visited": 0}

    if not lead_data_list:
        console.print(f'[yellow]🗃️  The leads Table Is Empty !.')
        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result

    async def scrape_organization_number_asynchronously(url, lead_id, business_name):
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
                        url_pattern = re.compile(
                            r'^(https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:(?!\.pdf|\.docx|\.jpg|\.png|\.gif)\S)*$')
                        if not url_pattern.match(link):
                            continue
                        if not link.startswith("http://") and not link.startswith("https://"):
                            link = "https://" + link
                        async with session.get(url=link, headers=headers, ssl=False) as res:
                            if res.status != 200:
                                print(
                                    f"[ {business_name} ] Got status code other than the 200: -> status code : {res.status} -> link : {link}")
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
        for index, url in enumerate(lead_data_list):
            lead_id, url, business_name = url[0], url[1], url[2]
            task = asyncio.create_task(scrape_organization_number_asynchronously(url, lead_id, business_name))
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


# Allabolag details scraper

async def scrape_allabolag_details(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT DISTINCT allabolag_id,organization_number FROM allabolag WHERE registered_name="null"')
    allabolag_data = cursor.fetchall()
    if len(allabolag_data) == 0:
        if console:
            console.print("\n[green]It Is Already Uptodate!\n", justify="center")
        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result

    allabolag_table = Table(title="",width=100,expand=True)

    allabolag_table.add_column("Registered Name", justify="center", style="cyan", no_wrap=True)
    allabolag_table.add_column("Ceo Name", justify="center",style="magenta",no_wrap=True)
    allabolag_table.add_column("Business", justify="center", style="green",no_wrap=True)
    allabolag_table.add_column("Revenue", justify="center", style="green",no_wrap=True)
    allabolag_table.add_column("Registration", justify="center", style="green",no_wrap=True)
    allabolag_table.add_column("Employees", justify="center", style="green",no_wrap=True)

    headcount_table = Table(title="",width=100)
    revenue_track_table = Table(title="",width=100)
    headcount_table.add_column("Registered Name", justify="right", style="cyan", no_wrap=True)
    revenue_track_table.add_column("Registered Name", justify="right", style="cyan", no_wrap=True)

    for year in range(2022, 2016, -1):
        headcount_table.add_column(f"Head Count - {year}", justify="right", style="cyan", )
        revenue_track_table.add_column(f"Revenue Track - {year}", justify="right", style="cyan", )
    if console:
        console.print("*note: table will be listed once everything is extracted!", justify="center")



    allabolag_scraped_stats_set = {'items_found':0,'total_no_of_items_searched':0}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36'
        , 'Accept-Language': 'en-US,en;q=0.9'
    }
    async def scrape_allabolag_details_asynchronously(organization_number, allabolag_id):
        allabolag_scraped_stats_set['total_no_of_items_searched'] += 1
        console.print(f'[yellow]🌐 Sending request to https://www.allabolag.se/{organization_number} -[reset] [blue][bold][{allabolag_id}]')

        try:
            async with session.get(url=f"https://www.allabolag.se/{organization_number}", headers=headers, ssl=False) as res:
                res = await res.text()
                soup = BeautifulSoup(res, 'lxml')
                temp = 0
                ceo_name = "null"

                if soup.select('#company-card_overview > div > div:nth-child(1) > dl > dd:nth-child(2) > a '):
                    ceo_name = soup.select('#company-card_overview > div > div:nth-child(1) > dl > dd:nth-child(2) > a ')[
                        0].text.strip()
                    temp = 2

                registered_name = soup.select(
                    '#company-card_container > div > div:nth-child(1) > div:nth-child(1) > div > div > div > h1')[
                    0].text.strip()
                revenue = soup.select(
                    "#company-card_overview > div.accountfigures_container > div.company-account-figures > div.table__container > table > tr:nth-child(1) > td:nth-child(2) ")[
                              0].text.strip() + " 000"
                year_of_registeration = soup.select(
                    f"#company-card_overview > div.cc-flex-grid > div:nth-child(1) > dl > dd:nth-child({8 + temp})")[
                    0].text.strip()
                type_of_business = soup.select(
                    f"#company-card_overview > div.cc-flex-grid > div:nth-child(1) > dl > dd:nth-child({2 + temp})")[
                    0].text.strip()
                # company-card_overview > div.cc-flex-grid > div:nth-child(1) > dl > dd:nth-child(2)
                try:
                    async with session.get(url=f"https://www.allabolag.se/{organization_number}/bokslut", headers=headers, ssl=False) as res:
                        res = await res.text()
                        soup = BeautifulSoup(res, 'lxml')
                        number_of_employees = soup.select("#bokslut > div > div:nth-child(7) > table > tbody > tr:nth-child(1) > td ")[
                            0].text.strip()
                        # print(number_of_employees)
                        # revenue_list = [x.text.strip() + " 000" for x in
                        #                 soup.select("#bokslut > div> div > table > tbody > tr")[24].select('td')[0:6] if 1 == 1]
                        # headcount_list = [int(x.text.strip()) for x in
                        #                   soup.select("#bokslut > div> div > table > tbody > tr")[25].select('td')[0:6] if 1 == 1]
                        headcount_list = []
                        revenue_list = []
                        for headcount in soup.select("#bokslut > div> div > table > tbody > tr")[25].select('td')[0:6]:
                            headcount_list.append(int(headcount.text.strip()) if headcount.text.strip().isnumeric() else 0)
                        for revenues in soup.select("#bokslut > div> div > table > tbody > tr")[24].select('td')[0:6]:
                            revenue_list.append(revenues.text.strip()+" 000" if revenues and revenues.text.strip().isspace() != True else "0 000")

                        revenue_list.insert(0, allabolag_id)
                        headcount_list.insert(0, allabolag_id)

                        headcount_list += [0] * (7 - len(headcount_list))
                        revenue_list += ["0 000"] * (7 - len(revenue_list))
                        allabolag_table.add_row(registered_name, ceo_name, type_of_business, revenue, year_of_registeration,
                                                number_of_employees)
                        revenue_track_table.add_row(registered_name, str(revenue_list[1]), str(revenue_list[2]), str(revenue_list[3]),
                                                    str(revenue_list[4]),
                                                    str(revenue_list[5]), str(revenue_list[6]))
                        headcount_table.add_row(registered_name, str(headcount_list[1]), str(headcount_list[2]), str(headcount_list[3]),
                                                str(headcount_list[4]), str(headcount_list[5]), str(headcount_list[6]))

                        cursor.execute("""
                            UPDATE allabolag
                            SET registered_name = %s,
                                ceo_name = %s,
                                type_of_business = %s,
                                revenue = %s,
                                number_of_employees = %s,
                                year_of_registeration = %s
                            WHERE allabolag_id = %s
                        """, (registered_name, ceo_name, type_of_business, revenue, number_of_employees, year_of_registeration,
                              allabolag_id))
                        cursor.execute("""
                            INSERT INTO revenue_track
                            (allabolag_id, revenue_track_2022, revenue_track_2021, revenue_track_2020, revenue_track_2019, revenue_track_2018, revenue_track_2017)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)""", revenue_list)
                        cursor.execute("""
                            INSERT INTO headcounts
                            (allabolag_id,headcount_2022,headcount_2021,headcount_2020,headcount_2019,headcount_2018,headcount_2017)
                            VALUES(%s,%s,%s,%s,%s,%s,%s)""", headcount_list)

                        allabolag_scraped_stats_set['items_found'] += 1
                        if console:
                            console.print(
                                f"[green]🎉 [bold]{registered_name}[reset][green]'s  Allabolag Data Are Extracted Successfully! | ({allabolag_scraped_stats_set['items_found']}/{len(allabolag_data)})")
                        if status:
                            status.update(f"[bold yellow]Scrapping Allabolag Details... [green]({allabolag_scraped_stats_set['items_found']+1}/{len(allabolag_data)}) done:{allabolag_scraped_stats_set['items_found']} | ")

                except Exception as err:
                    if console:
                        console.print(f"[red]🚨 [bold] Allabolag ID:{allabolag_id}[reset] [red] Is Failed To Scrape Details | Error : {err} | URL : https://www.allabolag.se/{organization_number}/bokslut")
        except Exception as error:
            console.print(
                f"[red]🚨 [bold] Allabolag ID:{allabolag_id}[reset] [red] Is Failed To Scrape Details | Error : {error} | URL : https://www.allabolag.se/{organization_number}")

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120), trust_env=True) as session:
        tasks = []
        for allabolag_id, organization_number in allabolag_data:
            task = asyncio.create_task(scrape_allabolag_details_asynchronously(organization_number, allabolag_id))
            tasks.append(task)
        await asyncio.gather(*tasks)

    if console:
        # console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeAllabolag",
                      justify="center")
        console.print(Markdown("---"))
        console.print(allabolag_table)
        console.print(revenue_track_table)
        console.print(headcount_table)
    connection.commit()
    cursor.close()
    connection.close()

    console.print(f"\n[blue]🗃️  Total No.of Allabolag Data Found : {allabolag_scraped_stats_set['items_found']} | Items searched : {allabolag_scraped_stats_set['total_no_of_items_searched']} ")

    result['time_taken'] = time.time() - result['time_taken']
    result["network_usage"] = get_network_usage() - result["network_usage"]
    return result
