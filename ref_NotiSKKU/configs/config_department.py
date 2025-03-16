DEPT_URLS = {
    "경제대학": "https://ecostat.skku.edu/ecostat/notice_total.do",
    "학부대학": "https://hakbu.skku.edu/hakbu/community/under_notice.do",
    "유학대학": "https://scos.skku.edu/scos/community/under_notice.do",
    "문과대학": "https://liberalarts.skku.edu/liberal/community/under_notice.do",
    "사회과학대학": "https://sscience.skku.edu/sscience/community/under_notice.do",
    "경영대학": "https://biz.skku.edu/bizskk/notice.do",
    "사범대학": "https://coe.skku.edu/coe/community/under_notice.do",
    "예술대학": "https://art.skku.edu/art/community/under_notice.do",
    "자연과학대학": "https://cscience.skku.edu/cscience/community/under_notice.do",
    "정보통신대학": "https://ice.skku.edu/ice/community/notice.do",
    "소프트웨어융합대학": "https://sw.skku.edu/sw/notice.do",
    "공과대학": "https://enc.skku.edu/enc/community/under_notice.do",
    "약학대학": "https://pharm.skku.edu/bbs/board.php?bo_table=notice",
    "생명공학대학": "https://biotech.skku.edu/biotech/community/under_notice.do",
    "스포츠과학대학": "https://sport.skku.edu/sports/community/under_notice.do",
    "의과대학": "https://www.skkumed.ac.kr/community_notice.asp",
    "성균융합원": "https://ics.skku.edu/ics/community/under_notice.do"
}

pin_dept = ["경영대학"]
other_dept = ["약학대학", "의과대학"]
has_views_dept = ["경제대학", "정보통신대학", "소프트웨어융합대학"]

DEPT_XPATHS = {}
for department in DEPT_URLS.keys():

    ## other majors 예외처리
    if department == "약학대학":
        DEPT_XPATHS[department] = {
            "category": '',
            "title": '//*[@id="board_list"]/li[{}]/a/article/h2',
            "id": '',
            "uploader": '//*[@id="board_list"]/li[{}]/a/article/p/span[1]',
            "date": '//*[@id="board_list"]/li[{}]/a/article/p/span[2]',
            "views": '',
            "link": '//*[@id="board_list"]/li[{}]/a'
        }
        continue
    
    if department == "의과대학":
        DEPT_XPATHS[department] = {
            "category": '',
            "title": '//*[@id="jwxe_main_content"]/div/div/ul/li[{}]/dl/dt/a',
            "id": '//*[@id="jwxe_main_content"]/div/div/ul/li[{}]/dl/dd/ul/li[1]',
            "uploader": '//*[@id="jwxe_main_content"]/div/div/ul/li[{}]/dl/dd/ul/li[2]',
            "date": '//*[@id="jwxe_main_content"]/div/div/ul/li[{}]/dl/dd/ul/li[3]',
            "views": '//*[@id="jwxe_main_content"]/div/div/ul/li[{}]/dl/dd/ul/li[4]',
            "link": '//*[@id="jwxe_main_content"]/div/div/ul/li[{}]/dl/dt/a'
        }
        continue
    
    # if (department in pin_dept): # 상단 고정 공지 있는 경우
    #     DEPT_XPATHS[department] = {}
        
    ## 조회수 필드가 있는 경우
    if (department in has_views_dept or department == "경영대학") : 
        DEPT_XPATHS[department] = {
            "category": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/span',
            "title": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/a',
            "id": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[1]',
            "uploader": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[2]',
            "date": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[3]',
            "views": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[4]/span',
            "link": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/a'
        }
        continue
    
    ## 그 외 모든 경우
    DEPT_XPATHS[department] = { 
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    }