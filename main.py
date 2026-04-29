import streamlit as st
import calendar
import json
import os

# 頁面配置
st.set_page_config(page_title="MOA Diary Direct", layout="wide")

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

# --- 3. UI 樣式 (關鍵：拔掉輸入框外框) ---
st.sidebar.title("設定")
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    h1, h2 {{ color: {t['title']} !important; text-align: center; }}
    
    /* 讓每一個日曆格子容器有邊框 */
    .day-box {{
        border: 1px solid {t['title']};
        border-radius: 5px;
        padding: 5px;
        background-color: white;
        min-height: 120px;
        margin-bottom: 5px;
    }}
    .special-box {{ background-color: {t['special_bg']} !important; }}

    /* 拔掉 Streamlit 輸入框的樣式，讓它像在格子內打字 */
    div[data-baseweb="textarea"] {{
        background-color: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    textarea {{
        background-color: transparent !important;
        color: #333 !important;
        font-size: 0.85rem !important;
        border: none !important;
        resize: none !important;
    }}
    /* 隱藏輸入框的標籤 */
    div[data-testid="stWidgetLabel"] {{ display: none !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部導航 ---
st.markdown(f"<h1>✨ MOA Diary</h1>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
if c1.button("上個月", use_container_width=True):
    st.session_state.curr_month -= 1
    if st.session_state.curr_month == 0:
        st.session_state.curr_month = 12
        st.session_state.curr_year -= 1
    st.rerun()
if c2.button("下個月", use_container_width=True):
    st.session_state.curr_month += 1
    if st.session_state.curr_month == 13:
        st.session_state.curr_month = 1
        st.session_state.curr_year += 1
    st.rerun()

st.markdown(f"<h2>{st.session_state.curr_year} / {st.session_state.curr_month:02d}</h2>", unsafe_allow_html=True)

# --- 5. 月曆主體 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_head = st.columns(7)
for i, d in enumerate(["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
    week_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; margin:0;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            
            with cols[i]:
                # 格子外層容器
                box_class = "day-box special-box" if is_special else "day-box"
                heart = "❤️" if is_special else ""
                
                # 顯示日期與標籤
                st.markdown(f"""
                    <div class="{box_class}">
                        <div style="color:{t['title']}; font-weight:bold;">{day:02d} {heart}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # 直接嵌入輸入框 (Text Area)
                # 這裡使用 st.text_area 讓你可以換行輸入
                current_text = st.session_state.notes.get(date_key, "")
                new_text = st.text_area(
                    label=date_key,
                    value=current_text,
                    key=f"input-{date_key}",
                    height=80
                )
                
                # 自動儲存機制：如果內容變動就存檔
                if new_text != current_text:
                    st.session_state.notes[date_key] = new_text
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)

                # 特別日子的底部標籤
                if is_special:
                    st.markdown(f"<div style='font-size:0.65rem; color:{t['title']}; text-align:right;'>{SPECIAL_DAYS[short_key]}</div>", unsafe_allow_html=True)

# 底部提醒
st.info("💡 內容會在你輸入完成並點擊格子外部或按 Ctrl+Enter 時自動儲存。")
