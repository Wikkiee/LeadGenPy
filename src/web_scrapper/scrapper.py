import os
import re
import time
import traceback

import requests
import selenium.common.exceptions
from selenium import webdriver
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

def scrape_data_from_google_map(industry_name="restaurant", location="sweden", limit=2, task_bar=None, progress=None,
                                console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    query = f'{industry_name} in {location}' if industry_name and location else f'{industry_name} {location}'
    try:
        driver = createDriver()
        if status:
            status.update("[bold yellow]Scrapping Data From The Google Map... [green](opening GoogleMap)")
        driver.get(f'https://www.google.com/maps/search/{query}')
        scrollable_table = driver.find_element(By.CSS_SELECTOR,
                                               "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")
        loop_breaker = 0

        if status:
            status.update("[bold yellow]Scrapping Data From The Google Map... [green](Fetching Business In GoogleMap)")
        while True:
            if loop_breaker == 2:
                pass
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
        res = soup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div:not(.TFQHme):not(.m6QErb) > div > a")

        links = [link.attrs['href'] for link in res]
    except Exception as error:
        traceback.print_exc()
        print(error)

        result['status'] = False
        result['error'] = error
        return result

    count = 0
    extracted_data_list = []

    for link in links:
        if count == limit:
            break

        try:
            driver.get(link)

            home_page_source = driver.page_source
            home_page_soup: BeautifulSoup = BeautifulSoup(home_page_source, 'lxml')

            business_data = get_business_details(home_page_soup,driver)
            business_data["google_map_url"] = link

            extracted_data_list.append(business_data)
            if status: status.update(f"[bold yellow]Scrapping Data From The Google Map... [green]({count+1}/{len(links)}) done:{len(extracted_data_list)}")
        except Exception as error:
            traceback.print_exc()
            print(error)

            result['status'] = False
            result['error'] = error
            return result

        count += 1
        if progress:
            progress.update(task_bar, advance=1)

    generate_json(extracted_data_list)
    driver.close()

    if progress:
        progress.stop()
    if console:
        console.print(
            f"[green]Scraped [cyan bold]{len(extracted_data_list)}[reset] [green]{industry_name} Data Successfully!\n")
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
                        load_full_review_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div > span  > button")))
                        load_full_review_button.click()
                        home_page_soup = BeautifulSoup(driver.page_source,'lxml')
                    except:
                        print("Error 1")

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


def scrape_organization_number(console=None, status=None):
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
                    f"[green]✅ [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({org_found}/{len(url_list)})")
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
                        f"[green]✅ [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({org_found}/{len(url_list)})")
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
                    f"[red]❌ [bold]{business_name}[reset] [red]Organization Number Not Found! [yellow]({org_found}/{len(url_list)})")

        if status:
            status.update(
                f"[bold yellow]Scrapping Organization Number... [green]({index}\{len(url_list)}) done:{org_found}")
    connections.commit()
    cursor.close()
    connections.close()

    result['time_taken'] = time.time() - result['time_taken']
    result["network_usage"] = get_network_usage() - result["network_usage"]
    return result


def scrape_business_email(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    try:
        connections = get_database_connection()
        cursor = connections.cursor()
        cursor.execute(
            "SELECT lead_id,business_name,website_url from leads WHERE website_url != 'null' AND business_email = 'null'  ")
        web_url_list = cursor.fetchall()

        email_found = 0
        for index,item in enumerate(web_url_list):
            lead_id, business_name, url = item

            # response = requests.get(url)
            response = requests.get(f"https://{url}")
            soup = BeautifulSoup(response.text, 'lxml')
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            emails = re.findall(email_pattern, soup.text)
            if emails:
                email_found += 1
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
                        f"[red]❌ [bold]{business_name}[reset] [red]Email Not Found! [yellow]({email_found}/{len(web_url_list)})")
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


def scrape_allabolag_details(console=None, status=None):
    result = {"status": True, "error": None, "time_taken": time.time(), "network_usage": get_network_usage()}

    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT allabolag_id,organization_number FROM allabolag WHERE registered_name="null"')
    allabolag_data = cursor.fetchall()
    if len(allabolag_data) == 0:
        if console:
            console.print("\n[green]It Is Already Uptodate!\n", justify="center")
        result['time_taken'] = time.time() - result['time_taken']
        result["network_usage"] = get_network_usage() - result["network_usage"]
        return result

    allabolag_table = Table(title="")

    allabolag_table.add_column("Registered Name", justify="right", style="cyan", no_wrap=True)
    allabolag_table.add_column("Ceo Name", style="magenta")
    allabolag_table.add_column("Business", justify="right", style="green")
    allabolag_table.add_column("Revenue", justify="right", style="green")
    allabolag_table.add_column("Registration", justify="right", style="green")
    allabolag_table.add_column("Employees", justify="right", style="green")

    headcount_table = Table(title="")
    revenue_track_table = Table(title="")
    headcount_table.add_column("Registered Name", justify="right", style="cyan", no_wrap=True)
    revenue_track_table.add_column("Registered Name", justify="right", style="cyan", no_wrap=True)

    for year in range(2022, 2016, -1):
        headcount_table.add_column(f"Head Count - {year}", justify="right", style="cyan", )
        revenue_track_table.add_column(f"Revenue Track - {year}", justify="right", style="cyan", )
    if console:
        console.print("*note: table will be listed once everything is extracted!", justify="center")
    index = 0
    for allabolag_id, organization_number in allabolag_data:
        res = requests.get(f"https://www.allabolag.se/{organization_number}")
        soup = BeautifulSoup(res.text, 'lxml')
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

        res = requests.get(f"https://www.allabolag.se/{organization_number}/bokslut")
        soup = BeautifulSoup(res.text, 'lxml')
        number_of_employees = soup.select("#bokslut > div > div:nth-child(7) > table > tbody > tr:nth-child(1) > td ")[
            0].text.strip()
        # print(number_of_employees)
        revenue_list = [x.text.strip() + " 000" for x in
                        soup.select("#bokslut > div> div > table > tbody > tr")[24].select('td')[0:6] if 1 == 1]
        headcount_list = [int(x.text.strip()) for x in
                          soup.select("#bokslut > div> div > table > tbody > tr")[25].select('td')[0:6] if 1 == 1]
        revenue_list.insert(0, allabolag_id)
        headcount_list.insert(0, allabolag_id)

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
        total_allabolag_found = 1
        index += 1
        if console:
            console.print(
                f"[green]✅ [bold]{registered_name}[reset][green]'s  Allabolag Data Are Extracted Successfully!")
        if status:
            status.update(f"[bold yellow]Scrapping Allabolag Details... [green]({index+1}/{len(allabolag_data)}) done:{total_allabolag_found} | ")
            total_allabolag_found += 1

    if console:
        console.clear()
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeAllabolag",
                      justify="center")
        console.print(Markdown("---"))
        console.print(allabolag_table)
        console.print(revenue_track_table)
        console.print(headcount_table)
    connection.commit()
    cursor.close()
    connection.close()

    result['time_taken'] = time.time() - result['time_taken']
    result["network_usage"] = get_network_usage() - result["network_usage"]
    return result
