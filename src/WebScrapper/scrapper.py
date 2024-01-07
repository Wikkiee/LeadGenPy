import re
import time
import traceback
import requests
from bs4 import BeautifulSoup
from Configs.selenium_config import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from WebScrapper.store import Store


class Scrappers:
    def scrape(self,industry_name, location):
        try:
            print("\n[LOG] - LOADING ITEMS\n")
            log_file = open('../assets/logs.txt',"a")
            scrapeDetail = ScrapeDetails()
            store = Store()
            query = f'{industry_name} in {location}' if industry_name and location else f'{industry_name} {location}'
            driver.get(
                f'https://www.google.com/maps/search/{query}')
            scrollableTable = driver.find_element(
                By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd")
            # while True:
            #     scrollableTable.send_keys(Keys.END)  # MAX - 120 Items
            #     if driver.find_elements(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd.QjC7t > div.m6QErb.tLjsW.eKbjU > div > p > span > span"):
            #         if driver.find_elements(
            #                 By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.RiRi5e.Hk4XGb.Yt0HSb > div > button"):
            #             driver.find_element(
            #                 By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div:nth-child(2) > div > div.e07Vkf.kA9KIf > div > div > div.RiRi5e.Hk4XGb.Yt0HSb > div > button").click()
            #         break
            print("\n[LOG] - ITEMS LOADED\n")
            log_file.write("\n[LOG] - ITEMS LOADED\n")
            soup = BeautifulSoup(driver.page_source, 'lxml')
            res = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div:not(.TFQHme):not(.m6QErb) > div > a")
            links = [link.attrs['href'] for link in res]
            print(f'{len(links)} ITEMS FOUND')
            log_file.write(f'{len(links)} ITEMS FOUND')
            result = []
            count = 0

            print("\n[LOG] - EXTRACTING DATA \n")
            log_file.write("\n[LOG] - EXTRACTING DATA \n")
            for link in links:
                if count == 2:
                    break
                driver.get(link)
                print(f"\n[LOG] -  VISITNG : {link[0:25]}... \n")
                log_file.write(f"\n[LOG] -  VISITNG : {link[0:25]}... \n")
                content = driver.page_source
                soup = BeautifulSoup(content, 'lxml')
                print("\n[LOG] - SOURCE PAGE EXTRACTED\n")
                log_file.write("\n[LOG] - SOURCE PAGE EXTRACTED\n")
                business_data = scrapeDetail.scrape_data(soup,log_file)
                business_data["google_map_link"] = link
                business_data["email"] = scrapeDetail.scrape_email(business_data["Website"],log_file) if business_data["Website"] != 'null' else 'null'
                business_data["status"] = "null"
                print("\n[LOG] - DETAILS EXTRACTED\n")
                log_file.write("\n[LOG] - DETAILS EXTRACTED\n")
                result.append(business_data)
                # store.insertOne([
                #     list(business_data.values())
                # ]) - uncomment this to add data to the google sheet on each iteration
                count += 1
            print("\n[LOG] - DATASET LOADED\n")
            log_file.write("\n[LOG] - DATASET LOADED\n")
            store.generate_json(result)
            print("\n[LOG] - EXTRACTION COMPLETED\n")
            log_file.write("\n[LOG] - EXTRACTION COMPLETED\n")
            log_file.close()
        except:
            traceback.print_exc()
            log_file.close()
            time.sleep(3)



class ScrapeDetails:
    def scrape_data(self,soup,log_file):
            try:
                print("\n[LOG] - EXTRACTING DETAILS\n")
                log_file.write("\n[LOG] - EXTRACTING DETAILS\n")
                business_data = {
                        "BusinessName": "null",
                        "Address": "null",
                        "PhoneNumber": "null",
                        "Website": "null",
                        "Category": "null",
                        "Rating": "null",
                        "ReviewCount": "null",
                }
                base_selector = 9
                for i in range(7,10):
                    if len(soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({i}) > div'))>1:
                        base_selector = i
                        break
                length = soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div') 
                name_selector = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1")
                category_selector = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div:nth-child(2) > span > span > button")
                ratings_selector = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(1) > span:nth-child(1)")
                reviews_selector = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div.LBgpqf > div > div.fontBodyMedium.dmRWX > div.F7nice > span:nth-child(2) > span > span")
                business_data["BusinessName"] = name_selector[0].text if name_selector else "null"
                print(f"\n[LOG] - Name: {business_data['BusinessName']}\n")
                log_file.write(f"\n[LOG] - Name: {business_data['BusinessName']}\n")
                for i in range(3,len(length)):
                    if soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') or soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img'):
                        src_link = soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img')[0].attrs['src'] if soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') else soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img')[0].attrs['src']
                        if(src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png"):
                            print("[LOG] - ADDRESS Found")
                            log_file.write("[LOG] - ADDRESS Found")
                            business_data["Address"] = soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[0].text if soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[0].text
                        elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png":
                            print("[LOG] - WEBSITE FOUND")
                            log_file.write("[LOG] - WEBSITE FOUND")
                            business_data["Website"] = soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[0].text if soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[0].text
                        elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png":
                            print("[LOG] - PHONE NUMBER FOUND")
                            log_file.write("[LOG] - PHONE NUMBER FOUND")
                            business_data["PhoneNumber"] = soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[0].text if soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[0].text
                business_data["Category"] = category_selector[0].text if category_selector else "null"
                business_data["Rating"] = ratings_selector[0].text if ratings_selector else "null"
                business_data["ReviewCount"] = reviews_selector[0].text[1:-1] if reviews_selector else "null"
                return business_data
            except Exception as error :
                print(error)

    
    def scrape_email(self,url,log_file):
        try:
            print(f"\n[LOG] - EXTRACTING EMAIL ADDRESS FROM https://{url}\n")
            log_file.write(f"\n[LOG] - EXTRACTING EMAIL ADDRESS FROM https://{url}\n")
            response = requests.get(f"https://{url}")
            soup = BeautifulSoup(response.text, 'lxml')
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            emails = re.findall(email_pattern, soup.text)
            
            if emails:
                result = re.sub(r'\d', '', emails[0])
                print(f"\n[LOG] - EMAIL FOUND : {result}")
                log_file.write(f"\n[LOG] - EMAIL FOUND : {result}")
                return result
            else:
                print(f'[LOG] - EMAIL NOT FOUND: {emails}')
                log_file.write(f'[LOG] - EMAIL NOT FOUND: {emails}')
            return 'null'
            
        except Exception as error:
            print(error)
            return "null"
