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
    "YEONJUN": {"bg": "#FFF5EE", "title": "#E9967A", "left_imgs": ["fox01.jpg", "fox02.jpg", "fox03.jpg"], "right_imgs": ["fox04.jpg", "fox05.jpg", "fox06.jpg"]},
    "SOOBIN": {"bg": "#F0F8FF", "title": "#4682B4", "left_imgs": ["dog01.jpg", "dog02.jpg", "dog03.jpg"], "right_imgs": ["dog04.jpg", "dog05.jpg", "dog06.jpg"]},
    "BEOMGYU": {"bg": "#FFF0F5", "title": "#DB7093", "left_imgs": ["bear01.jpg", "bear02.jpg", "bear03.jpg"], "right_imgs": ["bear04.jpg", "bear05.jpg", "bear06.jpg"]},
    "TAEHYUN": {"bg": "#F5F5F5", "title": "#708090", "left_imgs": ["cat01.jpg", "cat02.jpg", "cat03.jpg"], "right_imgs": ["cat04.jpg", "cat05.jpg", "cat06.jpg"]},
    "HUENINGKAI": {"bg": "#F8F4FF", "title": "#9370DB", "left_imgs": ["ang01.jpg", "ang02.jpg", "ang03.jpg"], "right_imgs": ["ang04.jpg", "ang05.jpg", "ang06.jpg"]}
}

# --- 2. 狀態初始化 ---
if 'notes' not in st.session_state:
    if os.path.exists("grid_notes.json"):
        with open("grid_notes.json", 'r', encoding='utf-8') as f:
            st.session_state.notes = json.load(f)
    else:
        st.session_state.notes = {}

if 'curr_year' not in st.session_state:
    st.session_state.curr_year = datetime.now().year
if 'curr_month' not in st.session_state:
    st.session_state.curr_month = datetime.now().month

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2, h3, p {{ color: {t['title']} !important; font-family: 'Microsoft JhengHei'; }}
    .stTextArea textarea {{ border: 1px solid {t['title']}; border-radius: 10px; padding: 5px;}}
    .calendar-container {{ border: 1px solid #ccc; padding: 10px; border-radius: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部裝飾圖案 (方案一：使用 st.columns 並限制圖片寬度) ---
st.title(" MOA Diary")

# 合併圖片列表並顯示
all_imgs = t["left_imgs"] + t["right_imgs"]
img_cols = st.columns(6) # 建立 6 個 columns

# 在每個 column 中顯示一個圖片，並限制寬度
for idx, img_name in enumerate(all_imgs):
    if os.path.exists(img_name):
        img = Image.open(img_name)
        # 設定寬度，例如 60px
        img_cols[idx].image(img, width=60) 

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
    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h3>", unsafe_allow_html=True)
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

# 用 markdown 表格或 st.columns 來實現月曆網格，適配手機
st.write("---") # 加上一條線分隔

# 用 columns 來實作星期頭
week_head = st.columns(7)
for i, d in enumerate(week_days):
    week_head[i].markdown(f"**{d}**")

# 用 columns 來實作日期格
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
            # 調整 text_area 高度和樣式
            new_val = cols[i].text_area(label, value=val, key=date_key, height=100)
            
            if new_val != val:
                st.session_state.notes[date_key] = new_val
                with open("grid_notes.json", 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
