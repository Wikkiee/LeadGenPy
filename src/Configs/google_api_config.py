import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build as __build
from googleapiclient.errors import HttpError
import time
from beaupy.spinners import *





def __initialize():
    spinner = Spinner(DOTS, "Authenticating with Google API ...")
    spinner.start()
    
    time.sleep(1)
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/gmail.modify"]
    credentials = None
    if os.path.exists("token.json"):
        credentials = Credentials.from_authorized_user_file("token.json",SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("../assets/credentials.json",SCOPES)
            credentials = flow.run_local_server(port=5000,redirect_uri_trailing_slash=False)
        with open("token.json","w") as token:
            token.write(credentials.to_json())
    try:
        sheet = __build('sheets', 'v4', credentials=credentials)
        gmail = __build('gmail','v1',credentials=credentials)
        sheet = sheet.spreadsheets()
        spinner.stop()
        return {"sheet":sheet,"gmail":gmail}
    except HttpError as error:
        spinner.stop()
        print(error)
service = __initialize()
