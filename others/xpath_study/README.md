# XPATH
: XML Path Language 의 줄임말로, XML 문서의 특정 요소 또는 속성에 접근하기 위한 경로를 지정하는 언어. (웹 크롤링에 많이 사용됨)

## 기본 문법
``` html
&lt;!DOCTYPE html&gt;
&lt;html&gt;
&lt;head&gt;
	&lt;meta charset="utf-8"&gt;
	&lt;title&gt;hashscraper&lt;/title&gt;
&lt;/head&gt;
&lt;body&gt;
	&lt;div id="container"&gt;
		&lt;div class="title"&gt;
			&lt;p class="content1"&gt;let's start crawling!&lt;/p&gt;
			&lt;p class="content2"&gt;crawling is fun!&lt;/p&gt;
		&lt;/div&gt;
	&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;

```
1. title 부분의 XPath
``` 
/html/head/title
```
2. 첫번째 p 요소의 XPath (class와 같이 요소를 결부하는 속성을 “@”로 표현)
``` python
/html/body/div/div/p[@class='content1']
```

## 그 외 추가 문법
``` python
# 'aa'를 포함하는 class명을 가진 div 요소를 선택
div[contains(@class, "aa")]

# path에 해당하는 노드 중 마지막 노드
div[@class="aa")/span[last()]

# class명에 'aa'와 'bb'를 포함하는 img 요소를 선택
img[contains(@class, "aa") and contains(@class, "bb")]

#class명에 'aa' 또는 'bb'를 포함하는 img 요소를 선택
img[contains(@class, "aa") or contains(@class, "bb")]

#class명에 'aa'를 포함하고 'bb'를 포함하지 않는 img 요소를 선택
img[contains(@class, "aa") and not(contains(@class, "bb")
```