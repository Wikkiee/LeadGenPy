import re

import traceback
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from Configs.database import get_database_connection
from Utils.store import generate_json
from Utils.create_driver import createDriver

from rich.table import Table
from rich.markdown import Markdown

def getDataFromGoogleMap(industryName="restaurants", location="sweden", limit=2, taskBar=None, progress=None):
    query = f'{industryName} in {location}' if industryName and location else f'{industryName} {location}'
    try:
        driver = createDriver()

        driver.get(f'https://www.google.com/maps/search/{query}')
        scrollableTable = driver.find_element(By.CSS_SELECTOR,"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")

        while True:
            scrollableTable.send_keys(Keys.END)  # MAX - 120 Items
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
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div:not(.TFQHme):not(.m6QErb) > div > a"
        )

        links = [link.attrs['href'] for link in res]
    except Exception as error:
        traceback.print_exc()
        print(error)
        return None

    count = 0
    result = []

    for link in links:
        if count == limit:
            break

        try:
            driver.get(link)

            homePageSource = driver.page_source
            homePageSoup: BeautifulSoup = BeautifulSoup(homePageSource, 'lxml')

            businessData = getBusinessDetails(homePageSoup)
            businessData["google_map_url"] = link

            result.append(businessData)
        except Exception as error:
            traceback.print_exc()
            print(error)
            return None

        count += 1
        if (progress):
            progress.update(taskBar, advance=1)

    generate_json(result)
    driver.close()
    return result


def getBusinessDetails(homePageSoup: BeautifulSoup):
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
            if len(homePageSoup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({i}) > div')) > 1:
                base_selector = i
                break

        length = homePageSoup.select(
            f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div')
        name_selector = homePageSoup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1")
        category_selector = homePageSoup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div:nth-child(2) > span > span > button")
        ratings_selector = homePageSoup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(1) > span:nth-child(1)")
        reviews_selector = homePageSoup.select(
            "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(2) > span > span")
        business_data["business_name"] = name_selector[0].text if name_selector else "null"

        for i in range(3, len(length)):
            if homePageSoup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') or homePageSoup.select(
                f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img'):
                src_link = homePageSoup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img')[
                    0].attrs['src'] if homePageSoup.select(
                    f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') else \
                    homePageSoup.select(
                        f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img')[
                        0].attrs['src']
                if src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png":

                    business_data["business_address"] = homePageSoup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[
                        0].text if homePageSoup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else \
                        homePageSoup.select(
                            f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[
                            0].text
                elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png":

                    business_data["website_url"] = homePageSoup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[
                        0].text if homePageSoup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else \
                        homePageSoup.select(
                            f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[
                            0].text
                elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png":

                    business_data["mobile_number"] = homePageSoup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[
                        0].text if homePageSoup.select(
                        f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else \
                        homePageSoup.select(
                            f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[
                            0].text

        business_data["business_category"] = category_selector[0].text if category_selector else "null"
        business_data["ratings"] = ratings_selector[0].text if ratings_selector else "null"
        business_data["review_counts"] = reviews_selector[0].text[1:-1] if reviews_selector else "null"

        count = 1
        for i in range(30, 60):
            if count > 3:
                break
            reviewer_name = homePageSoup.select(
                f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div > div > div:nth-child(2) > div > button > div")
            review_content = homePageSoup.select(
                f"#QA0Szd > div > div > div > div > div > div > div > div > div:nth-child({i}) > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div > span ")

            if len(reviewer_name) > 0:
                business_data[f"top_review_{count}"] = f"Review by {reviewer_name[0].text} \n{review_content[0].text}"
                count = count + 1

        return business_data
    except Exception as error:
        print(error)
        traceback.print_exc()
        return {}


def get_organization_number(console=None):
    connections = get_database_connection()
    cursor = connections.cursor()
    cursor.execute("SELECT lead_id,website_url,business_name from leads WHERE website_url != 'null' ")
    url_list = cursor.fetchall()

    orgFound = 0
    for url in url_list:
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
            orgFound += 1
            console.print(
                f"[green]✅ [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({orgFound}/{len(url_list)})")

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
                orgFound += 1
                console.print(
                    f"[green]✅ [bold]{business_name}[reset] [green]Organization Number Found [bold]{org_number[0]}[reset] [yellow]({orgFound}/{len(url_list)})")

                cursor.execute(f"""
                    INSERT INTO 
                    allabolag(lead_id,organization_number	)
                    VALUES({lead_id},{org_number[0].replace('-', '')})
                    """)
                break
        else:
            console.print(
                f"[red]❌ [bold]{business_name}[reset] [red]Organization Number Not Found! [yellow]({orgFound}/{len(url_list)})")

    connections.commit()
    cursor.close()
    connections.close()


def get_business_email(console=None):
    try:

        connections = get_database_connection()
        cursor = connections.cursor()
        cursor.execute(
            "SELECT lead_id,business_name,website_url from leads WHERE website_url != 'null' AND business_email = 'null'  ")
        web_url_list = cursor.fetchall()

        emailFound = 0
        for item in web_url_list:
            lead_id, business_name, url = item

            # response = requests.get(url)
            response = requests.get(f"https://{url}")
            soup = BeautifulSoup(response.text, 'lxml')
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            emails = re.findall(email_pattern, soup.text)
            if emails:
                emailFound += 1
                result = re.sub(r'\d', '', emails[0])
                console.print(
                    f"[green]✅ [bold]{business_name}[reset] [green]Email Scraped successfully [bold]{result}[reset] [yellow]({emailFound}/{len(web_url_list)})")
                cursor.execute("""
                    UPDATE leads
                    SET business_email = %s
                    WHERE lead_id = %s
                """, (result, lead_id))
                continue
            else:
                console.print(
                    f"[red]❌ [bold]{business_name}[reset] [red]Email Not Found! [yellow]({emailFound}/{len(web_url_list)})")

        connections.commit()
        cursor.close()
        connections.close()

    except Exception as error:
        traceback.print_exc()
        print(error)
        return "null"


def get_allabolag_details(console=None):
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT allabolag_id,organization_number FROM allabolag WHERE registered_name="null"')
    allabolag_data = cursor.fetchall()
    if len(allabolag_data) == 0:
        console.print("\n[green]It Is Already Uptodate!\n", justify="center")
        return

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

    for year in range(2022,2016,-1):
        headcount_table.add_column(f"Head Count - {year}", justify="right", style="cyan", )
        revenue_track_table.add_column(f"Revenue Track - {year}", justify="right", style="cyan", )


    console.print("*note: table will be listed once everything is extracted!",justify="center")
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
        revenue_track_table.add_row(registered_name,str(revenue_list[1]), str(revenue_list[2]), str(revenue_list[3]), str(revenue_list[4]),
                                str(revenue_list[5]), str(revenue_list[6]))
        headcount_table.add_row(registered_name,str(headcount_list[1]),str(headcount_list[2]),str(headcount_list[3]),str(headcount_list[4]),str(headcount_list[5]),str(headcount_list[6]))


        # print(revenue_list)
        # print(headcount_list)
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
        console.print(f"[green]✅ [bold]{registered_name}[reset][green]'s  Allabolag Data Are Extracted Successfully!")

    console.clear()
    console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow]ScrapeAllabolag", justify="center")
    console.print(Markdown("---"))
    console.print(allabolag_table)
    console.print(revenue_track_table)
    console.print(headcount_table)
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    print(getDataFromGoogleMap("restaurants", "india", 2))
