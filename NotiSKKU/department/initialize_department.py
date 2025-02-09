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

def update_google_sheets(name, data):
    """크롤링한 데이터를 Google Sheets에 업로드"""
    range_name = f"{name}!A2"
    body = {"values": data}
    
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    print("✅ Google Sheets 업데이트 완료!")


def get_notice(name):
    base_url = DEPARTMENT_URLS[name]
    max_pages = 10 
    
    notices = [["ID", "category", "title", "date", "uploader", "views", "link"]]

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
                    #print(f"❌ {i}번 공지 크롤링 오류 발생")
                    browser.close()
                    notices[1:] = sorted(notices[1:], key=lambda x: x[0])
                    return notices

        browser.close()
        notices[1:] = sorted(notices[1:], key=lambda x: x[0])

    return notices

def update_last_modified_time(name):
    """Google Sheets의 특정 셀에 최종 편집 시각 업데이트"""
    last_modified_time = datetime.now().strftime("최종 편집 일시: %Y-%m-%d %H시 %M분 %S초")
    range_name = f"{name}!A1"  

    body = {"values": [[last_modified_time]]}

    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()

    print(f"✅ 최종 편집 시각 업데이트 완료: {last_modified_time}")


for name in SHEET_NAMES:
    notices_data = get_notice(name)
    if notices_data:
        update_google_sheets(name, notices_data)
    else:
        print("❌ 크롤링된 데이터가 없습니다.")
    update_last_modified_time(name)
    
# notices_data = get_notice(SHEET_NAMES[2])
# if notices_data:
#     update_google_sheets(SHEET_NAMES[2], notices_data)
# else:
#     print("❌ 크롤링된 데이터가 없습니다.")
# update_last_modified_time(SHEET_NAMES[2])