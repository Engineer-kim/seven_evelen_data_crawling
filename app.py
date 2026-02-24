import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="이달의 편의점 행사", layout="wide")

# CSS 로드
def local_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

@st.cache_data(ttl=3600)
def get_combined_data():
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not csv_files: return pd.DataFrame()
    list_df = [pd.read_csv(f) for f in csv_files]
    df = pd.concat(list_df, ignore_index=True)
    df['event'] = df['event'].str.replace(' ', '', regex=False)
    df['price'] = df['price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0).astype(int)

    def calc(row):
        e, p = row['event'], row['price']
        if e == '1+1': return p // 2
        if e == '2+1': return p // 3
        if e == '3+1': return p // 4
        return p

    df['unit_price'] = df.apply(calc, axis=1)
    return df.drop_duplicates(subset=['name', 'event', 'brand'])

df = get_combined_data()

# 1. 사이드바 필터
st.sidebar.header("🔍 필터 및 정렬")
brand_list = sorted(df['brand'].unique().tolist())
selected_brands = st.sidebar.multiselect("🏪 편의점 브랜드", brand_list, default=brand_list)
search_query = st.sidebar.text_input("상품명 검색", "")
event_types = sorted([e for e in df['event'].unique().tolist() if e != '세일'])
selected_events = st.sidebar.multiselect("🏷️ 행사 종류", event_types, default=event_types)
sort_option = st.sidebar.selectbox("💰 가격 정렬", ["기본 (랜덤)", "상품 가격 낮은 순", "상품 가격 높은 순"])

# 필터링 및 정렬
filtered_df = df[(df['brand'].isin(selected_brands)) & (df['event'].isin(selected_events)) & (
    df['name'].str.contains(search_query, case=False))]

if sort_option == "상품 가격 낮은 순":
    filtered_df = filtered_df.sort_values(by='unit_price', ascending=True)
elif sort_option == "상품 가격 높은 순":
    filtered_df = filtered_df.sort_values(by='unit_price', ascending=False)

# 2. 페이지네이션
items_per_page = 30
total_pages = max((len(filtered_df) // items_per_page) + (1 if len(filtered_df) % items_per_page > 0 else 0), 1)

if 'current_page' not in st.session_state:
    st.session_state.current_page = 1

query_hash = search_query + str(selected_events) + str(selected_brands) + sort_option
if 'last_query' not in st.session_state or st.session_state.last_query != query_hash:
    st.session_state.current_page = 1
    st.session_state.last_query = query_hash

# 3. 메인 화면
st.title(f"🏪 {datetime.now().strftime('%Y년 %m월')} 편의점 행사 정보")

start_idx = (st.session_state.current_page - 1) * items_per_page
display_df = filtered_df.iloc[start_idx : start_idx + items_per_page]

if not display_df.empty:
    cols = st.columns(5)
    for idx, (_, row) in enumerate(display_df.iterrows()):
        with cols[idx % 5]:
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

    # 하단 네비게이션
    st.markdown("---")
    _, b1, p_box, b2, _ = st.columns([4, 0.3, 1, 0.3, 4])

    with b1:
        if st.button("❮", key="prev_btn") and st.session_state.current_page > 1:
            st.session_state.current_page -= 1
            st.rerun()

    with p_box:
        st.markdown(f"<div class='page-info-box'>{st.session_state.current_page} / {total_pages}</div>", unsafe_allow_html=True)

    with b2:
        if st.button("❯", key="next_btn") and st.session_state.current_page < total_pages:
            st.session_state.current_page += 1
            st.rerun()
else:
    st.warning("결과가 없습니다.")