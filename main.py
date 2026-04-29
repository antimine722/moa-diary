import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

# --- 2. 主題顏色與狀態 ---
THEMES = {
    "grey": {"bg": "#F5F5F5", "title": "#708090"},
    "orange": {"bg": "#FFF5EE", "title": "#E9967A"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB"},
}
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

# --- 3. 嵌入式 HTML/JS ---
# 我們將導覽按鈕直接寫在 HTML 裡，解決手機版排版消失的問題
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 10px; font-family: 'Microsoft JhengHei', sans-serif; border-radius: 10px;">
    
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
        <button onclick="changeMonth(-1)" style="padding: 5px 15px; border-radius: 5px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-weight: bold;"> < </button>
        <h2 id="currentDisplay" style="margin: 0; color: {t['title']}; font-size: 1.2rem;">2026 / 04</h2>
        <button onclick="changeMonth(1)" style="padding: 5px 15px; border-radius: 5px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-weight: bold;"> > </button>
    </div>

    <div style="display: flex; gap: 5px; margin-bottom: 15px; overflow-x: auto; white-space: nowrap; padding-bottom: 5px;">
        <button onclick="addTag('★生咖')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px;">★生咖</button>
        <button onclick="addTag('★演唱會')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px;">★演唱會</button>
        <button onclick="addTag('★應援')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px;">★應援</button>
        <button onclick="addTag('★回歸')" style="padding: 6px 12px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; font-size: 13px;">★回歸</button>
    </div>

    <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px;">
        </div>
</div>

<script>
    let currentYear = 2026;
    let currentMonth = 4;
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
        
        // 修正 Date.getDay() 的星期排版 (將週日 0 移至最後)
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

    // 初始化
    renderCalendar(currentYear, currentMonth);
</script>
"""

# 渲染到畫面上
st.components.v1.html(html_code, height=900, scrolling=True)
