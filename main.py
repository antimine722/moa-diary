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
    "grey": {"bg": "#F5F5F5", "title": "#708090", "special": "#A9A9A9"},
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "special": "#FF6B6B"},
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

# --- 3. 極限手機排版 CSS ---
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    /* 全域背景 */
    .stApp {{ background-color: {t['bg']}; }}
    
    /* [核心] 強制 7 欄橫向排列，不允許換行 */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: flex-start !important;
        gap: 2px !important;
    }}
    
    [data-testid="column"] {{
        flex: 1 1 0% !important;
        min-width: 0 !important;
    }}

    /* 日期標題小按鈕 */
    .stButton > button {{
        width: 100% !important;
        padding: 0px !important;
        font-size: 10px !important;
        height: 22px !important;
        min-height: 22px !important;
        border-radius: 4px 4px 0 0 !important;
        border: 1px solid {t['title']} !important;
    }}
    
    /* 選中日期的高亮 */
    .stButton > button[kind="primary"] {{
        background-color: {t['title']} !important;
        color: white !important;
    }}

    /* 輸入框針對手機尺寸微調 */
    div[data-baseweb="textarea"] {{
        border: 1px solid {t['title']} !important;
        border-top: none !important;
        border-radius: 0 0 4px 4px !important;
        background-color: white !important;
    }}
    
    textarea {{
        font-size: 10px !important;
        line-height: 1.2 !important;
        padding: 4px !important;
    }}

    /* 隱藏所有多餘元件標籤 */
    div[data-testid="stWidgetLabel"] {{ display: none !important; }}
    
    /* 調整標籤按鈕區的高度 */
    .tag-container .stButton > button {{
        height: 30px !important;
        font-size: 12px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部導航與標籤 ---
st.markdown(f"<h2 style='text-align:center; color:{t['title']}; font-size:1.5rem; margin-bottom:10px;'>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h2>", unsafe_allow_html=True)

# 標籤按鈕 (維持橫排)
tag_cols = st.columns(len(QUICK_TAGS))
for idx, tag in enumerate(QUICK_TAGS):
    if tag_cols[idx].button(f"★{tag}", key=f"t-{tag}"):
        if st.session_state.sel_date:
            d = st.session_state.sel_date
            st.session_state.notes[d] = f"{st.session_state.notes.get(d, '')} ★{tag} ".strip()
            # 更新對應的輸入框內容
            st.session_state[f"txt-{d}"] = st.session_state.notes[d]
            with open("grid_notes.json", 'w', encoding='utf-8') as f:
                json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
            st.rerun()

# --- 5. 月曆主體 ---
week_names = ["M", "T", "W", "T", "F", "S", "S"]
h_cols = st.columns(7)
for i, name in enumerate(week_names):
    h_cols[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:10px; margin:0;'><b>{name}</b></p>", unsafe_allow_html=True)

cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            d_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            s_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_spec = s_key in SPECIAL_DAYS
            is_sel = st.session_state.sel_date == d_key
            
            with cols[i]:
                # 1. 日期標頭 (點擊即可選中該日，以便使用上方標籤)
                btn_label = f"{day:02d}{'❤️' if is_spec else ''}"
                if st.button(btn_label, key=f"btn-{d_key}", type="primary" if is_sel else "secondary"):
                    st.session_state.sel_date = d_key
                    st.rerun()
                
                # 2. 直接輸入格 (關鍵)
                content = st.text_area(
                    label=d_key,
                    value=st.session_state.notes.get(d_key, ""),
                    key=f"txt-{d_key}",
                    height=75,
                    label_visibility="collapsed"
                )
                
                # 自動存檔：當輸入框內容與紀錄不同時觸發
                if content != st.session_state.notes.get(d_key, ""):
                    st.session_state.notes[d_key] = content
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
        else:
            # 空白格也佔據空間以維持排版
            cols[i].markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
