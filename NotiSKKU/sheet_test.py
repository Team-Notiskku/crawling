import os
from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from googleapiclient.discovery import build
from google.oauth2 import service_account

# ✅ Google Sheets API 설정
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1rn5W6x50T9H0Nijobqwi616Le77j3nrBACfDXDqVsjA"  # Google Sheets ID (URL에서 확인 가능)
SHEET_NAME = "시트1"  # Google Sheets의 시트 이름

CREDENTIALS_JSON = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if CREDENTIALS_JSON:
    with open("credentials.json", "w") as f:
        f.write(CREDENTIALS_JSON)  # Secret에서 가져온 JSON을 credentials.json 파일로 생성

    creds = service_account.Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)
    print("✅ Google Sheets API 인증 성공!")
else:
    raise ValueError("❌ GOOGLE_APPLICATION_CREDENTIALS 환경 변수가 설정되지 않았습니다.")

def update_google_sheets(data):
    """크롤링한 데이터를 Google Sheets에 업로드"""
    range_name = f"{SHEET_NAME}!A1"  # A1부터 데이터 입력
    body = {"values": data}
    
    service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    print("✅ Google Sheets 업데이트 완료!")


def get_notice():
    """공지사항 크롤링 (여러 페이지) 및 Google Sheets 업데이트"""
    base_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"
    max_pages = 5  # 크롤링할 페이지 수 (5페이지 = 50개 공지)
    
    # 데이터 저장 리스트 (Google Sheets 헤더 포함)
    notices = [["카테고리", "제목", "고유 ID", "게시자", "날짜", "조회수", "링크"]]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # UI 없이 실행
        page = browser.new_page()

        for page_num in range(max_pages):
            offset = page_num * 10  # 10 단위로 증가 (0, 10, 20, 30...)
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            print(f"📢 페이지 {page_num + 1} (offset={offset}) 크롤링 중...")
            page.goto(full_url)
            page.wait_for_load_state("load")

            # 공지사항 리스트 크롤링
            for i in range(1, 11):  # 1~10번 공지 크롤링
                try:
                    category = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/span[1]').inner_text(timeout=1000)
                    title = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').inner_text(timeout=1000)
                    unique_id = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[1]').inner_text(timeout=1000)
                    poster = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[2]').inner_text(timeout=1000)
                    date = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[3]').inner_text(timeout=1000)
                    views = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[4]/span').inner_text(timeout=1000)
                    next_url = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').get_attribute("href")
                    
                    unique_id = unique_id[3:]  # "No.12345" 형태에서 "12345"만 추출
                    next_url = urljoin(base_url, next_url)

                    # 데이터 추가
                    notices.append([category, title, unique_id, poster, date, views, next_url])

                except Exception as e:
                    print(f"❌ {i}번 공지 크롤링 오류 발생: {e}")

        browser.close()

    return notices


# 크롤링 실행 및 Google Sheets 업데이트
notices_data = get_notice()
if notices_data:
    update_google_sheets(notices_data)
else:
    print("❌ 크롤링된 데이터가 없습니다.")