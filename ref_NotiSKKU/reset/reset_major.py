from googleapiclient.discovery import build
from google.oauth2 import service_account
from configs.config_major import MAJOR_URLS

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XOv61iZQiPwc2CeqU4lnZsnmpUIhp4Tnjcsk84mHihU"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAMES = list(MAJOR_URLS.keys())

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

for name in SHEET_NAMES:
    range_name = f"{name}"  

    service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name  
    ).execute()

    print(f"{name} 시트 초기화 완료")