import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="이달의 편의점 행사", layout="wide")

# 현재 날짜 기준 이번 달 표시 (예: 2026년 02월)
this_month = datetime.now().strftime("%Y년 %m월")
st.title(f"🏪 {this_month} 세븐 일레븐 편의점 통합 행사 정보")

# 1. 폴더 내 모든 CSV 파일 읽기
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]

if not csv_files:
    st.error("⚠️ 이번 달 수집된 데이터(CSV)가 없습니다!")
else:
    # 모든 CSV 파일을 하나로 합치기 (이번 달 데이터 통합)
    list_df = []
    for file in csv_files:
        temp_df = pd.read_csv(file)
        list_df.append(temp_df)

    # 중복 상품 제거 (이름과 행사종류가 같으면 중복으로 간주)
    df = pd.concat(list_df, ignore_index=True).drop_duplicates(subset=['name', 'event'])

    # 2. 사이드바 필터
    st.sidebar.header("🔍 검색 및 필터")

    # 상품명 검색 기능 추가
    search_query = st.sidebar.text_input("상품명 검색", "")

    # 행사 종류 필터
    event_types = df['event'].unique().tolist()
    selected_events = st.sidebar.multiselect("🏷️ 행사 종류", event_types, default=event_types)

    # 데이터 필터링 적용
    filtered_df = df[
        (df['event'].isin(selected_events)) &
        (df['name'].str.contains(search_query, case=False))
        ]

    # 3. 요약 정보
    st.info(f"💡 이번 달 총 **{len(filtered_df)}개**의 행사 상품이 검색되었습니다.")

    # 4. 상품 그리드 출력 (가로 5개씩)
    if not filtered_df.empty:
        cols = st.columns(5)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[idx % 5]:
                st.image(row['img_url'], use_container_width=True)
                # 상품명 길면 생략 처리하는 스타일
                st.markdown(f"**{row['name']}**")
                st.markdown(f"💰 **{int(row['price']):,}원**")
                st.caption(f"📍 {row['brand']} | {row['event']}")
                st.write("---")
    else:
        st.warning("검색 결과가 없습니다.")