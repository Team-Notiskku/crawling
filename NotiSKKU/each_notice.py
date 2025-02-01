from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def get_notice():
    base_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"

    # Playwright 실행
    with sync_playwright() as p:
        # 브라우저 실행
        browser = p.chromium.launch(headless=False)  # 브라우저 UI 활성화
        page = browser.new_page()

        # 공지 페이지로 이동
        # offset = (페이지 번호 -1)*10
        print("공지 페이지로 이동 중...")
        notice_url = "?mode=list&&articleLimit=10&article.offset=0"
        page.goto(urljoin(base_url, notice_url))
        page.wait_for_load_state("load")

        # 공지사항 리스트 정보 크롤링
        print("공지사항 데이터 수집 중...")
        next_url = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[1]/dl/dt/a').get_attribute("href")
        next_url = urljoin(base_url, next_url)
        page.goto(next_url)

        input("종료하려면 Enter 키를 누르세요.")
        

# 함수 실행
get_notice()

# 크롤링한 데이터 출력
