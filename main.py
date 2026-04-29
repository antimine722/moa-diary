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
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "special_bg": "#B0C4DE", "imgs": ["dog01.jpg", "dog02.jpg", "dog03.jpg", "dog04.jpg", "dog05.jpg", "dog06.jpg"]},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "special_bg": "#FFC0CB", "imgs": ["bear01.jpg", "bear02.jpg", "bear03.jpg", "bear04.jpg", "bear05.jpg", "bear06.jpg"]},
    "gray": {"bg": "#F5F5F5", "title": "#708090", "special_bg": "#D3D3D3", "imgs": ["cat01.jpg", "cat02.jpg", "cat03.jpg", "cat04.jpg", "cat05.jpg", "cat06.jpg"]},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "special_bg": "#E6E6FA", "imgs": ["ang01.jpg", "ang02.jpg", "ang03.jpg", "ang04.jpg", "ang05.jpg", "ang06.jpg"]}
}

# --- 2. 狀態初始化 ---
if 'notes' not in st.session_state:
    if os.path.exists("grid_notes.json"):
        with open("grid_notes.json", 'r', encoding='utf-8') as f:
            st.session_state.notes = json.load(f)
    else:
        st.session_state.notes = {}

if 'curr_year' not in st.session_state:
    st.session_state.curr_year = 2026
if 'curr_month' not in st.session_state:
    st.session_state.curr_month = 4

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2, h3 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; }}
    
    /* 讓一般日期與特殊日期的外框大小一致 */
    .date-container {{
        min-height: 140px;
        margin-bottom: 10px;
    }}
    
    /* 特殊日子的容器樣式 */
    .special-box {{ 
        background-color: {t['special_bg']}; 
        border-radius: 8px; 
        padding: 8px; 
        border: 1.5px solid {t['title']};
        text-align: center;
        margin-bottom: 4px;
    }}
    
    .special-text {{
        color: {t['title']};
        font-size: 0.85rem;
        font-weight: bold;
        margin: 0;
        line-height: 1.2;
    }}

    /* 強制設定輸入框為白色底，並統一樣式 */
    .stTextArea textarea {{
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 1.5px solid {t['title']} !important;
        border-radius: 8px !important;
        height: 80px !important;
    }}
    
    /* 隱藏輸入框的小標籤以節省空間 */
    label {{ font-weight: bold; color: {t['title']}; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部裝飾 ---
st.title("✨ MOA Diary")
cols = st.columns(6)
for idx, img_name in enumerate(t["imgs"]):
    if os.path.exists(img_name):
        cols[idx].image(Image.open(img_name), use_container_width=True)

# --- 5. 月份導航 ---
st.write("") # 留白
n1, n2, n3 = st.columns([1, 2, 1])
with n1:
    if st.button("❮"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with n2:
    st.subheader(f"{st.session_state.curr_year} / {st.session_state.curr_month:02d}")
with n3:
    if st.button("❯"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 6. 月曆表格 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_head = st.columns(7)
for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]):
    week_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; margin-bottom:0;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    days = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            
            with days[i]:
                st.markdown('<div class="date-container">', unsafe_allow_html=True)
                
                # 如果是特殊日子
                if short_key in SPECIAL_DAYS:
                    st.markdown(f"""
                        <div class="special-box">
                            <p class="special-text">{day:02d} ❤️</p>
                            <p class="special-text">{SPECIAL_DAYS[short_key]}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    display_label = "Edit" 
                else:
                    display_label = f"{day:02d}"

                val = st.session_state.notes.get(date_key, "")
                # 使用 label_visibility 讓一般日顯示數字，特殊日隱藏數字標籤
                new_val = st.text_area(
                    display_label, 
                    value=val, 
                    key=date_key, 
                    label_visibility="visible" if short_key not in SPECIAL_DAYS else "collapsed"
                )
                
                if new_val != val:
                    st.session_state.notes[date_key] = new_val
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
                
                st.markdown('</div>', unsafe_allow_html=True)
