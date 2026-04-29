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
    
    /* 快速標籤按鈕樣式 */
    .tag-btn {{
        display: inline-block;
        padding: 4px 12px;
        margin: 0 5px;
        background-color: {t['special_bg']};
        color: white;
        border-radius: 4px;
        font-size: 0.8rem;
        font-weight: bold;
    }}

    /* 格子基本樣式 */
    .calendar-cell {{
        background-color: #FFFFFF;
        border: 1px solid {t['title']};
        border-radius: 4px;
        min-height: 110px;
        padding: 5px;
        display: flex;
        flex-direction: column;
    }}
    
    .special-cell {{ background-color: {t['special_bg']} !important; }}
    
    .date-num {{ color: {t['title']}; font-weight: bold; font-size: 1rem; }}
    .special-label {{ color: {t['title']}; font-size: 0.75rem; font-weight: bold; margin-top: auto; }}
    .note-preview {{ color: #666; font-size: 0.7rem; margin-top: 2px; }}

    /* 隱形按鈕讓格子可點擊 */
    div.stButton > button {{
        width: 100%; height: 110px; background: transparent; border: none; color: transparent;
        position: absolute; top: 0; left: 0; z-index: 5;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部裝飾與圖片 (縮小版) ---
st.title("MOA Diary")

# 將圖片放在導航列左右，模擬你原本的 layout
nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns([1, 1, 2, 1, 1])

with nav_col1:
    if st.button("❮", key="prev"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()

with nav_col2:
    # 顯示前三張縮小圖
    sub_cols = st.columns(3)
    for i in range(3):
        img_p = t["imgs"][i]
        if os.path.exists(img_p):
            sub_cols[i].image(Image.open(img_p), width=40)

with nav_col3:
    st.subheader(f"{st.session_state.curr_year} / {st.session_state.curr_month:02d}")

with nav_col4:
    # 顯示後三張縮小圖
    sub_cols_r = st.columns(3)
    for i in range(3, 6):
        img_p = t["imgs"][i]
        if os.path.exists(img_p):
            sub_cols_r[i-3].image(Image.open(img_p), width=40)

with nav_col5:
    if st.button("❯", key="next"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 5. 快速標籤列 ---
st.markdown("<div style='text-align: center; margin-bottom: 15px;'>", unsafe_allow_html=True)
tag_cols = st.columns(8) # 用較多欄位來置中
tags = ["生咖", "演唱會", "應援活動", "回歸"]
for idx, tag in enumerate(tags):
    tag_cols[idx+2].markdown(f"<div class='tag-btn'>{tag}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 6. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_head = st.columns(7)
for i, d in enumerate(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
    week_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:0.75rem; margin:0;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    days = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            note = st.session_state.notes.get(date_key, "")
            
            with days[i]:
                special_class = "special-cell" if is_special else ""
                heart = " ❤️" if is_special else ""
                special_text = f'<div class="special-label">{SPECIAL_DAYS[short_key]}</div>' if is_special else ""
                
                st.markdown(f"""
                    <div class="calendar-cell {special_class}">
                        <div class="date-num">{day:02d}{heart}</div>
                        <div class="note-preview">{note[:10] + '...' if len(note) > 10 else note}</div>
                        {special_text}
                    </div>
                """, unsafe_allow_html=True)
                
                if st.button("", key=f"btn-{date_key}"):
                    st.session_state.editing_date = date_key

# --- 7. 編輯區塊 ---
if st.session_state.editing_date:
    with st.expander(f"📝 編輯 {st.session_state.editing_date}", expanded=True):
        new_note = st.text_area("內容：", value=st.session_state.notes.get(st.session_state.editing_date, ""))
        if st.button("儲存並關閉"):
            st.session_state.notes[st.session_state.editing_date] = new_note
            with open("grid_notes.json", 'w', encoding='utf-8') as f:
                json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
            st.session_state.editing_date = None
            st.rerun()
