from selenium import webdriver
from beaupy import select,prompt
from rich.console import Console
import time
from beaupy.spinners import *




def __initialize():
    console = Console()
    spinner = Spinner(DOTS, "Initializing Selenium Webdriver ...")
    spinner.start()
    chrome_options = webdriver.ChromeOptions()
    
    #mode = int(input("<== SELENIUM: ==>\n1 - Launch headless Mode\n2 - Development Mode (Browswer Mode)\nEnter the value : "))
    mode = select(["Launch Headless Mode", "Launch Development Mode (Browser Mode)"])
    if mode  == "Launch Headless Mode":
        chrome_options.add_argument("--headless=new")
    console.print(f"[blue]{mode}[/blue]")
    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2,
                                                        'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2,
                                                        'durable_storage': 2}}
    #chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")

    spinner.stop()
    return webdriver.Chrome(
    '../assets/chromedriver.exe', chrome_options=chrome_options)
driver = __initialize()