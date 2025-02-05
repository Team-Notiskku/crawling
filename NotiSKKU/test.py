from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1rn5W6x50T9H0Nijobqwi616Le77j3nrBACfDXDqVsjA"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAME = "전체 공지"  ## 전체 / 단과대 / 학과 별 리스트 형태로 구현 예정

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

def get_latest():
    range_name = f"{SHEET_NAME}!A:A"  
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID, range=range_name
    ).execute()

    values = result.get("values", [])

    latest_id = values[-1]
    return latest_id[0], len(values) + 1 

def get_notice(latest_id):
    base_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"
    max_pages = 10 

    notices = []

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
                    id = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[1]').inner_text(timeout=1000)
                    id = id[3:]

                    if int(id) == latest_id:
                        browser.close()
                        notices[0:] = sorted(notices[0:], key=lambda x: x[0])  
                        return notices 

                    
                    category = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/span[1]').inner_text(timeout=1000)
                    title = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').inner_text(timeout=1000)
                    date = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[3]').inner_text(timeout=1000)
                    uploader = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[2]').inner_text(timeout=1000)
                    views = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[4]/span').inner_text(timeout=1000)
                    link = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').get_attribute("href")

                    link = urljoin(base_url, link)

                    notices.append([id, category, title, date, uploader, views, link])

                except Exception as e:
                    print(f"❌ {i}번 공지 크롤링 오류 발생: {e}")

    return notices

def update_google_sheets(new_notices, next_row):
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

latest_id, next_row = get_latest()
latest_id = int(latest_id)
new_notices = get_notice(latest_id)
update_google_sheets(new_notices, next_row)
