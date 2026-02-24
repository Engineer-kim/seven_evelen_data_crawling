import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="이달의 편의점 행사", layout="wide")

# CSS: 레이아웃 고정
st.markdown("""
    <style>
    .img-container { width: 100%; aspect-ratio: 1 / 1; overflow: hidden; border-radius: 12px; background-color: #f8f9fa; display: flex; align-items: center; justify-content: center; border: 1px solid #eee; }
    .img-container img { width: 100%; height: 100%; object-fit: contain; }
    .product-card { margin-bottom: 20px; }
    .product-name { height: 45px; overflow: hidden; font-size: 0.9rem; font-weight: bold; margin-top: 10px; line-height: 1.2; }
    .unit-price { color: #ff4b4b; font-weight: bold; font-size: 1.1rem; }
    .total-price { color: #888; font-size: 0.8rem; text-decoration: line-through; }
    </style>
    """, unsafe_allow_html=True)


@st.cache_data(ttl=3600)
def get_combined_data():
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not csv_files: return pd.DataFrame()

    list_df = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(list_df, ignore_index=True)

    # 데이터 정제: 행사명 공백 제거
    df['event'] = df['event'].str.replace(' ', '', regex=False)

    # 가격 컬럼 정제 (숫자 외 문자 제거 및 정수화)
    df['price'] = df['price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(int)

    # 실질 단가 계산 로직
    def calc(row):
        e, p = row['event'], row['price']
        if e == '1+1': return p // 2
        if e == '2+1': return p // 3
        if e == '3+1': return p // 4
        return p

    df['unit_price'] = df.apply(calc, axis=1)

    # 브랜드별 상품 중복 제거
    return df.drop_duplicates(subset=['name', 'event', 'brand'])


df = get_combined_data()

# 2. 사이드바 필터 및 검색
st.sidebar.header("🔍 필터 및 정렬")

# 브랜드 필터
brand_list = sorted(df['brand'].unique().tolist())
selected_brands = st.sidebar.multiselect("🏪 편의점 브랜드", brand_list, default=brand_list)

search_query = st.sidebar.text_input("상품명 검색", "")

# 행사 종류 필터
event_types = sorted([e for e in df['event'].unique().tolist() if e != '세일'])
selected_events = st.sidebar.multiselect("🏷️ 행사 종류", event_types, default=event_types)

# 가격 정렬 옵션
sort_option = st.sidebar.selectbox(
    "💰 가격 정렬",
    ["기본 (랜덤)", "상품 가격 낮은 순", "상품 가격 높은 순"]
)

# 필터링 적용
filtered_df = df[
    (df['brand'].isin(selected_brands)) &
    (df['event'].isin(selected_events)) &
    (df['name'].str.contains(search_query, case=False))
    ]

# 정렬 적용
if sort_option == "상품 가격 낮은 순":
    filtered_df = filtered_df.sort_values(by='unit_price', ascending=True)
elif sort_option == "상품 가격 높은 순":
    filtered_df = filtered_df.sort_values(by='unit_price', ascending=False)

# 페이지네이션 (속도 최적화: 한 번에 30개만 렌더링)
items_per_page = 30
total_pages = max((len(filtered_df) // items_per_page) + (1 if len(filtered_df) % items_per_page > 0 else 0), 1)
page = st.sidebar.number_input("📄 페이지 번호", min_value=1, max_value=total_pages, step=1)

start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page
display_df = filtered_df.iloc[start_idx:end_idx]

# 3. 상품 출력
st.title(f"🏪 {datetime.now().strftime('%Y년 %m월')} 편의점 행사 통합 정보")
st.write(f"총 {len(filtered_df)}개의 상품이 검색되었습니다. (현재 {page} / {total_pages} 페이지)")

if not display_df.empty:
    cols = st.columns(5)
    for idx, (_, row) in enumerate(display_df.iterrows()):
        with cols[idx % 5]:
            # 증정 행사인 경우 줄 그어진 총액 표시
            total_price_html = f'<div class="total-price">총액: {row["price"]:,}원</div>' if "+" in row['event'] else ""
            st.markdown(f"""
                <div class="product-card">
                    <div class="img-container"><img src="{row['img_url']}"></div>
                    <div class="product-name">{row['name']}</div>
                    <div class="unit-price">개당 {row['unit_price']:,}원</div>
                    {total_price_html}
                    <div style="font-size: 0.8rem; color: #666; margin-top:5px;">
                        📍 {row['brand']} | <span style="background-color:#eee; padding:2px 5px; border-radius:4px;">{row['event']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            st.write("")
else:
    st.warning("선택하신 조건에 맞는 결과가 없습니다.")