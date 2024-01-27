import os, json
import openai

from dotenv import load_dotenv
load_dotenv()

SELENIUM_CONFIG = CHATGPT_CONFIG = DATABASE_CONFIG = None

def initialize():
    global SELENIUM_CONFIG, DATABASE_CONFIG
    SELENIUM_CONFIG = json.load( open(os.path.join(os.getcwd(),'Configs\\seleniumConfig.json')) )
    DATABASE_CONFIG = json.load( open(os.path.join(os.getcwd(),'Configs\\databaseConfig.json')) )
    openai.api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    initialize()
    print(SELENIUM_CONFIG,CHATGPT_CONFIG,DATABASE_CONFIG, sep = '\n')
else:initialize()