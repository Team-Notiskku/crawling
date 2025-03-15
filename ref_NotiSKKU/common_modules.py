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
                    print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                    browser.close()
                    notices[1:] = sorted(notices[1:], key=lambda x: x[0])
                    return notices

        browser.close()
        notices[1:] = sorted(notices[1:], key=lambda x: x[0])

    return notices

def get_pinned(base_url, xpaths, latest_id, is_arch):
    max_pages = 10 
    
    if latest_id == 0:  # initializer일 때
        notices = [["ID", "category", "title", "date", "uploader", "views", "link"]]
    else:
        notices = []  # updater일 때

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for page_num in range(max_pages):
            offset = page_num * 10
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            page.goto(full_url)
            page.wait_for_load_state("load")
            if is_arch == 1:
                pinned_notices = page.locator('//*[@id="item_body"]/div[2]/div[1]/div/div[2]/div/div/div/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
            else:
                pinned_notices = page.locator('//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li/dl/dt[contains(@class, "board-list-content-top")]')
            pinned_count = pinned_notices.count()  # 고정 공지 개수

            notice_count = 0
            i = pinned_count + 1  # 고정 공지 이후부터 시작

            while notice_count < 10:
                try:
                    id = page.locator(xpaths["id"].format(i)).inner_text(timeout=1000)
                    try:
                        category = page.locator(xpaths["category"].format(i)).inner_text(timeout=1000)
                    except:
                        category = "없음"

                    title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                    date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                    uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                    if xpaths["views"] != "":
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                    else:
                        views = 'null'
                    link = page.locator(xpaths["link"].format(i)).get_attribute("href")

                    id = id[3:] 
                    link = urljoin(base_url, link)

                    notices.append([int(id), category, title, date, uploader, views, link])

                    notice_count += 1 
                    i += 1

                except Exception as e:
                    print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                    browser.close()
                    notices[1:] = sorted(notices[1:], key=lambda x: x[0])
                    return notices

        browser.close()
        notices[1:] = sorted(notices[1:], key=lambda x: x[0])

    return notices

def get_exceptions(SHEET_NAME, base_url, xpaths, latest_id):
    if SHEET_NAME == "화학과":
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
                        id = 0
                        category = "없음"
                        title = page.locator(xpaths["title"].format(i)).inner_text(timeout=1000)
                        date = page.locator(xpaths["date"].format(i)).inner_text(timeout=1000)
                        date = date[14:]
                        uploader = page.locator(xpaths["uploader"].format(i)).inner_text(timeout=1000)
                        uploader = uploader[9:]
                        views = page.locator(xpaths["views"].format(i)).inner_text(timeout=1000)
                        views = views[6:]
                        link = page.locator(xpaths["link"].format(i)).get_attribute("href")
                         
                        link = urljoin(base_url, link)

                        notices.append([int(id), category, title, date, uploader, views, link])

                    except Exception as e:
                        print(f"{i-1}번 공지 이후로 공지가 없습니다. 크롤링을 종료합니다.")
                        browser.close()
                        notices.reverse()
                        if latest_id == 0: # initializer일때
                            notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])
                        return notices

            browser.close()
            notices.reverse()
            if latest_id == 0: # initializer일때
                notices.insert(0, ["ID", "category", "title", "date", "uploader", "views", "link"])

        return notices
    else:
        return []