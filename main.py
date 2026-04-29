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
    
    /* 頂部導航按鈕樣式 */
    .nav-container {{
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    .nav-btn button {{
        background: transparent !important;
        border: none !important;
        color: {t['title']} !important;
        font-size: 35px !important;
        font-weight: bold !important;
        cursor: pointer;
        padding: 0 15px !important;
    }}

    /* 月曆格子樣式 */
    .calendar-cell {{
        background-color: #FFFFFF;
        border: 1px solid {t['title']};
        border-radius: 4px;
        min-height: 110px;
        padding: 6px;
        position: relative;
        display: flex;
        flex-direction: column;
    }}
    .special-cell {{ background-color: {t['special_bg']} !important; }}
    .date-num {{ color: {t['title']}; font-weight: bold; font-size: 1rem; }}
    .special-label {{ color: {t['title']}; font-size: 0.75rem; font-weight: bold; margin-top: auto; }}
    .note-preview {{ color: #555; font-size: 0.7rem; line-height: 1.2; margin-top: 2px; }}

    /* 隱形按鈕覆蓋格子 */
    div.stButton > button {{
        width: 100%; height: 110px; background: transparent; border: none; color: transparent;
        position: absolute; top: 0; left: 0; z-index: 10;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部標題 ---
# --- 4. 頂部標題 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)

# --- 5. 翻頁導航列 (具備方框的按鈕) ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
nav_btn_cols = st.columns(2)

with nav_btn_cols[0]:
    if st.button("Last Month", key="btn_last", use_container_width=True):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()

with nav_btn_cols[1]:
    if st.button("Next Month", key="btn_next", use_container_width=True):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 裝飾圖片區 ---
# 圖片移動到導航列下方，避免與翻頁按鈕擠在一起
img_cols = st.columns(6)
for idx, img_name in enumerate(t["imgs"]):
    if os.path.exists(img_name):
        img_cols[idx].image(Image.open(img_name), use_container_width=True)

# --- 6. 標籤選擇區 (如果有需要可以保留) ---
st.columns(4) # 這裡可以放你的 生咖/演唱會 等標籤按鈕
# --- 6. 縮小圖裝飾 ---
# 裝飾圖移到導航列下方，避免遮擋按鈕觸控區域


# --- 6. 年月顯示 ---


# --- 7. 月曆主體 ---
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
                preview = (note[:15] + '...') if len(note) > 15 else note

                st.markdown(f"""
                    <div class="calendar-cell {special_class}">
                        <div class="date-num">{day:02d}{heart}</div>
                        <div class="note-preview">{preview}</div>
                        {special_text}
                    </div>
                """, unsafe_allow_html=True)
                
                # 格子點擊按鈕
                if st.button("", key=f"btn-{date_key}"):
                    st.session_state.editing_date = date_key

# --- 8. 編輯視窗 ---
if st.session_state.editing_date:
    st.markdown("---")
    with st.expander(f"📝 編輯 {st.session_state.editing_date}", expanded=True):
        current_note = st.session_state.notes.get(st.session_state.editing_date, "")
        new_note = st.text_area("內容：", value=current_note, height=100)
        
        c1, c2 = st.columns(2)
        if c1.button("儲存"):
            st.session_state.notes[st.session_state.editing_date] = new_note
            with open("grid_notes.json", 'w', encoding='utf-8') as f:
                json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
            st.session_state.editing_date = None
            st.rerun()
        if c2.button("取消"):
            st.session_state.editing_date = None
            st.rerun() 加上去
按鈕不要陰影
