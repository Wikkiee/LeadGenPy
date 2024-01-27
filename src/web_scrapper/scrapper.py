import re

import traceback
import requests
from bs4 import BeautifulSoup
from Configs.selenium_config import driver
from selenium.webdriver.common.by import By
from Configs.database_config import get_database_connection
from Utils.store import generate_json


def get_organization_number():
    connections = get_database_connection()
    cursor = connections.cursor()
    cursor.execute("SELECT lead_id,website_url from leads WHERE website_url != 'null' ")
    url_list = cursor.fetchall()
    print(url_list)
    for url in url_list:
        lead_id, url = url[0], url[1]
        response = requests.get(f"https://{url}")
        soup = BeautifulSoup(response.text, 'lxml')

        # Pattern for XXXXXX-XXXX format
        def extract_org_number(page):
            pattern_1 = r'\b\d{6}-\d{4}\b'
            matches = re.findall(pattern_1, page.text)
            return matches

        org_number = extract_org_number(soup)
        if org_number:
            print(f'\n{url[0]} - Org.No : {org_number[0]}\n')
            print(org_number)
            cursor.execute(f"""
                    INSERT INTO 
                    allabolag(lead_id,organization_number	)
                    VALUES({lead_id},{org_number[0].replace('-', '')})

            """)
            connections.commit()
            print("Inserted - 1")
            continue

        links_list = []
        for i in soup.find_all("a", href=True):
            links_list.append(i['href'])
        ending_words = ['privacy', 'policy', 'terms', 'Integritetspolicy']
        pattern_links = re.compile(r'https?://\S*?(' + '|'.join(ending_words) + r')\S*', re.IGNORECASE)
        matches_links = [link for link in links_list if pattern_links.search(link)]
        print("Privacy policy links:", matches_links)

        for link in matches_links:
            response = requests.get(link)
            soup = BeautifulSoup(response.text, 'lxml')
            org_number = extract_org_number(soup)
            if org_number:
                print(f'\n{url} - Org.No : {org_number[0]}\n')
                print(org_number)

                cursor.execute(f"""
                    INSERT INTO 
                    allabolag(lead_id,organization_number	)
                    VALUES({lead_id},{org_number[0].replace('-', '')})

                    """)
                print("Inserted - 2")
                break

    connections.commit()
    cursor.close()
    connections.close()


def get_business_email():
    try:

        connections = get_database_connection()
        cursor = connections.cursor()
        cursor.execute("SELECT lead_id,website_url from leads WHERE website_url != 'null' ")
        web_url_list = cursor.fetchall()

        for item in web_url_list:
            lead_id, url = item
            print(url)
            # response = requests.get(url)
            response = requests.get(f"https://{url}")
            soup = BeautifulSoup(response.text, 'lxml')
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            emails = re.findall(email_pattern, soup.text)
            if emails:
                result = re.sub(r'\d', '', emails[0])
                print(result)
                cursor.execute("""
                    UPDATE leads
                    SET business_email = %s
                    WHERE lead_id = %s

                """, (result, lead_id))
                if cursor.rowcount:
                    print("updated")
                continue
            else:
                print(f'[LOG] - EMAIL NOT FOUND: {emails}')

        connections.commit()
        cursor.close()
        connections.close()

    except Exception as error:
        traceback.print_exc()
        print(error)
        return "null"


def get_allabolag_details():

    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT allabolag_id,organization_number FROM allabolag WHERE registered_name="null"')
    allabolag_data = cursor.fetchall()
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
        print(registered_name)
        print(ceo_name)
        print(type_of_business)
        print(revenue)
        print(year_of_registeration)
        res = requests.get(f"https://www.allabolag.se/{organization_number}/bokslut")
        soup = BeautifulSoup(res.text, 'lxml')
        number_of_employees = \
            soup.select("#bokslut > div > div:nth-child(7) > table > tbody > tr:nth-child(1) > td ")[0].text.strip()
        print(number_of_employees)
        revenue_list = [x.text.strip() + " 000" for x in
                        soup.select("#bokslut > div> div > table > tbody > tr")[24].select('td')[0:6] if 1 == 1]
        headcount_list = [int(x.text.strip()) for x in
                          soup.select("#bokslut > div> div > table > tbody > tr")[25].select('td')[0:6] if 1 == 1]
        revenue_list.insert(0, allabolag_id)
        headcount_list.insert(0, allabolag_id)
        print(revenue_list)
        print(headcount_list)
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

    connection.commit()
    cursor.close()
    connection.close()
    print("Completed")


def get_business_details(home_page_soup):
    try:

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
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') or home_page_soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img'):
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

        # Review page:
        count = 1
        for i in range(30, 60):
            if count > 3:
                break
            reviewer_name = home_page_soup.select(
                f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div > div > div:nth-child(2) > div > button > div")
            review_content = home_page_soup.select(
                f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div > span ")
            if len(reviewer_name) > 0:
                business_data[
                    f"top_review_{count}"] = f"Review by {reviewer_name[0].text} \n{review_content[0].text}"
                count = count + 1

        return business_data
    except Exception as error:
        print(error)
        traceback.print_exc()
        return {}


def get_data_from_google_map(industry_name, location):

    try:
        query = f'{industry_name} in {location}' if industry_name and location else f'{industry_name} {location}'
        driver.get(
            f'https://www.google.com/maps/search/{query}')
        scrollable_table = driver.find_element(
            By.CSS_SELECTOR,
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")
        # while True:
        #     scrollable_table.send_keys(Keys.END)  # MAX - 120 Items
        #     if driver.find_elements(By.CSS_SELECTOR,
        #                             "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t > div.m6QErb.tLjsW.eKbjU > div > p > span > span"):
        #         if driver.find_elements(
        #                 By.CSS_SELECTOR,
        #                 "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.RiRi5e.Hk4XGb.Yt0HSb > div > button"):
        #             driver.find_element(
        #                 By.CSS_SELECTOR,
        #                 "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.RiRi5e.Hk4XGb.Yt0HSb > div > button").click()
        #         break

        soup = BeautifulSoup(driver.page_source, 'lxml')
        res = soup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div:not(.TFQHme):not(.m6QErb) > div > a")
        links = [link.attrs['href'] for link in res]

        result = []
        count = 0

        for link in links:
            if count == 2:
                break
            driver.get(link)

            home_page_source = driver.page_source
            home_page_soup = BeautifulSoup(home_page_source, 'lxml')

            business_data = get_business_details(home_page_soup)
            business_data["google_map_url"] = link

            result.append(business_data)

            count += 1

        generate_json(result)
        driver.close()
        return result[0]
    except Exception as error:
        traceback.print_exc()
        print(error)
