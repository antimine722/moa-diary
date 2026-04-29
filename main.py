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
if 'editing_date' not in st.session_state: st.session_state.editing_date = None

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2, h3 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; }}
    
    /* 格子基本樣式 */
    .calendar-cell {{
        background-color: #FFFFFF;
        border: 1px solid {t['title']};
        border-radius: 4px;
        min-height: 120px;
        padding: 6px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}
    
    /* 特殊日底色 */
    .special-cell {{
        background-color: {t['special_bg']} !important;
    }}
    
    .date-num {{
        color: {t['title']};
        font-weight: bold;
        font-size: 1.1rem;
    }}
    
    .special-label {{
        color: {t['title']};
        font-size: 0.8rem;
        font-weight: bold;
        margin-top: auto;
    }}

    .note-text {{
        color: #555;
        font-size: 0.75rem;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
    }}
    
    /* 讓按鈕隱形但可以點擊格子 */
    div.stButton > button {{
        width: 100%;
        height: 120px;
        background: transparent;
        border: none;
        color: transparent;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 10;
    }}
    div.stButton > button:hover {{ color: transparent; background: rgba(0,0,0,0.05); }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部裝飾 ---
st.title("✨ MOA Diary")
cols = st.columns(6)
for idx, img_name in enumerate(t["imgs"]):
    if os.path.exists(img_name):
        cols[idx].image(Image.open(img_name), use_container_width=True)

# --- 5. 月份導航 ---
n1, n2, n3 = st.columns([1, 2, 1])
with n1:
    if st.button("❮", key="prev"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with n2:
    st.subheader(f"{st.session_state.curr_year} / {st.session_state.curr_month:02d}")
with n3:
    if st.button("❯", key="next"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 6. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_head = st.columns(7)
for i, d in enumerate(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
    week_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:0.8rem;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    days = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            note = st.session_state.notes.get(date_key, "")
            
            with days[i]:
                # 繪製格子 HTML
                special_class = "special-cell" if is_special else ""
                heart = " ❤️" if is_special else ""
                special_text = f'<div class="special-label">{SPECIAL_DAYS[short_key]}</div>' if is_special else ""
                
                st.markdown(f"""
                    <div class="calendar-cell {special_class}">
                        <div class="date-num">{day:02d}{heart}</div>
                        <div class="note-text">{note}</div>
                        {special_text}
                    </div>
                """, unsafe_allow_html=True)
                
                # 點擊格子彈出編輯器
                if st.button("", key=f"btn-{date_key}"):
                    st.session_state.editing_date = date_key

# --- 7. 編輯彈窗 ---
if st.session_state.editing_date:
    with st.expander(f"📝 編輯 {st.session_state.editing_date} 的日記", expanded=True):
        current_note = st.session_state.notes.get(st.session_state.editing_date, "")
        new_note = st.text_area("內容：", value=current_note, height=100)
        
        c1, c2 = st.columns(2)
        if c1.button("儲存"):
            st.session_state.notes[st.session_state.editing_date] = new_note
            with open("grid_notes.json", 'w', encoding='utf-8') as f:
                json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
            st.session_state.editing_date = None
            st.rerun()
        if c2.button("關閉"):
            st.session_state.editing_date = None
            st.rerun()
