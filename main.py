import streamlit as st
import calendar
from datetime import datetime
import json
import os
from PIL import Image

# 頁面配置
st.set_page_config(page_title="MOA Diary Mobile", layout="wide")

# --- 1. 核心資料 ---
SPECIAL_DAYS = {
    "03-04": "Debut Day", "08-22": "MOA Day", "09-13": "YEONJUN Day",
    "12-05": "SOOBIN Day", "03-13": "BEOMGYU Day", "02-05": "TAEHYUN Day",
    "08-14": "HUENINGKAI Day"
}

THEMES = {
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "imgs": ["fox01.jpg", "fox02.jpg", "fox03.jpg"]},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "imgs": ["dog01.jpg", "dog02.jpg", "dog03.jpg"]},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "imgs": ["bear01.jpg", "bear02.jpg", "bear03.jpg"]},
    "gray": {"bg": "#F5F5F5", "title": "#708090", "imgs": ["cat01.jpg", "cat02.jpg", "cat03.jpg"]},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "imgs": ["ang01.jpg", "ang02.jpg", "ang03.jpg"]}
}

# --- 2. 狀態初始化 ---
if 'notes' not in st.session_state:
    if os.path.exists("grid_notes.json"):
        with open("grid_notes.json", 'r', encoding='utf-8') as f:
            st.session_state.notes = json.load(f)
    else:
        st.session_state.notes = {}

if 'curr_year' not in st.session_state:
    st.session_state.curr_year = 2026
if 'curr_month' not in st.session_state:
    st.session_state.curr_month = 4

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2, h3, p {{ color: {t['title']} !important; font-family: 'Microsoft JhengHei'; }}
    .stTextArea textarea {{ border: 2px solid {t['title']}; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部裝飾圖案 ---
st.title("✨ MOA Diary")

# 顯示該主題的可愛圖片
img_cols = st.columns(len(t["imgs"]))
for idx, img_name in enumerate(t["imgs"]):
    if os.path.exists(img_name):
        img = Image.open(img_name)
        img_cols[idx].image(img, use_container_width=True)

# --- 5. 月份導航 ---
c1, c2, c3 = st.columns([1, 2, 1])
with c1:
    if st.button("❮"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with c2:
    st.markdown(f"<h2 style='text-align: center;'>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h2>", unsafe_allow_html=True)
with c3:
    if st.button("❯"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 6. 月曆本體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 顯示星期頭
week_head = st.columns(7)
for i, d in enumerate(week_days):
    week_head[i].markdown(f"**{d}**")

# 顯示日期格
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            
            # 裝飾特別日子
            label = f"{day:02d}"
            if short_key in SPECIAL_DAYS:
                label = f"{day:02d} ❤️"
            
            val = st.session_state.notes.get(date_key, "")
            new_val = cols[i].text_area(label, value=val, key=date_key, height=100)
            
            if new_val != val:
                st.session_state.notes[date_key] = new_val
                with open("grid_notes.json", 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
