import re
import time
import datetime
import traceback
import requests
from bs4 import BeautifulSoup
from beaupy.spinners import *
from Configs.selenium_config import driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from WebScrapper.store import Store


class Scrappers:
    def scrape(self,industry_name, location):
        time_stamp = datetime.datetime.now().strftime("%H:%M:%S")
        try:
            log_file = open('../assets/logs.txt',"a")
            log_file.write(f"[{time_stamp}] - LOADING ITEMS\n")
            spinner = Spinner(ARC,f"Searching {industry_name} in {location} on Google Map Search ...")
            spinner.start()
            scrapeDetail = ScrapeDetails()
            store = Store()
            query = f'{industry_name} in {location}' if industry_name and location else f'{industry_name} {location}'
            driver.get(
                f'https://www.google.com/maps/search/{query}')
            spinner.stop()
            spinner = Spinner(ARC,"Loading items in the sidebar ...")
            spinner.start()
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

            log_file.write(f"[{time_stamp}] - ITEMS LOADED\n")
            soup = BeautifulSoup(driver.page_source, 'lxml')
            res = soup.select("#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div:not(.TFQHme):not(.m6QErb) > div > a")
            links = [link.attrs['href'] for link in res]
            spinner.stop()
            spinner = Spinner(ARC,f"{len(links)} Items Found ...")
            spinner.start()
            log_file.write(f'[{time_stamp}] - {len(links)} ITEMS FOUND\n')
            result = []
            count = 0
            time.sleep(1)
            spinner.stop()
            spinner = Spinner(ARC,"Extracting data ...")
            spinner.start()
            log_file.write(f"[{time_stamp}] - EXTRACTING DATA\n")
            time.sleep(1)
            spinner.stop()
            for link in links:
                if count == 3:
                    break
                driver.get(link)
                spinner = Spinner(ARC,f"Visiting the item's : {link[0:25]} ...")
                spinner.start()

                log_file.write(f"[{time_stamp}] -  VISITNG : {link[0:25]}... \n")
                content = driver.page_source
                soup = BeautifulSoup(content, 'lxml')
                time.sleep(1)
                spinner.stop()

                spinner = Spinner(ARC,f"Page's Source Extracted ...")
                spinner.start()
                
                log_file.write(f"[{time_stamp}] - SOURCE PAGE EXTRACTED\n")
                time.sleep(1)
                spinner.stop()
                business_data = scrapeDetail.scrape_data(soup,log_file)
                business_data["google_map_link"] = link
                business_data["email"] = scrapeDetail.scrape_email(business_data["Website"],log_file) if business_data["Website"] != 'null' else 'null'
                business_data["status"] = "null"
                spinner = Spinner(ARC,f"Details Extracted ...")
                
                spinner.start()

                log_file.write(f"[{time_stamp}] - DETAILS EXTRACTED\n")
                result.append(business_data)
                # store.insertOne([
                #     list(business_data.values())
                # ]) - uncomment this to add data to the google sheet on each iteration
                time.sleep(1)
                spinner.stop()
                count += 1
            spinner = Spinner(ARC,f"Dataset Loaded ...")
            spinner.start()
            log_file.write(f"[{time_stamp}] - DATASET LOADED\n")
            store.generate_json(result)
            time.sleep(1)
            spinner.stop()
            spinner = Spinner(ARC,f"Extraction Completed ...")
            spinner.start()
            log_file.write(f"[{time_stamp}] - EXTRACTION COMPLETED\n")
            log_file.close()
            time.sleep(1)
            spinner.stop()
        except:
            traceback.print_exc()
            spinner.stop()
            log_file.close()
            time.sleep(3)



class ScrapeDetails:
    time_stamp = datetime.datetime.now().strftime("%H:%M:%S")
    def scrape_data(self,soup,log_file):
            try:


                spinner = Spinner(ARC,f"Extracting details ...")
                spinner.start()
                log_file.write(f"[{self.time_stamp}] - EXTRACTING DETAILS\n")
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
                time.sleep(1)
                spinner.stop()
                spinner = Spinner(ARC,f"Business Name: {business_data['BusinessName']} ...")
                spinner.start()

                log_file.write(f"[{self.time_stamp}] - Name: {business_data['BusinessName']}\n")
                time.sleep(1)
                spinner.stop()
                for i in range(3,len(length)):
                    if soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') or soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img'):
                        src_link = soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img')[0].attrs['src'] if soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div.cXHGnc > div > img') else soup.select(f'#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div.cXHGnc > div > img')[0].attrs['src']
                        if(src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/place_gm_blue_24dp.png"):
                            spinner = Spinner(ARC,f"Address found ...")
                            spinner.start()
                            log_file.write(f"[{self.time_stamp}] - ADDRESS Found\n")
                            business_data["Address"] = soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[0].text if soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[0].text
                            time.sleep(1)
                            spinner.stop()
                        elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/public_gm_blue_24dp.png":
                            spinner = Spinner(ARC,f"Address found ...")
                            spinner.start()
                            log_file.write(f"[{self.time_stamp}] - WEBSITE FOUND\n")
                            business_data["Website"] = soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[0].text if soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[0].text
                            time.sleep(1)
                            spinner.stop()
                        elif src_link == "//www.gstatic.com/images/icons/material/system_gm/2x/phone_gm_blue_24dp.png":
                           
                            spinner = Spinner(ARC,f"Phone number found ...")
                            spinner.start()
                            log_file.write(f"[{self.time_stamp}] - PHONE NUMBER FOUND\n")
                            business_data["PhoneNumber"] = soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2) > div")[0].text if soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > button > div > div:nth-child(2)") else soup.select(f"#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child({base_selector}) > div:nth-child({i}) > a > div > div:nth-child(2) > div")[0].text
                            time.sleep(1)
                            spinner.stop()
                business_data["Category"] = category_selector[0].text if category_selector else "null"
                business_data["Rating"] = ratings_selector[0].text if ratings_selector else "null"
                business_data["ReviewCount"] = reviews_selector[0].text[1:-1] if reviews_selector else "null"
                return business_data
            except Exception as error :
                spinner.stop()
                
                print(error)
                traceback.print_exc()

    
    def scrape_email(self,url,log_file):
        try:
            spinner = Spinner(ARC,f"Extracting Email Address from https://{url} ...")
            spinner.start()
            log_file.write(f"\n[{self.time_stamp}] - EXTRACTING EMAIL ADDRESS FROM https://{url}\n")
            response = requests.get(f"https://{url}")
            soup = BeautifulSoup(response.text, 'lxml')
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
            emails = re.findall(email_pattern, soup.text)
            time.sleep(1)
            spinner.stop()
            if emails:
                result = re.sub(r'\d', '', emails[0])
                time.sleep(1)
                spinner.stop()
                spinner = Spinner(ARC,f" Email Address Found : {result} ...")
                spinner.start()
                log_file.write(f"[{self.time_stamp}] - EMAIL FOUND : {result}\n")
                time.sleep(1)
                spinner.stop()
                return result
            else:
                time.sleep(1)
                spinner.stop()
                spinner = Spinner(ARC,f" Email Address Not Found ...")
                spinner.start()
                print(f'[LOG] - EMAIL NOT FOUND: {emails}')
                log_file.write(f'[{self.time_stamp}] - EMAIL NOT FOUND: {emails}\n')
                time.sleep(1)
                spinner.stop()
            return 'null'
            
        except Exception as error:
            spinner.stop()
            traceback.print_exc()
            print(error)
            return "null"
