from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

service.spreadsheets().values().clear(
    spreadsheetId=SPREADSHEET_ID,
    range= "시트1" 
).execute()

print("공통 공지 초기화 완료")