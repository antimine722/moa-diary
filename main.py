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
    
    /* 頂部翻頁按鈕：白色底方框、無陰影 */
    .nav-container div.stButton > button {{
        background-color: white !important;
        color: {t['title']} !important;
        border: 1px solid {t['title']} !important;
        box-shadow: none !important;
        border-radius: 8px !important;
        height: 45px !important;
        font-weight: bold !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}

    /* 月曆格子容器樣式 */
    .calendar-cell {{
        background-color: #FFFFFF;
        border: 1px solid {t['title']};
        border-radius: 4px;
        min-height: 110px;
        padding: 6px;
        position: relative;
        display: flex;
        flex-direction: column;
        z-index: 1;
    }}
    .special-cell {{ background-color: {t['special_bg']} !important; }}
    .date-num {{ color: {t['title']}; font-weight: bold; font-size: 1rem; }}
    .special-label {{ color: {t['title']}; font-size: 0.75rem; font-weight: bold; margin-top: auto; }}
    .note-preview {{ color: #555; font-size: 0.7rem; line-height: 1.2; margin-top: 2px; }}

    /* 格子點擊按鈕：必須完全透明且覆蓋整個格子 */
    .grid-btn-container {{
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 110px;
        z-index: 5;
    }}
    .grid-btn-container div.stButton > button {{
        width: 100% !important;
        height: 110px !important;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        box-shadow: none !important;
        padding: 0 !important;
    }}
    /* 防止點擊時出現原生按鈕的藍框或陰影 */
    .grid-btn-container div.stButton > button:focus, 
    .grid-btn-container div.stButton > button:active {{
        background: transparent !important;
        box-shadow: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部標題 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)

# --- 5. 翻頁導航列 (方框按鈕) ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
nav_btn_cols = st.columns(2)
with nav_btn_cols[0]:
    if st.button("Last Month", key="nav_prev", use_container_width=True):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with nav_btn_cols[1]:
    if st.button("Next Month", key="nav_next", use_container_width=True):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 年月顯示與裝飾圖 ---
st.markdown(f"<h2>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h2>", unsafe_allow_html=True)

img_cols = st.columns(6)
for idx, img_name in enumerate(t["imgs"]):
    if os.path.exists(img_name):
        img_cols[idx].image(Image.open(img_name), use_container_width=True)

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
                # 格子外觀佈局
                special_class = "special-cell" if is_special else ""
                heart = " ❤️" if is_special else ""
                special_text = f'<div class="special-label">{SPECIAL_DAYS[short_key]}</div>' if is_special else ""
                preview = (note[:15] + '...') if len(note) > 15 else note

                # 使用容器包裹格子內容與按鈕
                st.markdown(f"""
                    <div style="position: relative; height: 110px;">
                        <div class="calendar-cell {special_class}">
                            <div class="date-num">{day:02d}{heart}</div>
                            <div class="note-preview">{preview}</div>
                            {special_text}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 在同一欄位放置透明按鈕，透過 CSS 絕對定位覆蓋
                st.markdown('<div class="grid-btn-container">', unsafe_allow_html=True)
                if st.button("", key=f"btn-{date_key}"):
                    st.session_state.editing_date = date_key
                st.markdown('</div>', unsafe_allow_html=True)

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
            st.rerun()
