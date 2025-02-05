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

def update_google_sheets(data):
    """크롤링한 데이터를 Google Sheets에 업로드"""
    range_name = f"{SHEET_NAME}!A1"
    body = {"values": data}
    
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    print("✅ Google Sheets 업데이트 완료!")


def get_notice():
    base_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"
    max_pages = 10 
    
    notices = [["ID", "category", "title", "date", "uploader", "views", "link"]]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(max_pages):
            offset = page_num * 10
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            print(f"📢 페이지 {page_num + 1} (offset={offset}) 크롤링 중...")
            page.goto(full_url)
            page.wait_for_load_state("load")

            for i in range(1, 11):
                try:
                    id = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[1]').inner_text(timeout=1000)
                    category = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/span[1]').inner_text(timeout=1000)
                    title = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').inner_text(timeout=1000)
                    date = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[3]').inner_text(timeout=1000)
                    uploader = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[2]').inner_text(timeout=1000)
                    views = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[4]/span').inner_text(timeout=1000)
                    link = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').get_attribute("href")
                    
                    id = id[3:] 
                    link = urljoin(base_url, link)

                    notices.append([id, category, title, date, uploader, views, link])

                except Exception as e:
                    print(f"❌ {i}번 공지 크롤링 오류 발생: {e}")

        browser.close()

        notices[1:] = sorted(notices[1:], key=lambda x: x[0])

    return notices


notices_data = get_notice()
if notices_data:
    update_google_sheets(notices_data)
else:
    print("❌ 크롤링된 데이터가 없습니다.")