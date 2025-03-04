from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from department_config import DEPARTMENT_URLS, DEPARTMENT_XPATHS

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1YX53hQ1oHjAhl8wvsa6nIq6P5Eh0SMyV8SaN8hsPyTg"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAMES = list(DEPARTMENT_URLS.keys())

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

def get_latest(SHEET_NAME):
    range_name = f"{SHEET_NAME}!A:A"  
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=range_name
    ).execute()

    values = result.get("values", [])
    
    if(len(values) == 0) :
        latest_id = 0
    else:
        latest_id = values[-1]
    return latest_id[0], len(values) + 1 

def get_notice(latest_id, SHEET_NAME):
    base_url = DEPARTMENT_URLS[SHEET_NAME]
    max_pages = 10 
    
    notices = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        xpaths = DEPARTMENT_XPATHS[name]

        for page_num in range(max_pages):
            offset = page_num * 10
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            print(f"📢 페이지 {page_num + 1} (offset={offset}) 크롤링 중...")
            page.goto(full_url)
            page.wait_for_load_state("load")

            for i in range(1, 11):
                try:
                    id = page.locator(xpaths["id"].format(i)).inner_text(timeout=1000)
                    id = id[3:] 
                    if int(id) == latest_id:
                        browser.close()
                        notices[1:] = sorted(notices[1:], key=lambda x: x[0])  
                        return notices 
                    
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
                    link = urljoin(base_url, link)

                    notices.append([id, category, title, date, uploader, views, link])

                except Exception as e:
                    print(f"❌ {i}번 공지 크롤링 오류 발생: {e}")
                    browser.close()
                    notices[0:] = sorted(notices[0:], key=lambda x: x[0])
                    return notices

        browser.close()
        notices[0:] = sorted(notices[0:], key=lambda x: x[0])

    return notices

def update_google_sheets(new_notices, next_row, SHEET_NAME):
    if not new_notices:
        print("✅ 새로운 공지가 없습니다.")
        return

    range_name = f"{SHEET_NAME}!A{next_row}"  

    body = {"values": new_notices}

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS", 
        body=body
    ).execute()

    print(f"✅ Google Sheets에 {len(new_notices)}개의 새로운 공지를 추가했습니다. (시작 행: {next_row})")

def update_last_modified_time(SHEET_NAME):
    """Google Sheets의 특정 셀에 최종 편집 시각 업데이트"""
    last_modified_time = datetime.now().strftime("최종 편집 일시: %Y-%m-%d %H시 %M분 %S초")
    range_name = f"{SHEET_NAME}!A1"  

    body = {"values": [[last_modified_time]]}

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"✅ 최종 편집 시각 업데이트 완료: {last_modified_time}")



for name in SHEET_NAMES:
    latest_id, next_row = get_latest(name)
    latest_id = int(latest_id)
    new_notices = get_notice(latest_id, name)
    update_google_sheets(new_notices, next_row, name)
    update_last_modified_time(name)
