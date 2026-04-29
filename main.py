import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

# --- 2. 完整主題設定 (包含連動圖片) ---
# 我為每個主題選定了對應的裝飾動物網址 (左3張，右3張)
THEMES = {
    "orange": {
        "bg": "#FFF5EE", "title": "#E9967A",
        "imgs_l": ["https://img.icons8.com/puffy/48/fox.png", "https://img.icons8.com/puffy/48/null/fox.png", "https://img.icons8.com/puffy/48/fox.png"],
        "imgs_r": ["https://img.icons8.com/puffy/48/fox.png", "https://img.icons8.com/puffy/48/null/fox.png", "https://img.icons8.com/puffy/48/fox.png"]
    },
    "grey": {
        "bg": "#F5F5F5", "title": "#708090",
        "imgs_l": ["https://img.icons8.com/puffy/48/wolf.png", "https://img.icons8.com/puffy/48/null/wolf.png", "https://img.icons8.com/puffy/48/wolf.png"],
        "imgs_r": ["https://img.icons8.com/puffy/48/wolf.png", "https://img.icons8.com/puffy/48/null/wolf.png", "https://img.icons8.com/puffy/48/wolf.png"]
    },
    "purple": {
        "bg": "#F8F4FF", "title": "#9370DB",
        "imgs_l": ["https://img.icons8.com/puffy/48/cat.png", "https://img.icons8.com/puffy/48/null/cat.png", "https://img.icons8.com/puffy/48/cat.png"],
        "imgs_r": ["https://img.icons8.com/puffy/48/cat.png", "https://img.icons8.com/puffy/48/null/cat.png", "https://img.icons8.com/puffy/48/cat.png"]
    },
    "pink": {
        "bg": "#FFF0F5", "title": "#DB7093",
        "imgs_l": ["https://img.icons8.com/puffy/48/rabbit.png", "https://img.icons8.com/puffy/48/null/rabbit.png", "https://img.icons8.com/puffy/48/rabbit.png"],
        "imgs_r": ["https://img.icons8.com/puffy/48/rabbit.png", "https://img.icons8.com/puffy/48/null/rabbit.png", "https://img.icons8.com/puffy/48/rabbit.png"]
    },
    "blue": {
        "bg": "#F0F8FF", "title": "#4682B4",
        "imgs_l": ["https://img.icons8.com/puffy/48/dog.png", "https://img.icons8.com/puffy/48/null/dog.png", "https://img.icons8.com/puffy/48/dog.png"],
        "imgs_r": ["https://img.icons8.com/puffy/48/dog.png", "https://img.icons8.com/puffy/48/null/dog.png", "https://img.icons8.com/puffy/48/dog.png"]
    }
}

theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

# 初始化年份與月份狀態
if 'year' not in st.session_state: st.session_state.year = 2026
if 'month' not in st.session_state: st.session_state.month = 4

# --- 3. 頂部原生控制區 (將其隱藏，因為我們要整合進 HTML 裡固定住) ---
# st.markdown(f"<h1 style='text-align: center; color: {t['title']};'>✨ MOA Diary</h1>", unsafe_allow_html=True)
# (移除原生的 col1, col2, col3 翻頁按鈕，因為我們要整合進 HTML)

# --- 4. 嵌入式 HTML/JS (整合圖片、固定標題、翻頁按鈕與 7 欄排版) ---
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 10px; font-family: sans-serif; border-radius: 10px;">
    
    <div style="position: sticky; top: 0; background: {t['bg']}; padding: 10px 0; z-index: 100; border-bottom: 2px solid {t['title']}; margin-bottom: 15px;">
        
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 10px;">
            <div style="display: flex; gap: 5px;">
                <img src="{t['imgs_l'][0]}" width="30" height="30">
                <img src="{t['imgs_l'][1]}" width="30" height="30">
                <img src="{t['imgs_l'][2]}" width="30" height="30">
            </div>
            
            <h1 style="margin: 0; color: {t['title']}; font-size: 1.5rem; white-space: nowrap;">✨ MOA Diary</h1>
            
            <div style="display: flex; gap: 5px;">
                <img src="{t['imgs_r'][0]}" width="30" height="30">
                <img src="{t['imgs_r'][1]}" width="30" height="30">
                <img src="{t['imgs_r'][2]}" width="30" height="30">
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; width: 80%; margin: 0 auto;">
            <button onclick="changeMonth(-1)" style="padding: 5px 12px; border-radius: 5px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-weight: bold; cursor: pointer;">⬅️</button>
            <h2 id="currentDisplay" style="margin: 0; color: {t['title']}; font-size: 1.1rem;">{st.session_state.year} / {st.session_state.month:02d}</h2>
            <button onclick="changeMonth(1)" style="padding: 5px 12px; border-radius: 5px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-weight: bold; cursor: pointer;">➡️</button>
        </div>
    </div>

    <div style="display: flex; gap: 5px; margin-bottom: 15px; overflow-x: auto; white-space: nowrap; padding-bottom: 5px;">
        <button onclick="addTag('★生咖')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px; cursor: pointer;">★生咖</button>
        <button onclick="addTag('★演唱會')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px; cursor: pointer;">★演唱會</button>
        <button onclick="addTag('★應援')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px; cursor: pointer;">★應援</button>
        <button onclick="addTag('★回歸')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px; cursor: pointer;">★回歸</button>
    </div>

    <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px;"></div>
</div>

<script>
    // 從 Python 傳入初始狀態
    let currentYear = {st.session_state.year};
    let currentMonth = {st.session_state.month};
    let selectedId = null;

    function renderCalendar(year, month) {{
        const grid = document.getElementById('calendar-grid');
        const display = document.getElementById('currentDisplay');
        display.innerText = `${{year}} / ${{String(month).padStart(2, '0')}}`;
        
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
            cell.style = "background:white; border:1px solid #ddd; height:85px; display:flex; flex-direction:column; border-radius:4px; overflow:hidden; cursor: pointer;";
            
            cell.innerHTML = `
                <div style="font-size:10px; padding:2px; background:#fafafa; border-bottom:1px solid #eee;">${{i}}</div>
                <textarea id="input-${{dKey}}" oninput="saveData('${{dKey}}')" style="flex:1; border:none; outline:none; font-size:10px; padding:3px; resize:none; width:100%; box-sizing:border-box; background:transparent;">${{savedNote}}</textarea>
            `;
            grid.appendChild(cell);
        }}
    }}

    // [核心邏輯] JS 翻頁，不觸發 Python Rerun
    function changeMonth(step) {{
        currentMonth += step;
        if (currentMonth > 12) {{ currentMonth = 1; currentYear++; }}
        if (currentMonth < 1) {{ currentMonth = 12; currentYear--; }}
        renderCalendar(currentYear, currentMonth);
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

    // 初始化渲染
    renderCalendar(currentYear, currentMonth);
</script>
"""

# 將 scrolling 設為 false，因為我們希望在組件內部處理捲動
st.components.v1.html(html_code, height=1000, scrolling=True)
