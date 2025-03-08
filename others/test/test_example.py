from playwright.sync_api import sync_playwright

def test_google_search():
    with sync_playwright() as p:
        # 브라우저 실행
        browser = p.chromium.launch(headless=True) #False로 바꾸면 브라우저 실제로 실행됨
        page = browser.new_page()

        # Google로 이동
        print("Google로 이동 중...")
        page.goto("https://www.google.com")
        page.wait_for_load_state("load")

        # 검색창 대기 및 입력
        print("검색창 로드 대기...")
        page.wait_for_selector("textarea[name='q']", timeout=10000)
        print("검색어 입력 중...")
        page.fill("textarea[name='q']", "Playwright Python")
        page.press("textarea[name='q']", "Enter")

        # 검색 결과 대기 및 출력
        print("결과 로드 대기...")
        page.wait_for_selector("#search", timeout=10000)
        first_result = page.query_selector("h3").inner_text()
        print(f"첫 번째 검색 결과: {first_result}")

        browser.close()

test_google_search()
