from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import os
import Configs.config as config

Driver = None
def __initialize():
    chrome_options = webdriver.ChromeOptions()

    prefs = {'profile.default_content_setting_values': config.SELENIUM_CONFIG["profile.default_content_setting_values"]}
    chrome_options.add_experimental_option('prefs', prefs)

    for argument in config.SELENIUM_CONFIG["arguments"]:
        chrome_options.add_argument(argument)

    return webdriver.Chrome( service=Service(os.path.join(os.getcwd(),config.SELENIUM_CONFIG["chromeDriverPath"])), chrome_options=chrome_options)

if __name__ == "__main__":
    Driver = __initialize()
    print("driver:",Driver)
else: Driver = __initialize()
