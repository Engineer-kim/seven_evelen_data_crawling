# 🏪 7Eleven Crawling Project

편의점의 **1+1** 및 **2+1** 행사 상품 정보를 수집하여 대시보드 형식으로 정보제공


###  설치 및 환경 설정

*- 필수 라이브러리 설치*
```bash
pip install pandas requests beautifulsoup4
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
-  기존 Csv 파일이 존재할 경우,삭제후 시행.
-  app.py 실행전 requirements.txt 파일내의 의존성 설치해야함

*- 배포 URL* 
- https://sevenevelendatacrawling-u2c2p3snucvvuwvmuetooy.streamlit.app/
 