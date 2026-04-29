import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

# --- 2. 完整主題設定 ---
THEMES = {
    "grey": {"bg": "#F5F5F5", "title": "#708090"},
    "orange": {"bg": "#FFF5EE", "title": "#E9967A"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB"},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093"},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4"}
}

theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

# 初始化年份與月份狀態
if 'year' not in st.session_state: st.session_state.year = 2026
if 'month' not in st.session_state: st.session_state.month = 4

# --- 3. 頂部原生控制區 ---
st.markdown(f"<h1 style='text-align: center; color: {t['title']};'>✨ MOA Diary</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅️ 上個月"):
        st.session_state.month -= 1
        if st.session_state.month < 1:
            st.session_state.month = 12
            st.session_state.year -= 1
        st.rerun()

with col2:
    st.markdown(f"<h2 style='text-align: center; color: {t['title']}; margin: 0;'>{st.session_state.year} / {st.session_state.month:02d}</h2>", unsafe_allow_html=True)

with col3:
    if st.button("下個月 ➡️"):
        st.session_state.month += 1
        if st.session_state.month > 12:
            st.session_state.month = 1
            st.session_state.year += 1
        st.rerun()

# --- 4. 嵌入式 HTML/JS (鎖定手機 7 欄排版) ---
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 10px; font-family: sans-serif; border-radius: 10px;">
    
    <div style="display: flex; gap: 5px; margin-bottom: 15px; overflow-x: auto; white-space: nowrap; padding-bottom: 5px;">
        <button onclick="addTag('★生咖')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']};">★生咖</button>
        <button onclick="addTag('★演唱會')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']};">★演唱會</button>
        <button onclick="addTag('★應援')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']};">★應援</button>
        <button onclick="addTag('★回歸')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']};">★回歸</button>
    </div>

    <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px;"></div>
</div>

<script>
    const currentYear = {st.session_state.year};
    const currentMonth = {st.session_state.month};
    let selectedId = null;

    function renderCalendar(year, month) {{
        const grid = document.getElementById('calendar-grid');
        grid.innerHTML = '';
        
        const dayNames = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
        dayNames.forEach(name => {{
            grid.innerHTML += `<div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold; padding-bottom:5px;">${{name}}</div>`;
        }});

        const firstDay = new Date(year, month - 1, 1).getDay();
        const daysInMonth = new Date(year, month, 0).getDate();
        const offset = firstDay === 0 ? 6 : firstDay - 1;

        for (let i = 0; i < offset; i++) grid.innerHTML += '<div></div>';

        for (let i = 1; i <= daysInMonth; i++) {{
            let dKey = `${{year}}-${{String(month).padStart(2, '0')}}-${{String(i).padStart(2, '0')}}`;
            let savedNote = localStorage.getItem(dKey) || "";
            
            let cell = document.createElement('div');
            cell.id = `cell-${{dKey}}`;
            cell.onclick = () => selectDay(dKey);
            cell.style = "background:white; border:1px solid #ddd; height:85px; display:flex; flex-direction:column; border-radius:4px; overflow:hidden;";
            
            cell.innerHTML = `
                <div style="font-size:10px; padding:2px; background:#fafafa; border-bottom:1px solid #eee;">${{i}}</div>
                <textarea id="input-${{dKey}}" oninput="saveData('${{dKey}}')" style="flex:1; border:none; outline:none; font-size:10px; padding:3px; resize:none; width:100%; box-sizing:border-box; background:transparent;">${{savedNote}}</textarea>
            `;
            grid.appendChild(cell);
        }}
    }}

    function selectDay(id) {{
        if(selectedId) {{
            let prevCell = document.getElementById(`cell-${{selectedId}}`);
            if(prevCell) prevCell.style.border = "1px solid #ddd";
        }}
        selectedId = id;
        document.getElementById(`cell-${{id}}`).style.border = "2px solid {t['title']}";
    }}

    function saveData(id) {{
        localStorage.setItem(id, document.getElementById(`input-${{id}}`).value);
    }}

    function addTag(tag) {{
        if(!selectedId) {{ alert("請先點選一個格子！"); return; }}
        let el = document.getElementById(`input-${{selectedId}}`);
        el.value = (el.value + " " + tag).trim();
        saveData(selectedId);
    }}

    renderCalendar(currentYear, currentMonth);
</script>
"""

st.components.v1.html(html_code, height=900, scrolling=True)
