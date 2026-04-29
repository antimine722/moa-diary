import streamlit as st
import calendar
from datetime import datetime
import json
import os

# 頁面配置 (適配手機)
st.set_page_config(page_title="MOA Diary Mobile", layout="centered")

# --- 1. 核心資料與邏輯 ---
SPECIAL_DAYS = {
    "03-04": "Debut Day", "08-22": "MOA Day", "09-13": "YEONJUN Day",
    "12-05": "SOOBIN Day", "03-13": "BEOMGYU Day", "02-05": "TAEHYUN Day",
    "08-14": "HUENINGKAI Day"
}

THEMES = {
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "btn": "#FFDAB9"},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "btn": "#ADD8E6"},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "btn": "#FFB6C1"},
    "gray": {"bg": "#F5F5F5", "title": "#708090", "btn": "#D3D3D3"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "btn": "#D1C4E9"}
}

STORAGE_FILE = "grid_notes.json"

def load_data():
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

# 初始化 Session State (這在網頁版非常重要)
if 'notes' not in st.session_state:
    st.session_state.notes = load_data()
if 'curr_year' not in st.session_state:
    st.session_state.curr_year = datetime.now().year
if 'curr_month' not in st.session_state:
    st.session_state.curr_month = datetime.now().month

# --- 2. UI 樣式設定 ---
theme_choice = st.sidebar.selectbox("選擇主題", list(THEMES.keys()), index=0)
t = THEMES[theme_choice]

# 用 CSS 模擬你的 Tkinter 背景色
st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2, h3 {{ color: {t['title']} !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 標題與導航 ---
st.title("✨ MOA Diary")

col_prev, col_mid, col_next = st.columns([1, 2, 1])
with col_prev:
    if st.button("❮"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with col_mid:
    st.subheader(f"{st.session_state.curr_year} / {st.session_state.curr_month:02d}")
with col_next:
    if st.button("❯"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year = 1
        st.rerun()

# --- 4. 標籤功能 ---
st.write("快速標籤：")
tag_col = st.columns(4)
tags = ["生咖", "演唱會", "應援活動", "回歸"]
for i, tag in enumerate(tags):
    if tag_col[i].button(tag):
        st.info(f"提示：請直接在下方格子輸入 ★ {tag}")

# --- 5. 月曆網格 (這是網頁版的改寫方式) ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            
            # 生日標記
            label = f"{day}"
            if short_key in SPECIAL_DAYS:
                label = f"{day} ❤️"
            
            # 讀取現有內容
            existing_note = st.session_state.notes.get(date_key, "")
            
            # 輸入框
            new_note = cols[i].text_area(label, value=existing_note, height=100, key=date_key)
            
            # 如果內容改變，存檔
            if new_note != existing_note:
                st.session_state.notes[date_key] = new_note
                with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
