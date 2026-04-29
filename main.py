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

# 包含灰色主題
THEMES = {
    "grey": {"bg": "#F5F5F5", "title": "#708090", "special": "#A9A9A9"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "special": "#B399D4"},
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "special": "#FF6B6B"},
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

# --- 3. UI 樣式 ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1 {{ color: {t['title']} !important; text-align: center; font-family: 'Microsoft JhengHei'; }}
    div[data-testid="stWidgetLabel"] {{ display: none !important; }}
    
    /* 日期按鈕樣式 */
    .stButton > button {{
        width: 100%;
        border-radius: 8px 8px 0 0 !important;
        border: 1px solid {t['title']} !important;
        background-color: white !important;
        color: {t['title']} !important;
    }}
    
    /* 選中後的按鈕樣式 */
    .stButton > button[kind="primary"] {{
        background-color: {t['title']} !important;
        color: white !important;
        border: 1px solid white !important;
    }}

    /* 打字框樣式 */
    div[data-baseweb="textarea"] {{
        border: 2px solid {t['title']} !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        background-color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 圖片顯示 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)
img_cols = st.columns(6)
prefix = {"purple": "ang", "orange": "fox", "blue": "dog", "pink": "bear", "grey": "wolf"}.get(theme_choice, "fox")
for idx in range(1, 7):
    path = f"{prefix}{idx:02d}.jpg"
    if os.path.exists(path): 
        img_cols[idx-1].image(Image.open(path), use_container_width=True)

# --- 5. 導航與標籤 ---
c1, c2, c3, c4, c5 = st.columns([1, 1, 3, 1, 1])
with c2: 
    if st.button("<", key="prev_btn"): 
        st.session_state.curr_month -= 1
        if st.session_state.curr_month == 0:
            st.session_state.curr_month = 12
            st.session_state.curr_year -= 1
        st.rerun()
with c3: 
    st.markdown(f"<h2 style='text-align:center; color:{t['title']}; margin:0;'>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h2>", unsafe_allow_html=True)
with c4: 
    if st.button(">", key="next_btn"): 
        st.session_state.curr_month += 1
        if st.session_state.curr_month == 13:
            st.session_state.curr_month = 1
            st.session_state.curr_year += 1
        st.rerun()

# 標籤按鈕區
st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
tag_cols = st.columns(len(QUICK_TAGS))
for idx, tag in enumerate(QUICK_TAGS):
    if tag_cols[idx].button(f"★{tag}", key=f"tag_btn_{tag}", use_container_width=True):
        if st.session_state.sel_date:
            d = st.session_state.sel_date
            old_val = st.session_state.notes.get(d, "")
            new_val = f"{old_val} ★{tag} ".strip()
            
            # 同步更新
            st.session_state.notes[d] = new_val
            st.session_state[f"txt-{d}"] = new_val
            
            with open("grid_notes.json", 'w', encoding='utf-8') as f:
                json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
            st.rerun()
        else:
            st.warning("請先點擊下方的日期數字選中格子！")

# --- 6. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
h_cols = st.columns(7)
for i, d in enumerate(week_names):
    h_cols[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:0.8rem;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            d_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_spec = short_key in SPECIAL_DAYS
            is_sel = st.session_state.sel_date == d_key
            
            with cols[i]:
                # 日期按鈕標頭
                label = f"{day:02d}{'❤️' if is_spec else ''}"
                if st.button(label, key=f"btn-{d_key}", type="primary" if is_sel else "secondary"):
                    st.session_state.sel_date = d_key
                    st.rerun()
                
                # 文字輸入框
                txt_val = st.text_area(
                    label=d_key, 
                    value=st.session_state.notes.get(d_key, ""), 
                    key=f"txt-{d_key}", 
                    height=85, 
                    label_visibility="collapsed"
                )
                
                # 手動編輯存檔
                if txt_val != st.session_state.notes.get(d_key, ""):
                    st.session_state.notes[d_key] = txt_val
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)

                if is_spec:
                    st.markdown(f"<p style='font-size:0.7rem; color:{t['special']}; text-align:center; margin:0;'>{SPECIAL_DAYS[short_key]}</p>", unsafe_allow_html=True)
