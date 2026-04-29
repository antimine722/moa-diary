import streamlit as st
import calendar
import json
import os
from PIL import Image

# 頁面配置
st.set_page_config(page_title="MOA Diary Grid", layout="wide")

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
    h1, h2 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; }}
    
    /* 日期顯示列 */
    .date-header {{
        background-color: {t['title']};
        color: white;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 4px 4px 0 0;
        font-size: 0.9rem;
        display: flex;
        justify-content: space-between;
    }}
    
    /* 特別日子的日期列顏色 */
    .special-header {{
        background-color: #FF6B6B !important;
    }}

    /* 輸入方框的樣式微調 */
    div[data-baseweb="textarea"] {{
        border: 1px solid {t['title']} !important;
        border-top: none !important; /* 與上方日期列接合 */
        border-radius: 0 0 4px 4px !important;
        background-color: white !important;
    }}
    
    textarea {{
        font-size: 0.8rem !important;
        padding: 5px !important;
    }}

    /* 隱藏標籤空間 */
    div[data-testid="stWidgetLabel"] {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 標題與導航 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    if st.button("上個月", use_container_width=True):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with c2:
    if st.button("下個月", use_container_width=True):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

st.markdown(f"<h2>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h2>", unsafe_allow_html=True)

# --- 5. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_head = st.columns(7)
week_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
for i, d in enumerate(week_names):
    week_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; margin:0; font-size:0.7rem;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            
            with cols[i]:
                # 1. 上方日期顯示列
                header_class = "date-header special-header" if is_special else "date-header"
                heart = "❤️" if is_special else ""
                st.markdown(f"""
                    <div class="{header_class}">
                        <span>{day:02d} {heart}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # 2. 下方打字方框
                current_text = st.session_state.notes.get(date_key, "")
                new_text = st.text_area(
                    label=date_key,
                    value=current_text,
                    key=f"input-{date_key}",
                    height=90
                )
                
                # 特別日子的備註文字 (顯示在方框最下面)
                if is_special:
                    st.markdown(f"<div style='font-size:0.6rem; color:#FF6B6B; text-align:center; margin-top:-5px;'>{SPECIAL_DAYS[short_key]}</div>", unsafe_allow_html=True)
                
                # 儲存邏輯
                if new_text != current_text:
                    st.session_state.notes[date_key] = new_text
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)

# 底部提醒
st.markdown("---")
st.caption("💡 提示：輸入完畢後點擊格子以外的地方即可自動儲存。")
