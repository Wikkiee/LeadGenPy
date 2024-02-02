import csv
import os
import smtplib
import ssl
import time
from email.message import EmailMessage

from memory_profiler import memory_usage
from Configs.database import get_database_connection
from Utils.embed_content_generator import generate_embedded_email_content
from Utils.create_driver import createDriver
def f():
    a = 1
    return a

def test():
    driver = createDriver()
    driver.get("https://www.whatismyip.com/my-ip-information/")
    os.system("pause")

if __name__ == "__main__":
   test()