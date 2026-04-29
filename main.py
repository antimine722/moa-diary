import streamlit as st
import calendar
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
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "special_bg": "#FFDAB9"},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "special_bg": "#C6E2FF"},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "special_bg": "#FFC0CB"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "special_bg": "#E6E6FA"}
}

# --- 2. 狀態初始化 ---
if 'notes' not in st.session_state:
    if os.path.exists("grid_notes.json"):
        with open("grid_notes.json", 'r', encoding='utf-8') as f:
            st.session_state.notes = json.load(f)
    else:
        st.session_state.notes = {}

# 預設為 2026 年 4 月
if 'curr_year' not in st.session_state: st.session_state.curr_year = 2026
if 'curr_month' not in st.session_state: st.session_state.curr_month = 4

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; margin-bottom: 0px !important; }}
    
    /* 移除所有標籤空間 */
    div[data-testid="stWidgetLabel"] {{ display: none !important; }}

    /* 導航按鈕樣式 */
    .nav-container div.stButton > button {{
        background-color: white !important;
        color: {t['title']} !important;
        border: 1px solid {t['title']} !important;
        border-radius: 10px !important;
        height: 40px !important;
        font-weight: bold !important;
    }}

    /* 日期顯示列 (上方色塊) */
    .date-header {{
        background-color: {t['title']};
        color: white;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 8px 8px 0 0;
        font-size: 1rem;
    }}
    
    .special-header {{ background-color: #FF6B6B !important; }}

    /* 打字方框樣式 */
    div[data-baseweb="textarea"] {{
        border: 2px solid {t['title']} !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background-color: white !important;
    }}
    textarea {{
        font-size: 0.9rem !important;
        padding: 8px !important;
        color: #333 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 標題與裝飾圖 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)

# 顯示裝飾圖
img_cols = st.columns(6)
# 根據主題選擇圖片前綴 (例如紫色用 ang, 橘色用 fox)
img_prefix = {
    "purple": "ang", "orange": "fox", "blue": "dog", "pink": "bear"
}.get(theme_choice, "fox")

for idx in range(1, 7):
    img_name = f"{img_prefix}{idx:02d}.jpg"
    if os.path.exists(img_name):
        img_cols[idx-1].image(Image.open(img_name), use_container_width=True)

# --- 5. 導航列 (年 / 月) ---
st.markdown('<div class="nav-container">', unsafe_allow_html=True)
# 使用 5 欄位排版，讓按鈕對稱，中間顯示年/月
nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([1, 1, 3, 1, 1])

with nav_c2:
    if st.button("<", key="prev"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()

with nav_c3:
    # 修改為「年 / 月」格式
    display_date = f"{st.session_state.curr_year} / {st.session_state.curr_month:02d}"
    st.markdown(f"<h2 style='text-align:center; color:{t['title']}; margin:0; font-family:sans-serif;'>{display_date}</h2>", unsafe_allow_html=True)

with nav_c4:
    if st.button(">", key="next"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- 6. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
week_head = st.columns(7)
for i, d in enumerate(week_names):
    week_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:0.8rem; margin:15px 0 5px 0;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            
            with cols[i]:
                # 1. 上方日期條
                header_class = "date-header special-header" if is_special else "date-header"
                heart = " ❤️" if is_special else ""
                st.markdown(f'<div class="{header_class}">{day:02d}{heart}</div>', unsafe_allow_html=True)
                
                # 2. 打字方框 (無標籤、無年月日字樣)
                current_text = st.session_state.notes.get(date_key, "")
                new_text = st.text_area(
                    label="note_input", 
                    value=current_text,
                    key=f"input-{date_key}",
                    height=100,
                    label_visibility="collapsed"
                )
                
                if new_text != current_text:
                    st.session_state.notes[date_key] = new_text
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)

                if is_special:
                    st.markdown(f"<p style='font-size:0.7rem; color:#FF6B6B; text-align:center; margin-top:2px;'>{SPECIAL_DAYS[short_key]}</p>", unsafe_allow_html=True)
