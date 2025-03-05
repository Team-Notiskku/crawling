from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime
from major_config import MAJOR_URLS, MAJOR_XPATHS

SERVICE_ACCOUNT_FILE = "notiskku-449608-4c2aa194efc2.json" ## 병합 시 수정 필요 (credentials.json)
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1XOv61iZQiPwc2CeqU4lnZsnmpUIhp4Tnjcsk84mHihU"  ## 병합 시 수정 필요 (1RPTHVpyEJb4mZs9sz10E5OwIpZB-3YJcfrg5H7dFqhM)
SHEET_NAMES = list(MAJOR_URLS.keys())

creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build("sheets", "v4", credentials=creds)

def update_google_sheets(name, data):
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
    base_url = MAJOR_URLS[name]
    max_pages = 10 
    
    notices = [["ID", "category", "title", "date", "uploader", "views", "link"]]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        xpaths = MAJOR_XPATHS[name]

        for page_num in range(max_pages):
            offset = page_num * 10
            notice_url = f"?mode=list&&articleLimit=10&article.offset={offset}"
            full_url = urljoin(base_url, notice_url)
            
            #print(f"📢 페이지 {page_num + 1} (offset={offset}) 크롤링 중...")
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
                    print(f"❌ {i}번 공지 크롤링 오류 발생: {e}, {name}")
                    
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


done_major = ["국어국문학과", "문헌정보학과", "중어중문학과", "글로벌리더학부", "미디어커뮤니케이션학과", "사회학과", "심리학과", "아동·청소년학과", "정치외교학과",
              "행정학과", "글로벌경제학과", "통계학과", "교육학과", "수학교육과", "컴퓨터교육과", "한문교육과", "물리학과", "데이터사이언스융합전공" ]
pin_major = ["독어독문학과", "러시아어문학과", "사학과", "영어영문학과", "철학과", "프랑스어문학과", "한문학과", "사회복지학과", "소비자학과", "경영학과", "글로벌경영학과",
             "디자인학과", "무용학과", "연기예술학과", "의상학과", "영상학과", "수학과", "화학과", "소재부품융합공학과", "전기전자공학부", "차세대반도체공학연계전공",
              "글로벌융합학부 공통", "소프트웨어학과", "인공지능융합전공",    ]



for name in SHEET_NAMES:
    # 이미 성공한 학과
    if name in done_major:
        continue
    # 상단 고정 공지가 있는 학과
    if name in pin_major:
        print(f"😭 상단 고정 공지가 있습니다: {name}")
        continue
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