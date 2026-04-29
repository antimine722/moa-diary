import streamlit as st
import calendar
import json
import os

# --- 1. 配置與核心資料 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

SPECIAL_DAYS = {"03-04": "Debut", "08-22": "MOA", "09-13": "YEONJUN", "12-05": "SOOBIN", "03-13": "BEOMGYU", "02-05": "TAEHYUN", "08-14": "HUENINGKAI"}
QUICK_TAGS = ["生咖", "演唱會", "應援活動", "回歸"]
THEMES = {
    "orange": {"bg": "#FFF5EE", "title": "#E9967A", "cell": "#FFF"},
    "grey": {"bg": "#F5F5F5", "title": "#708090", "cell": "#FFF"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB", "cell": "#FFF"},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4", "cell": "#FFF"},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093", "cell": "#FFF"}
}

# --- 2. 狀態管理 ---
if 'notes' not in st.session_state:
    if os.path.exists("grid_notes.json"):
        with open("grid_notes.json", 'r', encoding='utf-8') as f: st.session_state.notes = json.load(f)
    else: st.session_state.notes = {}

for k in ['curr_year', 'curr_month', 'sel_date']:
    if k not in st.session_state: st.session_state[k] = (2026 if k=='curr_year' else (4 if k=='curr_month' else None))

# --- 3. 強制排版 CSS ---
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.markdown(f"""
    <style>
    .stApp {{ background-color: {t['bg']}; }}
    /* 強制橫向滾動容器，確保格子不被壓縮 */
    .cal-container {{ overflow-x: auto; width: 100%; }}
    .cal-table {{ border-collapse: collapse; width: 100%; min-width: 350px; table-layout: fixed; }}
    .cal-table th, .cal-table td {{ border: 1px solid {t['title']}; padding: 2px; text-align: center; background: {t['cell']}; vertical-align: top; }}
    .cal-table th {{ background: {t['title']}; color: white; font-size: 10px; }}
    .day-num {{ font-weight: bold; font-size: 12px; color: {t['title']}; margin: 2px; }}
    .selected-cell {{ background-color: #FFF9C4 !important; border: 2px solid gold !important; }}
    .special-text {{ color: red; font-size: 8px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. 頂部控制區 ---
st.title("✨ MOA Diary")

# 標籤列
tag_cols = st.columns(len(QUICK_TAGS))
for i, tag in enumerate(QUICK_TAGS):
    if tag_cols[i].button(f"★{tag}", use_container_width=True):
        if st.session_state.sel_date:
            d = st.session_state.sel_date
            st.session_state.notes[d] = f"{st.session_state.notes.get(d, '')} ★{tag}".strip()
            with open("grid_notes.json", 'w', encoding='utf-8') as f: json.dump(st.session_state.notes, f, ensure_ascii=False)
            st.rerun()

# --- 5. 手機穩定版月曆渲染 ---
cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# 建立 HTML 表格
html_code = f'<div class="cal-container"><table class="cal-table"><thead><tr>'
for d in days: html_code += f'<th>{d}</th>'
html_code += '</tr></thead><tbody>'

for week in cal:
    html_code += '<tr>'
    for day in week:
        if day == 0:
            html_code += '<td></td>'
        else:
            d_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            s_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_sel = st.session_state.sel_date == d_key
            sel_class = "selected-cell" if is_sel else ""
            note = st.session_state.notes.get(d_key, "")
            spec = f"<div class='special-text'>{SPECIAL_DAYS[s_key]}</div>" if s_key in SPECIAL_DAYS else ""
            
            html_code += f'<td class="{sel_class}"><div class="day-num">{day}</div><div style="font-size:10px; height:40px; overflow:hidden;">{note}</div>{spec}</td>'
    html_code += '</tr>'
html_code += '</tbody></table></div>'

st.markdown(html_code, unsafe_allow_html=True)

# --- 6. 輸入編輯區 ---
st.markdown("---")
if st.session_state.sel_date:
    st.write(f"正在編輯: {st.session_state.sel_date}")
    new_txt = st.text_area("內容輸入", value=st.session_state.notes.get(st.session_state.sel_date, ""), key="edit_area")
    if st.button("儲存內容"):
        st.session_state.notes[st.session_state.sel_date] = new_txt
        with open("grid_notes.json", 'w', encoding='utf-8') as f: json.dump(st.session_state.notes, f, ensure_ascii=False)
        st.rerun()

# 選擇日期按鈕區 (因為 HTML 無法直接觸發 Streamlit 事件，我們用一個選擇器)
all_days = [f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{d:02d}" for week in cal for d in week if d != 0]
st.session_state.sel_date = st.selectbox("請先在此選擇日期，再使用上方標籤或下方輸入框：", ["請選擇"] + all_days)
