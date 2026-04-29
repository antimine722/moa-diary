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

if 'curr_year' not in st.session_state: st.session_state.curr_year = 2026
if 'curr_month' not in st.session_state: st.session_state.curr_month = 4

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; padding-bottom: 20px; }}
    
    /* 移除所有標籤佔用的空間 */
    div[data-testid="stWidgetLabel"] {{ display: none !important; }}

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

# --- 4. 頂部裝飾 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)

# 顯示裝飾圖
img_cols = st.columns(6)
imgs = ["fox01.jpg", "fox02.jpg", "fox03.jpg", "fox04.jpg", "fox05.jpg", "fox06.jpg"]
for idx, img_name in enumerate(imgs):
    if os.path.exists(img_name):
        img_cols[idx].image(Image.open(img_name), use_container_width=True)

# 導航按鈕 (只有按鈕與當月數字)
nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([1, 1, 2, 1, 1])
with nav_c2:
    if st.button("＜", key="prev", use_container_width=True):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with nav_c3:
    st.markdown(f"<h2 style='text-align:center; color:{t['title']}; margin:0;'>{st.session_state.curr_month} 月</h2>", unsafe_allow_html=True)
with nav_c4:
    if st.button("＞", key="next", use_container_width=True):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 5. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
week_head = st.columns(7)
for i, d in enumerate(week_names):
    week_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:0.8rem; margin:10px 0;'><b>{d}</b></p>", unsafe_allow_html=True)

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
                
                # 2. 打字方框 (關鍵修正：label_visibility="collapsed")
                current_text = st.session_state.notes.get(date_key, "")
                new_text = st.text_area(
                    label="hidden", 
                    value=current_text,
                    key=f"input-{date_key}",
                    height=100,
                    label_visibility="collapsed" # 這行會把 2026-03-02 隱藏
                )
                
                if new_text != current_text:
                    st.session_state.notes[date_key] = new_text
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)

                if is_special:
                    st.markdown(f"<p style='font-size:0.7rem; color:#FF6B6B; text-align:center; margin:0;'>{SPECIAL_DAYS[short_key]}</p>", unsafe_allow_html=True)
