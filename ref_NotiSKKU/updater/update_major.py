from googleapiclient.discovery import build
from google.oauth2 import service_account
from configs.config_major import MAJOR_URLS, MAJOR_XPATHS, pin_major, other_major
from common_modules import get_general, update_google_sheets, update_last_modified_time, get_pinned, get_exceptions, get_latest, get_latest_date

SERVICE_ACCOUNT_FILE = "credentials.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XOv61iZQiPwc2CeqU4lnZsnmpUIhp4Tnjcsk84mHihU"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAMES = list(MAJOR_URLS.keys())

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

for name in SHEET_NAMES:
    latest_id, next_row = get_latest(SPREADSHEET_ID, name)
    latest_id = int(latest_id)
    if name == "건축학과(건축학계열)":
        data = get_pinned(MAJOR_URLS[name], MAJOR_XPATHS[name], latest_id, 1)
    elif name in pin_major:
        data = get_pinned(MAJOR_URLS[name], MAJOR_XPATHS[name], latest_id, 0)
    elif name in other_major:
        if latest_id == 0:
            latest_date = get_latest_date(SPREADSHEET_ID, name)
            data = get_exceptions(name, MAJOR_URLS[name], MAJOR_XPATHS[name], latest_date)
        else :
            data = 0
    else:
        data = get_general(MAJOR_URLS[name], MAJOR_XPATHS[name], latest_id)

    if data:
        update_google_sheets(SPREADSHEET_ID, name, data, next_row)
    
    update_last_modified_time(SPREADSHEET_ID, name)
