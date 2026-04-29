import streamlit as st
import calendar
from datetime import datetime
import json
import os
from PIL import Image

# 頁面配置
st.set_page_config(page_title="MOA Diary", layout="wide")

# --- 1. 核心資料 ---
SPECIAL_DAYS = {
    "03-04": "Debut Day", "08-22": "MOA Day", "09-13": "YEONJUN Day",
    "12-05": "SOOBIN Day", "03-13": "BEOMGYU Day", "02-05": "TAEHYUN Day",
    "08-14": "HUENINGKAI Day"
}

THEMES = {
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "special_bg": "#FFDAB9", "imgs": ["fox01.jpg", "fox02.jpg", "fox03.jpg", "fox04.jpg", "fox05.jpg", "fox06.jpg"]},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "special_bg": "#C6E2FF", "imgs": ["dog01.jpg", "dog02.jpg", "dog03.jpg", "dog04.jpg", "dog05.jpg", "dog06.jpg"]},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "special_bg": "#FFC0CB", "imgs": ["bear01.jpg", "bear02.jpg", "bear03.jpg", "bear04.jpg", "bear05.jpg", "bear06.jpg"]},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "special_bg": "#E6E6FA", "imgs": ["ang01.jpg", "ang02.jpg", "ang03.jpg", "ang04.jpg", "ang05.jpg", "ang06.jpg"]}
}

# --- 2. 狀態初始化 ---
if 'notes' not in st.session_state:
    if os.path.exists("grid_notes.json"):
        with open("grid_notes.json", 'r', encoding='utf-8') as f:
            st.session_state.notes = json.load(f)
    else:
        st.session_state.notes = {}

if 'curr_year' not in st.session_state: st.session_state.curr_year = 2026
if 'curr_month' not in st.session_state: st.session_state.curr_month = 4

# --- 3. UI 樣式強化 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2, h3 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; }}
    
    /* 讓星期標題置中 */
    .week-text {{ text-align: center; color: {t['title']}; font-weight: bold; font-size: 0.8rem; margin: 0; }}

    /* 格子容器樣式 */
    .calendar-cell {{
        background-color: #FFFFFF;
        border: 1px solid {t['title']};
        border-radius: 4px;
        padding: 5px;
        min-height: 130px;
        display: flex;
        flex-direction: column;
    }}
    .special-cell {{ background-color: {t['special_bg']} !important; }}
    
    /* 隱藏 text_area 的預設邊框與標籤，使其融入格子 */
    .stTextArea textarea {{
        background-color: transparent !important;
        border: none !important;
        color: #333 !important;
        height: 75px !important;
        padding: 0 !important;
        font-size: 0.85rem !important;
    }}
    .stTextArea label {{ display: none !important; }}
    
    /* 特殊日文字樣式 */
    .special-label-text {{
        color: {t['title']};
        font-size: 0.75rem;
        font-weight: bold;
        margin-top: auto;
    }}
    
    /* 標籤按鈕樣式 */
    .tag-container {{ text-align: center; margin: 10px 0; }}
    .tag-item {{
        display: inline-block;
        padding: 2px 10px;
        margin: 2px;
        border: 1px solid {t['title']};
        color: {t['title']};
        border-radius: 12px;
        font-size: 0.7rem;
        background: white;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部導航 (左右翻頁按鈕 + 縮小圖) ---
st.title("✨ MOA Diary")

# 模擬原本 nav_frame 的布局
nav_cols = st.columns([0.5, 1.5, 2, 1.5, 0.5])

with nav_cols[0]:
    if st.button("❮", key="btn_prev"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()

with nav_cols[1]:
    img_sub = st.columns(3)
    for i in range(3):
        if os.path.exists(t["imgs"][i]):
            img_sub[i].image(Image.open(t["imgs"][i]), width=35)

with nav_cols[2]:
    st.subheader(f"{st.session_state.curr_year} / {st.session_state.curr_month:02d}")

with nav_cols[3]:
    img_sub_r = st.columns(3)
    for i in range(3, 6):
        if os.path.exists(t["imgs"][i]):
            img_sub_r[i-3].image(Image.open(t["imgs"][i]), width=35)

with nav_cols[4]:
    if st.button("❯", key="btn_next"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 5. 快速標籤 (生咖、演唱會...) ---
st.markdown(f"""
    <div class="tag-container">
        <span class="tag-item">生咖</span>
        <span class="tag-item">演唱會</span>
        <span class="tag-item">應援活動</span>
        <span class="tag-item">回歸</span>
    </div>
""", unsafe_allow_html=True)

# --- 6. 月曆主體 (直接輸入版) ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_head = st.columns(7)
for i, d in enumerate(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
    week_head[i].markdown(f"<p class='week-text'>{d}</p>", unsafe_allow_html=True)

for week in cal:
    days = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            
            with days[i]:
                # 繪製格子外殼
                special_class = "special-cell" if is_special else ""
                heart = " ❤️" if is_special else ""
                
                # 開啟格子容器
                st.markdown(f'<div class="calendar-cell {special_class}"><div style="color:{t["title"]}; font-weight:bold;">{day:02d}{heart}</div>', unsafe_allow_html=True)
                
                # 直接嵌入輸入框
                val = st.session_state.notes.get(date_key, "")
                new_val = st.text_area("", value=val, key=f"input-{date_key}")
                
                # 儲存邏輯
                if new_val != val:
                    st.session_state.notes[date_key] = new_val
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
                
                # 如果是特殊日，顯示底部文字
                if is_special:
                    st.markdown(f'<div class="special-label-text">{SPECIAL_DAYS[short_key]}</div>', unsafe_allow_html=True)
                
                # 關閉格子容器
                st.markdown('</div>', unsafe_allow_html=True)
