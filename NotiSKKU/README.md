## makefile 사용 (채연 로컬)
### NotiSKKU 디렉토리 내 
1. make init -> initial_data.py (100개 데이터 초기 크롤링)
2. make test -> test.py (초기 데이터 이외 추가 데이터 업데이트)





### XPath

``` python
# 카테고리
//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{1부터 10사이의 숫자}]/dl/dt/span[1]

# 제목
//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{1부터 10사이의 숫자}]/dl/dt/a/text()

# 고유 번호
//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{1부터 10사이의 숫자}]/dl/dd/ul/li[1]/text()

# 게시자
//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{1부터 10사이의 숫자}]/dl/dd/ul/li[2]/text()

# 게시일
//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{1부터 10사이의 숫자}]/dl/dd/ul/li[3]/text()

# 조회수
//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[{1부터 10사이의 숫자}]/dl/dd/ul/li[4]/span

# 연결 URL
//*[@id="jwxe_main_content"]/div/div/div[1]/div[1]/ul/li[1]/dl/dt/a
```
