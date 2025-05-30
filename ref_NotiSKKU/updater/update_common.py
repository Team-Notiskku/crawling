from googleapiclient.discovery import build
from google.oauth2 import service_account
from common_modules import get_general, update_google_sheets, update_last_modified_time, get_latest

##SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json"
SERVICE_ACCOUNT_FILE = "credentials.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAME = "시트1"
BASE_URL = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"
XPATH = {
    "category": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/span[1]',
    "title": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a',
    "id": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[1]',
    "uploader": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[2]',
    "date": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[3]',
    "views": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dd/ul/li[4]/span',
    "link": '//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{}]/dl/dt/a'
}

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

latest_id, next_row = get_latest(SPREADSHEET_ID, SHEET_NAME)
latest_id = int(latest_id)
data = get_general(BASE_URL, XPATH, latest_id)
if data:
    update_google_sheets(SPREADSHEET_ID, SHEET_NAME, data, next_row)
update_last_modified_time(SPREADSHEET_ID, SHEET_NAME)

