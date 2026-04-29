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

# 標籤清單
QUICK_TAGS = ["生咖", "演唱會", "應援活動", "回歸"]

THEMES = {
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "special_bg": "#FFDAB9", "tag_bg": "#E9967A"},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "special_bg": "#C6E2FF", "tag_bg": "#4682B4"},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "special_bg": "#FFC0CB", "tag_bg": "#DB7093"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "special_bg": "#E6E6FA", "tag_bg": "#B8A2E3"}
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
if 'active_date' not in st.session_state: st.session_state.active_date = None

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; }}
    
    div[data-testid="stWidgetLabel"] {{ display: none !important; }}

    /* 導航按鈕 */
    .nav-container div.stButton > button {{
        background-color: white !important;
        color: {t['title']} !important;
        border: 1px solid {t['title']} !important;
        border-radius: 10px !important;
    }}

    /* 日期標題色塊 */
    .date-header {{
        background-color: {t['title']};
        color: white;
        font-weight: bold;
        padding: 4px 10px;
        border-radius: 8px 8px 0 0;
        font-size: 0.9rem;
    }}
    .special-header {{ background-color: #FF6B6B !important; }}
    
    /* 打字方框樣式 */
    div[data-baseweb="textarea"] {{
        border: 2px solid {t['title']} !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background-color: white !important;
    }}

    /* 標籤按鈕樣式 */
    .tag-container div.stButton > button {{
        background-color: {t['tag_bg']} !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-size: 0.8rem !important;
        padding: 2px 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部導航 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)

nav_c1, nav_c2, nav_c3, nav_c4, nav_c5 = st.columns([1, 1, 3, 1, 1])
with nav_c2:
    if st.button("<", key="prev"):
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with nav_c3:
    st.markdown(f"<h2 style='text-align:center; color:{t['title']}; margin:0;'>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h2>", unsafe_allow_html=True)
with nav_c4:
    if st.button(">", key="next"):
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# --- 5. 快速標籤列 (使用 ★ 字號) ---

tag_cols = st.columns(len(QUICK_TAGS) + 2)
for idx, tag in enumerate(QUICK_TAGS):
    with tag_cols[idx]:
        if st.button(tag, key=f"tag-{tag}", use_container_width=True):
            if st.session_state.active_date:
                # 取得當前輸入框的值 (直接從 session_state 拿最準)
                current_val = st.session_state.get(f"input-{st.session_state.active_date}", "")
                new_text = f"{current_val} ★{tag} ".strip()
                
                # 更新狀態與筆記
                st.session_state.notes[st.session_state.active_date] = new_text
                st.session_state[f"input-{st.session_state.active_date}"] = new_text
                
                with open("grid_notes.json", 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
                st.rerun()
            else:
                

# --- 6. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
cols_head = st.columns(7)
for i, d in enumerate(week_names):
    cols_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:0.8rem; margin:10px 0;'><b>{d}</b></p>", unsafe_allow_html=True)

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
                
                # 2. 下方直接打字方框
                current_text = st.session_state.notes.get(date_key, "")
                
                # 使用 text_area 讓內容顯示並可編輯
                new_text = st.text_area(
                    label=date_key,
                    value=current_text,
                    key=f"input-{date_key}",
                    height=90,
                    label_visibility="collapsed"
                )
                
                # 儲存與 active_date 追蹤
                if new_text != current_text:
                    st.session_state.notes[date_key] = new_text
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
                
                # 簡單邏輯：最後被操作的輸入框即為 active_date
                if st.session_state[f"input-{date_key}"] == new_text:
                    # 這邊用一個隱藏機制來更新當前選中的格子
                    if st.session_state.get(f"input-{date_key}") != "":
                        st.session_state.active_date = date_key

                if is_special:
                    st.markdown(f"<p style='font-size:0.7rem; color:#FF6B6B; text-align:center; margin:0;'>{SPECIAL_DAYS[short_key]}</p>", unsafe_allow_html=True)
