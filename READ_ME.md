# 🏪 7Eleven Crawling Project

편의점의 **1+1** 및 **2+1** 행사 상품 정보를 수집하여 대시보드 형식으로 정보제공


###  설치 및 환경 설정

*- 필수 라이브러리(의존성) 설치*
```bash
[크롤]
pip install pandas requests beautifulsoup4
```
```bash
[대시보드]
pip install -r requirements.txt
```

*- 라이브러리 설명*
- **pandas**: 데이터 조작 및 분석을 위한 라이브러리로, 크롤링한 데이터를 DataFrame 형태로 저장하고 처리하는 데 사용
- **requests**: 웹 페이지에 HTTP 요청을 보내고 응답을 받는 라이브러리로, 크롤링할 웹 페이지의 HTML 소스를 가져오는 데 사용
- **beautifulsoup4**: HTML 및 XML 문서를 파싱하는 라이브러리로, 크롤링한 웹 페이지에서 필요한 정보를 추출하는 데 사용
- **streamlit**: 대시보드 및 웹 애플리케이션을 쉽게 만들 수 있는 라이브러리로, 크롤링한 데이터를 시각화하여 사용자에게 제공하는 데 사용
- **pandas** 데이터 조작 및 분석을 위한 라이브러리로, 여러 편의점의 CSV 파일을 하나로 합치고 행사 상품의 개당 가격이나 할인율을 계산하는 등 데이터를 처리하는 데 사용
- **plotly**  인터랙티브한 시각화 차트를 만드는 라이브러리로, 막대 그래프와 선 그래프로 보여주는 데 사용

*- 실행 방법*
- 크롤
```bash
python main.py
```
- 대시보드 실행
```bash
streamlit run app.py
```

*- 참고 사항*
-  크롤 실행시, 기존 Csv 파일이 존재할 경우,삭제후 시행.
-  대시보드 실행전 requirements.txt 파일내의 의존성 설치 필요.
-  초기에는 속도 느립니다, 이후 캐시된 데이터 이용으로 속도가 향상.


*- 배포 URL(LIVE URL)* 
- https://sevenevelendatacrawling-u2c2p3snucvvuwvmuetooy.streamlit.app/
 
