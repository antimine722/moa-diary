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

# --- 3. UI 樣式 (強制修正格子) ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2, h3 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; }}
    
    /* 容器：強制設定高度並允許內容重疊 */
    .day-wrapper {{
        position: relative;
        background-color: #FFFFFF;
        border: 1px solid {t['title']};
        border-radius: 4px;
        height: 140px;
        margin-bottom: 10px;
        padding: 5px;
        overflow: hidden;
    }}
    .special-wrapper {{ background-color: {t['special_bg']} !important; }}

    /* 日期數字與愛心 */
    .date-header {{
        color: {t['title']};
        font-weight: bold;
        font-size: 1rem;
        z-index: 1;
    }}

    /* 輸入框：完全透明且覆蓋整個格子 */
    .stTextArea textarea {{
        background-color: transparent !important;
        border: none !important;
        color: #444 !important;
        height: 90px !important;
        font-size: 0.85rem !important;
        padding: 0 !important;
        z-index: 2;
    }}
    .stTextArea label {{ display: none !important; }}
    
    /* 特殊日文字：固定在底部 */
    .special-label-bottom {{
        position: absolute;
        bottom: 5px;
        left: 5px;
        color: {t['title']};
        font-size: 0.75rem;
        font-weight: bold;
        pointer-events: none; /* 防止擋住輸入點擊 */
    }}
    
    /* 導航按鈕樣式 */
    .nav-btn button {{
        background-color: transparent !important;
        border: none !important;
        color: {t['title']} !important;
        font-size: 24px !important;
        font-weight: bold !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部導航 (左右翻頁 + 縮小圖) ---
st.title("✨ MOA Diary")

n_col = st.columns([1, 2, 3, 2, 1])

with n_col[0]:
    if st.button("❮", key="prev_btn"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()

with n_col[1]:
    sub = st.columns(3)
    for i in range(3):
        if os.path.exists(t["imgs"][i]): sub[i].image(Image.open(t["imgs"][i]), width=35)

with n_col[2]:
    st.subheader(f"{st.session_state.curr_year} / {st.session_state.curr_month:02d}")

with n_col[3]:
    sub_r = st.columns(3)
    for i in range(3, 6):
        if os.path.exists(t["imgs"][i]): sub_r[i-3].image(Image.open(t["imgs"][i]), width=35)

with n_col[4]:
    if st.button("❯", key="next_btn"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 5. 月曆網格 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
cols_head = st.columns(7)
for i, d in enumerate(week_days):
    cols_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-weight:bold; font-size:0.7rem;'>{d}</p>", unsafe_allow_html=True)

for week in cal:
    days = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            
            with days[i]:
                # 組合 HTML 結構
                sp_class = "special-wrapper" if is_special else ""
                heart = " ❤️" if is_special else ""
                
                st.markdown(f'<div class="day-wrapper {sp_class}"><div class="date-header">{day:02d}{heart}</div>', unsafe_allow_html=True)
                
                # 直接打字的輸入框
                val = st.session_state.notes.get(date_key, "")
                new_val = st.text_area("", value=val, key=f"txt-{date_key}")
                
                if new_val != val:
                    st.session_state.notes[date_key] = new_val
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
                
                # 特殊日文字放在最下面
                if is_special:
                    st.markdown(f'<div class="special-label-bottom">{SPECIAL_DAYS[short_key]}</div>', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
