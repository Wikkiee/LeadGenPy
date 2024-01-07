import os
import openai
from dotenv import load_dotenv
load_dotenv()
import time
from beaupy.spinners import *

spinner = Spinner(DOTS, "Authenticating with OpenAI ...")
spinner.start()
time.sleep(2)
openai.api_key = os.getenv("OPENAI_API_KEY")
spinner.stop()