import streamlit as st
import base64
import os

# --- 1. 頁面配置 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

# --- 2. 圖片處理函式 (轉 Base64) ---
def get_image_base64(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = f.read()
        return f"data:image/jpeg;base64,{base64.b64encode(data).decode()}"
    return "" # 若檔案不存在則回傳空字串

# 讀取你的 6 張圖片
img_files = ["ang01.jpg", "ang02.jpg", "ang03.jpg", "ang04.jpg", "ang05.jpg", "ang06.jpg"]
img_data = [get_image_base64(f) for f in img_files]

# --- 3. 主題與月份狀態 ---
THEMES = {
    "purple": {"bg": "#F8F4FF", "title": "#9370DB"},
    "pink": {"bg": "#FFF0F5", "title": "#DB7093"},
    "orange": {"bg": "#FFF5EE", "title": "#E9967A"},
    "blue": {"bg": "#F0F8FF", "title": "#4682B4"},
    "grey": {"bg": "#F5F5F5", "title": "#708090"}
}

theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

# 初始化狀態
if 'year' not in st.session_state: st.session_state.year = 2026
if 'month' not in st.session_state: st.session_state.month = 4

# --- 4. 嵌入式 HTML/JS ---
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 8px; font-family: sans-serif; border-radius: 10px;">
    
    <div style="position: sticky; top: 0; background: {t['bg']}; z-index: 100; padding-bottom: 10px; border-bottom: 1px solid {t['title']};">
        
        <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 10px;">
            <div style="display: flex; gap: 3px;">
                <img src="{img_data[0]}" style="width:28px; height:28px; border-radius:50%; object-fit:cover;">
                <img src="{img_data[1]}" style="width:28px; height:28px; border-radius:50%; object-fit:cover;">
                <img src="{img_data[2]}" style="width:28px; height:28px; border-radius:50%; object-fit:cover;">
            </div>
            
            <h1 style="margin: 0; color: {t['title']}; font-size: 1.3rem; white-space: nowrap;">MOA Diary</h1>
            
            <div style="display: flex; gap: 3px;">
                <img src="{img_data[3]}" style="width:28px; height:28px; border-radius:50%; object-fit:cover;">
                <img src="{img_data[4]}" style="width:28px; height:28px; border-radius:50%; object-fit:cover;">
                <img src="{img_data[5]}" style="width:28px; height:28px; border-radius:50%; object-fit:cover;">
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 280px; margin: 0 auto;">
            <button onclick="changeMonth(-1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:4px; padding:2px 12px; cursor:pointer;"> < </button>
            <b id="currentDisplay" style="color:{t['title']}; font-size: 1rem;">{st.session_state.year} / {st.session_state.month:02d}</b>
            <button onclick="changeMonth(1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:4px; padding:2px 12px; cursor:pointer;"> > </button>
        </div>
    </div>

    <div style="display: flex; gap: 5px; margin: 10px 0; overflow-x: auto; white-space: nowrap; padding-bottom: 5px;">
        <button onclick="addTag('★生咖')" style="font-size:12px; border-radius:15px; border:1px solid {t['title']}; background:white; color:{t['title']}; padding:4px 10px; cursor:pointer;">生咖</button>
        <button onclick="addTag('★演唱會')" style="font-size:12px; border-radius:15px; border:1px solid {t['title']}; background:white; color:{t['title']}; padding:4px 10px; cursor:pointer;">演唱會</button>
        <button onclick="addTag('★應援活動')" style="font-size:12px; border-radius:15px; border:1px solid {t['title']}; background:white; color:{t['title']}; padding:4px 10px; cursor:pointer;">應援活動</button>
        <button onclick="addTag('★回歸')" style="font-size:12px; border-radius:15px; border:1px solid {t['title']}; background:white; color:{t['title']}; padding:4px 10px; cursor:pointer;">回歸</button>
    </div>

    <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px;"></div>
</div>

<script>
    let curY = {st.session_state.year}, curM = {st.session_state.month}, selId = null;

    function render(y, m) {{
        const grid = document.getElementById('calendar-grid');
        document.getElementById('currentDisplay').innerText = `${{y}} / ${{String(m).padStart(2, '0')}}`;
        grid.innerHTML = '';
        
        ['MON','TUE','WED','THU','FRI','SAT','SUN'].forEach(n => {{
            grid.innerHTML += `<div style="text-align:center; font-size:9px; color:{t['title']}; font-weight:bold; margin-bottom:5px;">${{n}}</div>`;
        }});

        const first = new Date(y, m-1, 1).getDay();
        const days = new Date(y, m, 0).getDate();
        const offset = first === 0 ? 6 : first - 1;

        for(let i=0; i<offset; i++) grid.innerHTML += '<div style="background:rgba(255,255,255,0.3); border:0.5px solid #eee; height:80px;"></div>';

        for(let i=1; i<=days; i++) {{
            let k = `${{y}}-${{String(m).padStart(2, '0')}}-${{String(i).padStart(2, '0')}}`;
            let note = localStorage.getItem(k) || "";
            let cell = document.createElement('div');
            cell.id = `c-${{k}}`;
            cell.onclick = () => {{
                if(selId) {{
                    let prev = document.getElementById(`c-${{selId}}`);
                    if(prev) prev.style.border="1px solid #ddd";
                }}
                selId = k;
                cell.style.border=`2px solid {t['title']}`;
            }};
            cell.style = "background:white; border:1px solid #ddd; height:80px; display:flex; flex-direction:column; border-radius:4px; overflow:hidden;";
            cell.innerHTML = `
                <div style="font-size:10px; padding:2px; color:{t['title']}; border-bottom:1px solid #eee;">${{String(i).padStart(2, '0')}}</div>
                <textarea id="i-${{k}}" oninput="localStorage.setItem('${{k}}', this.value)" style="flex:1; border:none; outline:none; font-size:10px; padding:3px; resize:none; background:transparent; width:100%; box-sizing:border-box;">${{note}}</textarea>
            `;
            grid.appendChild(cell);
        }}
    }}

    function changeMonth(s) {{
        curM += s;
        if(curM>12) {{ curM=1; curY++; }} else if(curM<1) {{ curM=12; curY--; }}
        render(curY, curM);
    }}

    function addTag(t) {{
        if(!selId) return alert("請先選一個日期格子！");
        let el = document.getElementById(`i-${{selId}}`);
        el.value = (el.value + " " + t).trim();
        localStorage.setItem(selId, el.value);
    }}

    render(curY, curM);
</script>
"""

st.components.v1.html(html_code, height=950, scrolling=True)
