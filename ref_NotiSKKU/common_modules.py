from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

def get_latest(SPREADSHEET_ID, SHEET_NAME):
    range_name = f"{SHEET_NAME}!A:A"  
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=range_name
    ).execute()

    values = result.get("values", [])

    if(len(values) != 0):
        latest_id = values[-1]
        return latest_id[0], len(values) + 1 
    else:
        return 0, 1

def update_google_sheets(SPREADSHEET_ID, SHEET_NAME, data, next_row):
    if not data:
        print(f"{SHEET_NAME}은 공지가 없습니다.")
        return
    
    range_name = f"{SHEET_NAME}!A{next_row}" 
    body = {"values": data}

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS", 
        body=body
    ).execute()
    print(f"Google Sheets에 {len(data)}개의 새로운 공지를 추가했습니다. (시작 행: {next_row})")

def update_last_modified_time(SPREADSHEET_ID, SHEET_NAME):
    last_modified_time = datetime.now().strftime("최종 편집 일시: %Y-%m-%d %H시 %M분 %S초")
    range_name = f"{SHEET_NAME}!A1"  

    body = {"values": [[last_modified_time]]}

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"{SHEET_NAME} 최종 편집 시각 업데이트 완료")

def get_general(base_url, xpaths, latest_id):
    max_pages = 10 
    
    if latest_id == 0: # initializer일때
        notices = [["ID", "category", "title", "date", "uploader", "views", "link"]]
    else:
        notices = [] # updater일떄

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(max_pages):
            offset = page_num * 10
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            page.goto(full_url)
            page.wait_for_load_state("load")

            for i in range(1, 11):
                try:
                    id = page.locator(xpaths["id"].format(i)).inner_text(timeout=1000)
                    try:
                        category = page.locator(xpaths["category"].format(i)).inner_text(timeout=1000)
                    except:
                        category = "없음"

                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    if xpaths["views"] != "" :
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                    else:
                        views = 'null'
                    link = page.locator(xpaths["link"].format(i)).get_attribute("href")

                    id = id[3:] 
                    link = urljoin(base_url, link)

                    notices.append([int(id), category, title, date, uploader, views, link])

                except Exception as e:
                    print(f"❌ {i}번 공지 크롤링 오류 발생: {e}")
                    browser.close()
                    notices[1:] = sorted(notices[1:], key=lambda x: x[0])
                    return notices

        browser.close()
        notices[1:] = sorted(notices[1:], key=lambda x: x[0])

    return notices