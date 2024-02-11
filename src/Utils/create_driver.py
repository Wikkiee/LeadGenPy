from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os
import Configs.config as config


def createDriver() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values': config.SELENIUM_CONFIG["profile.default_content_setting_values"]}
    # PROXY = "45.61.187.67:4000"
    # chrome_options.add_argument(f"--proxy-server={PROXY}")
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


    for argument in config.SELENIUM_CONFIG["arguments"]:
        chrome_options.add_argument(argument)

    driver = webdriver.Chrome(options=chrome_options)
    return driver
