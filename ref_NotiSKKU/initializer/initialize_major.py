from googleapiclient.discovery import build
from google.oauth2 import service_account
from configs.config_major import MAJOR_URLS, MAJOR_XPATHS, pin_major, other_major
from common_modules import get_general, update_google_sheets, update_last_modified_time, get_pinned, get_exceptions

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XOv61iZQiPwc2CeqU4lnZsnmpUIhp4Tnjcsk84mHihU"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAMES = list(MAJOR_URLS.keys())

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

for name in SHEET_NAMES:
    print(f"{name} 크롤링을 시작합니다.")
 
    if name == "건축학과(건축학계열)":
        data = get_pinned(MAJOR_URLS[name], MAJOR_XPATHS[name], -1, 1)
    elif name in pin_major:
        data = get_pinned(MAJOR_URLS[name], MAJOR_XPATHS[name], -1, 0)
    elif name in other_major:
        data = get_exceptions(name, MAJOR_URLS[name], MAJOR_XPATHS[name], -1)
    else:
        data = get_general(MAJOR_URLS[name], MAJOR_XPATHS[name], -1)
    
    if data:
        update_google_sheets(SPREADSHEET_ID, name, data, 2)
    
    update_last_modified_time(SPREADSHEET_ID, name)
