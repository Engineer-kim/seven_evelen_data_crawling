import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="이달의 편의점 행사", layout="wide")

# CSS: 이미지와 상품 카드의 높이를 강제로 고정
st.markdown("""
    <style>
    .img-container {
        width: 100%;
        aspect-ratio: 1 / 1; /* 1:1 정사각형 고정 */
        overflow: hidden;
        border-radius: 12px;
        background-color: #f8f9fa;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid #eee;
    }
    .img-container img {
        width: 100%;
        height: 100%;
        object-fit: contain; /* 이미지가 잘리지 않게 프레임 안에 맞춤 (정사각형 유지) */
    }
    .product-card {
        margin-bottom: 20px;
    }
    .product-name {
        height: 45px; /* 상품명 두 줄 높이 고정 */
        overflow: hidden;
        font-size: 0.9rem;
        font-weight: bold;
        margin-top: 10px;
        line-height: 1.2;
    }
    </style>
    """, unsafe_allow_html=True)

# 현재 날짜 기준 제목
this_month = datetime.now().strftime("%Y년 %m월")
st.title(f"🏪 {this_month} 세븐 일레븐 통합 행사 정보")

# 1. 파일 로드 및 통합
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

if not csv_files:
    st.error("⚠️ 데이터 파일(CSV)이 없습니다!")
else:
    list_df = []
    for file in csv_files:
        list_df.append(pd.read_csv(file))
    df = pd.concat(list_df, ignore_index=True).drop_duplicates(subset=['name', 'event'])

    # 2. 필터 및 검색
    search_query = st.sidebar.text_input("상품명 검색", "")
    event_types = df['event'].unique().tolist()
    selected_events = st.sidebar.multiselect("🏷️ 행사 종류", event_types, default=event_types)

    filtered_df = df[
        (df['event'].isin(selected_events)) &
        (df['name'].str.contains(search_query, case=False))
    ]

    # 3. 상품 출력 (5열 그리드)
    if not filtered_df.empty:
        cols = st.columns(5)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[idx % 5]:
                # HTML을 사용하여 이미지와 텍스트 레이아웃 강제 고정
                st.markdown(f"""
                    <div class="product-card">
                        <div class="img-container">
                            <img src="{row['img_url']}">
                        </div>
                        <div class="product-name">{row['name']}</div>
                        <div style="color: #ff4b4b; font-weight: bold;">{int(row['price']):,}원</div>
                        <div style="font-size: 0.8rem; color: #666;">📍 {row['brand']} | {row['event']}</div>
                    </div>
                """, unsafe_allow_html=True)
                st.write("") # 간격용
    else:
        st.warning("검색 결과가 없습니다.")