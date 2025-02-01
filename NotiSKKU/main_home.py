from playwright.sync_api import sync_playwright
from urllib.parse import urljoin

def get_notice():
    with sync_playwright() as p:
        # 브라우저 실행
        browser = p.chromium.launch(headless=True)  # 브라우저 UI 활성화
        page = browser.new_page()

        # 공지 페이지로 이동
        # offset = (페이지 번호 -1)*10
        print("공지 페이지로 이동 중...")
        base_url = "https://www.skku.edu/skku/campus/skk_comm/notice01.do"
        notice_url = "?mode=list&&articleLimit=10&article.offset=0"
        page.goto(urljoin(base_url, notice_url))
        page.wait_for_load_state("load")

        # 공지사항 리스트 정보 크롤링
        print("공지사항 데이터 수집 중...")
        notices = []

        for i in range(1, 11):  # 1부터 10까지 반복
            try:
                category = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/span[1]').inner_text(timeout=1000)
                title = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').inner_text(timeout=1000)
                unique_id = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[1]').inner_text(timeout=1000)
                poster = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[2]').inner_text(timeout=1000)
                date = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[3]').inner_text(timeout=1000)
                views = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dd/ul/li[4]/span').inner_text(timeout=1000)
                next_url = page.locator(f'//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{i}]/dl/dt/a').get_attribute("href")
                
                unique_id = unique_id[3:]
                next_url = urljoin(base_url, next_url)
                # 각 공지사항 정보를 딕셔너리로 저장
                notice = {
                    "category": category,
                    "title": title,
                    "unique_id": unique_id,
                    "poster": poster,
                    "date": date,
                    "views": views,
                    "next url": next_url
                }

                notices.append(notice)
            except Exception as e:
                print(f"리스트 {i}번 항목 크롤링 중 오류 발생: {e}")

        browser.close()
        return notices

# 함수 실행
notices = get_notice()

# 크롤링한 데이터 출력
for idx, notice in enumerate(notices, start=1):
    print(f"공지사항 {idx}:")
    for key, value in notice.items():
        print(f"  {key}: {value}")
    print("-" * 40)

