from __future__ import print_function
import os.path
import googleapiclient
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = './texts/keys.json'
creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#Edit this to the spreadsheet ID
SPREADSHEET_ID = '1-y1D045V935gN-QgU1Num1nTugItfcmOkW2Kf5RAE6s'
#Edit this to the name of the spreadsheet tab that is active
CURRENT_RAID = 'Night at the Gallery'

#Gets the value(s) from SPREADSHEET_ID and CURRENT_RAID
def get_value(sheet: googleapiclient.discovery.Resource, range: str):
    values = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                    range=CURRENT_RAID+'!'+range).execute()
    return values.get('values')

def get_missing_hits():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    attendance_array = []
    num_members = int(get_value(sheet, 'X7')[0][0])-1
    members = get_value(sheet, 'A2:A'+str(int(get_value(sheet, 'X7')[0][0])-1))
    xl_date = datetime.strptime(get_value(sheet, 'B1')[0][0]+'/'+str(datetime.today().year), '%m/%d/%Y')
    now = datetime.now()
    days_passed = min((now-xl_date).days, 13)
    print('days passed: {}'.format(days_passed))
    if days_passed < 0:
        return []
    col_today = chr(ord('B') + days_passed)
    current_status = get_value(sheet, col_today+'2:'+col_today+str(num_members))
    if not current_status:
        current_status = [[]]
    current_status += [[]] * max(num_members - len(current_status) - 1, 0)
    for i in range(len(current_status)):
        print(current_status[i])
        if not current_status[i] or current_status[i][0] != '>>>':
            attendance_array.append(members[i][0])
    return(attendance_array)

print('attendance.py ready')