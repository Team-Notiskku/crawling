DEPARTMENT_URLS = {
    "경제대학": "https://ecostat.skku.edu/ecostat/notice_total.do",
    "학부대학": "https://hakbu.skku.edu/hakbu/community/under_notice.do",
    "유학대학": "https://scos.skku.edu/scos/community/under_notice.do",
    "문과대학": "https://liberalarts.skku.edu/liberal/community/under_notice.do",
    "사회과학대학": "https://sscience.skku.edu/sscience/community/under_notice.do",
    "경영대학": "https://biz.skku.edu/bizskk/notice.do",
    "사범대학": "https://biz.skku.edu/bizskk/notice.do",
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

DEPARTMENT_XPATHS = {
    "경제대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/span',
        "title": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[3]',
        "views": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[4]/span',
        "link": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dt/a'
    },
    "학부대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "유학대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "문과대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "사회과학대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "경영대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "사범대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "예술대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "자연과학대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "정보통신대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[4]/span',
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "소프트웨어융합대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": '//*[@id="jwxe_main_content"]/div/div/div[2]/ul/li[{}]/dl/dd/ul/li[4]/span',
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "공과대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "약학대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "생명공학대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "스포츠과학대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "의과대학": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    },
    "성균융합원": {
        "category": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/span[1]',
        "title": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a',
        "id": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[1]',
        "uploader": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[2]',
        "date": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dd/ul/li[3]',
        "views": "",
        "link": '//*[@id="jwxe_main_content"]/div/div/div/ul/li[{}]/dl/dt/a'
    }
}