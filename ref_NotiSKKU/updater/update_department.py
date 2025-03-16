from googleapiclient.discovery import build
from google.oauth2 import service_account
from configs.config_department import DEPT_URLS, DEPT_XPATHS, pin_dept, other_dept, has_views_dept
from common_modules import get_general, update_google_sheets, update_last_modified_time, get_pinned, get_exceptions, get_latest, get_latest_date

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1YX53hQ1oHjAhl8wvsa6nIq6P5Eh0SMyV8SaN8hsPyTg"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAMES = list(DEPT_URLS.keys())

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

for name in SHEET_NAMES:
    print(f"{name} 크롤링을 시작합니다.")
    latest_id, next_row = get_latest(SPREADSHEET_ID, name)
    latest_id = int(latest_id)
    if name in pin_dept:
        data = get_pinned(DEPT_URLS[name], DEPT_XPATHS[name], latest_id, 0)
    elif name in other_dept:
        if latest_id == 0:
            latest_date = get_latest_date(SPREADSHEET_ID, name)
            data = get_exceptions(name, DEPT_URLS[name], DEPT_XPATHS[name], latest_date)
        else :
            data = 0
        data = get_exceptions(name, DEPT_URLS[name], DEPT_XPATHS[name], latest_id)
    else:
        data = get_general(DEPT_URLS[name], DEPT_XPATHS[name], latest_id)
    
    if data:
        update_google_sheets(SPREADSHEET_ID, name, data, next_row)
    
    update_last_modified_time(SPREADSHEET_ID, name)
