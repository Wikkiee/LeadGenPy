import json
import os

import openai
from dotenv import load_dotenv

load_dotenv()

SELENIUM_CONFIG = CHATGPT_CONFIG = DATABASE_CONFIG = APPLICATION_PROPERTIES = None


def initialize():
    global SELENIUM_CONFIG, DATABASE_CONFIG,APPLICATION_PROPERTIES
    SELENIUM_CONFIG = json.load(open(os.path.join(os.getcwd(), '..\\src\\configs\\selenium_config.json')))
    DATABASE_CONFIG = json.load(open(os.path.join(os.getcwd(), '..\\src\\configs\\database_config.json')))
    APPLICATION_PROPERTIES = json.load(open(os.path.join(os.getcwd(), '..\\src\\configs\\application_properties.json')))
    openai.api_key = os.getenv("OPENAI_API_KEY")

def update_configs(console=None,confirm=None,select=None,Markdown=None):
    if console:
        console.print("[bold green underline]LeadGenPy[reset][cyan bold]/[reset][yellow] Settings",
                      justify="center")
        console.print(Markdown("---"))
        try:
            while True:
                new_changes = False
                option = select(["Google Map Scraper","Database","OpenAI API Key","Back"])
                if option == "Back":
                    return
                if option == "Google Map Scraper":
                    while True:
                        options = [f"Scrape Top Review: [{'Enabled' if APPLICATION_PROPERTIES['google_map_data_scraper']['scrape_top_review'] else 'Disabled'}]","Back"]
                        item_index  = select(options,return_index = True)
                        print(item_index )
                        if item_index == 1:
                            break
                        if item_index == 0:
                            if confirm(options[item_index ],yes_text="Enable",no_text="Disable"):
                                APPLICATION_PROPERTIES['google_map_data_scraper']['scrape_top_review'] = True
                                new_changes = True
                            else:
                                APPLICATION_PROPERTIES['google_map_data_scraper']['scrape_top_review'] = False
                                new_changes = True
                        if new_changes:
                            with open('./configs/application_properties.json','w') as json_file:
                                json.dump(APPLICATION_PROPERTIES,json_file)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    initialize()
    print(SELENIUM_CONFIG, CHATGPT_CONFIG, DATABASE_CONFIG,APPLICATION_PROPERTIES, sep='\n')
else:
    initialize()
#
# {
#   "google_map_data_scraper": {
#     "scrape_top_review": true
#   }
# }