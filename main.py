import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime


def crawl_7eleven():
    print("🚀 세븐일레븐 데이터 수집을 시작합니다... (Ajax 직접 요청 방식)")

    all_products = []
    # pTab 1: 1+1, pTab 2: 2+1
    event_configs = [(1, "1+1"), (2, "2+1")]

    # 실제 데이터가 요청되는 URL (이미지 로그 확인 결과)
    url = "https://www.7-eleven.co.kr/product/listMoreAjax.asp"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://www.7-eleven.co.kr/product/presentList.asp"
    }

    for p_tab, event_label in event_configs:
        print(f"📦 {event_label} 상품 가져오는 중...")

        # intPageSize를 크게 잡아서 MORE 버튼 클릭 없이 한 번에 다 가져오기
        payload = {
            "intPageSize": 1000000,
            "pTab": p_tab,
            "currPage": 1
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # 상품 리스트는 li 태그로 구성됨
                items = soup.select("li")

                for item in items:
                    try:
                        # 1. 상품명 (alt 속성이나 txt_product 클래스)
                        img_tag = item.select_one(".pic_product img")
                        name = img_tag.get('alt', '').strip() if img_tag else item.select_one(".txt_product").get_text(
                            strip=True)

                        # 2. 가격 (숫자만 추출)
                        price_text = item.select_one(".price_list span").get_text(strip=True).replace(',', '')
                        price = int(price_text)

                        # 3. 행사 종류 (이미지 로그 상의 태그)
                        event = item.select_one(".tag_list_01 li").get_text(strip=True)

                        # 4. 이미지 주소
                        img_src = img_tag.get('src')
                        img_url = f"https://www.7-eleven.co.kr{img_src}"

                        all_products.append({
                            "brand": "7Eleven",
                            "name": name,
                            "price": price,
                            "event": event,
                            "img_url": img_url
                        })
                    except Exception:
                        continue
        except Exception as e:
            print(f"❌ {event_label} 수집 중 오류: {e}")

    # 2. 저장 형식 (CSV, utf-8-sig, 편의점명_날짜.csv)
    if all_products:
        df = pd.DataFrame(all_products)
        df = df[["brand", "name", "price", "event", "img_url"]]  # 열 이름 및 순서 고정

        today = datetime.now().strftime("%y%m%d")
        file_name = f"7Eleven_{today}.csv"

        df.to_csv(file_name, index=False, encoding='utf-8-sig')

        print("\n" + "=" * 40)
        print(f"🎉 수집 성공! 파일이 생성되었습니다.")
        print(f"📄 파일명: {file_name}")
        print(f"📊 총 상품 수: {len(all_products)}개")
        print("=" * 40)
    else:
        print("❌ 수집된 데이터가 없습니다. 다시 확인해 주세요.")


if __name__ == "__main__":
    crawl_7eleven()