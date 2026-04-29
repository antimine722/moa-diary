import streamlit as st
import calendar
import json
import os
from PIL import Image

# --- 1. 配置與核心資料 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

SPECIAL_DAYS = {
    "03-04": "Debut Day", "08-22": "MOA Day", "09-13": "YEONJUN Day",
    "12-05": "SOOBIN Day", "03-13": "BEOMGYU Day", "02-05": "TAEHYUN Day",
    "08-14": "HUENINGKAI Day"
}
QUICK_TAGS = ["生咖", "演唱會", "應援活動", "回歸"]

THEMES = {
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "special": "#FF6B6B"},
    "grey": {"bg": "#F5F5F5", "title": "#708090", "special": "#A9A9A9"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "special": "#B399D4"},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "special": "#5CACEE"},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "special": "#FF69B4"}
}

# --- 2. 狀態初始化 ---
if 'notes' not in st.session_state:
    if os.path.exists("grid_notes.json"):
        with open("grid_notes.json", 'r', encoding='utf-8') as f:
            st.session_state.notes = json.load(f)
    else: st.session_state.notes = {}

if 'curr_year' not in st.session_state: st.session_state.curr_year = 2026
if 'curr_month' not in st.session_state: st.session_state.curr_month = 4
if 'sel_date' not in st.session_state: st.session_state.sel_date = None

# --- 3. 強制手機版 7 欄佈局的 CSS ---
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1 {{ color: {t['title']} !important; text-align: center; margin-bottom: 0; }}
    
    /* 強制在手機上維持橫向排列 */
    [data-testid="column"] {{
        min-width: 0 !important;
        flex: 1 1 0% !important;
    }}
    
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
    }}

    /* 日期按鈕與標籤按鈕 */
    .stButton > button {{
        width: 100%;
        padding: 2px !important;
        font-size: 10px !important;
        border-radius: 4px !important;
        border: 1px solid {t['title']} !important;
    }}
    
    /* 選中狀態 */
    .stButton > button[kind="primary"] {{
        background-color: {t['title']} !important;
        color: white !important;
    }}

    /* 輸入框在手機上變小一點以免爆掉 */
    div[data-baseweb="textarea"] {{
        border: 1px solid {t['title']} !important;
        border-top: none !important;
        background-color: white !important;
    }}
    textarea {{
        font-size: 11px !important;
        padding: 5px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 裝飾與標籤列 ---
st.markdown(f"<h1>MOA Diary</h1>", unsafe_allow_html=True)

# 圖片列 (強制 6 欄)
img_cols = st.columns(6)
prefix = {"purple": "ang", "orange": "fox", "blue": "dog", "pink": "bear", "grey": "wolf"}.get(theme_choice, "fox")
for idx in range(1, 7):
    path = f"{prefix}{idx:02d}.jpg"
    if os.path.exists(path):
        img_cols[idx-1].image(Image.open(path), use_container_width=True)

# 導航
c1, c2, c3, c4, c5 = st.columns([1, 1, 3, 1, 1])
with c2: 
    if st.button("<", key="p"):
        st.session_state.curr_month -= 1
        st.rerun()
with c3:
    st.markdown(f"<p style='text-align:center; color:{t['title']}; font-weight:bold; margin-top:5px;'>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</p>", unsafe_allow_html=True)
with c4:
    if st.button(">", key="n"):
        st.session_state.curr_month += 1
        st.rerun()

# 標籤列 (強制橫排)
tag_cols = st.columns(len(QUICK_TAGS))
for idx, tag in enumerate(QUICK_TAGS):
    if tag_cols[idx].button(f"★{tag}", key=f"t-{tag}"):
        if st.session_state.sel_date:
            d = st.session_state.sel_date
            st.session_state.notes[d] = f"{st.session_state.notes.get(d, '')} ★{tag} ".strip()
            st.session_state[f"txt-{d}"] = st.session_state.notes[d]
            with open("grid_notes.json", 'w', encoding='utf-8') as f:
                json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
            st.rerun()

# --- 5. 月曆主體 ---
week_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
h_cols = st.columns(7)
for i, name in enumerate(week_names):
    h_cols[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:9px; margin:0;'><b>{name}</b></p>", unsafe_allow_html=True)

cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            d_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            is_spec = f"{st.session_state.curr_month:02d}-{day:02d}" in SPECIAL_DAYS
            is_sel = st.session_state.sel_date == d_key
            
            with cols[i]:
                # 日期按鈕
                if st.button(f"{day:02d}{'❤️' if is_spec else ''}", key=f"btn-{d_key}", 
                             type="primary" if is_sel else "secondary"):
                    st.session_state.sel_date = d_key
                    st.rerun()
                
                # 文字輸入 (高度縮小以符合手機螢幕)
                txt = st.text_area(label=d_key, value=st.session_state.notes.get(d_key, ""), 
                                   key=f"txt-{d_key}", height=60, label_visibility="collapsed")
                
                if txt != st.session_state.notes.get(d_key, ""):
                    st.session_state.notes[d_key] = txt
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
