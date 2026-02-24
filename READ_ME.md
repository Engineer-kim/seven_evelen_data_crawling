# 🏪 7Eleven Crawling Project

편의점의 **1+1** 및 **2+1** 행사 상품 정보를 수집하여 대시보드 형식으로 정보제공


###  설치 및 환경 설정

*- 필수 라이브러리 설치*
```bash
[크롤]
pip install pandas requests beautifulsoup4
```
```bash
[대시보드]
pip install -r requirements.txt
```

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
-  대시보드 실행전 requirements.txt 파일내의 의존성 설치해야함
-  초기에는 속도 느립니다, 이후 캐시된 데이터 이용으로 속도가 향상됩니다.

*- 배포 URL* 
- https://sevenevelendatacrawling-u2c2p3snucvvuwvmuetooy.streamlit.app/
 