import streamlit as st
import base64
import os

# --- 1. 頁面配置 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

# --- 2. 圖片處理函式 ---
def get_img_64(name):
    if os.path.exists(name):
        with open(name, "rb") as f:
            return f"data:image/jpeg;base64,{base64.b64encode(f.read()).decode()}"
    return ""

# --- 3. 完整主題與圖片連動設定 ---
THEMES = {
    "orange": {
        "bg": "#FFF5EE", "title": "#E9967A",
        "imgs": [f"fox0{i}.jpg" for i in range(1, 7)]
    },
    "pink": {
        "bg": "#FFF0F5", "title": "#DB7093",
        "imgs": [f"bear0{i}.jpg" for i in range(1, 7)]
    },
    "grey": {
        "bg": "#F5F5F5", "title": "#708090",
        "imgs": [f"cat0{i}.jpg" for i in range(1, 7)]
    },
    "blue": {
        "bg": "#F0F8FF", "title": "#4682B4",
        "imgs": [f"dog0{i}.jpg" for i in range(1, 7)]
    },
    "purple": {
        "bg": "#F8F4FF", "title": "#9370DB",
        "imgs": [f"ang0{i}.jpg" for i in range(1, 7)]
    }
}

theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

current_imgs = [get_img_64(img_name) for img_name in t["imgs"]]

if 'year' not in st.session_state: st.session_state.year = 2026
if 'month' not in st.session_state: st.session_state.month = 4

# --- 5. 核心 HTML/JS ---
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 12px; font-family: sans-serif; border-radius: 15px; min-height: 850px;">
    
    <div style="position: sticky; top: 0; background: {t['bg']}; z-index: 100; padding-bottom: 10px; border-bottom: 2px solid {t['title']};">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 15px;">
            <div style="display: flex; gap: 5px;">
                <img src="{current_imgs[0]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[1]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[2]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;">
            </div>
            <h1 style="margin: 0; color: {t['title']}; font-size: 1.8rem;">MOA Diary</h1>
            <div style="display: flex; gap: 5px;">
                <img src="{current_imgs[3]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[4]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[5]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover;">
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 300px; margin: 0 auto;">
            <button onclick="changeMonth(-1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:8px; padding:5px 20px; cursor:pointer;"> < </button>
            <b id="currentDisplay" style="color:{t['title']}; font-size: 1.3rem;">{st.session_state.year} / {st.session_state.month:02d}</b>
            <button onclick="changeMonth(1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:8px; padding:5px 20px; cursor:pointer;"> > </button>
        </div>
    </div>

    <div style="display: flex; gap: 8px; margin: 15px 0; overflow-x: auto; justify-content: center;">
        <button onclick="addTag('★生咖')" style="border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer;">🎂 生咖</button>
        <button onclick="addTag('★演唱會')" style="border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer;">🎤 演唱會</button>
        <button onclick="addTag('★應援')" style="border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer;">🪄 應援</button>
        <button onclick="addTag('★回歸')" style="border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer;">💿 回歸</button>
    </div>

    <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px;"></div>
</div>

<script>
    let curY = {st.session_state.year};
    let curM = {st.session_state.month};
    let selId = null;

    const ANNIVERSARIES = {{
        "03-04": "🎉 Debut Day", "08-22": "💙 MOA Day", "09-13": "🦊 YEONJUN",
        "12-05": "🐰 SOOBIN", "03-13": "🧸 BEOMGYU", "02-05": "🐿️ TAEHYUN", "08-14": "🐧 HUENINGKAI"
    }};

    function render(y, m) {{
        const grid = document.getElementById('calendar-grid');
        const display = document.getElementById('currentDisplay');
        if(!grid || !display) return;

        display.innerText = y + " / " + String(m).padStart(2, '0');
        grid.innerHTML = '';
        
        ['MON','TUE','WED','THU','FRI','SAT','SUN'].forEach(n => {{
            const wk = document.createElement('div');
            wk.style = "text-align:center; font-size:11px; color:{t['title']}; font-weight:bold; padding:5px;";
            wk.innerText = n;
            grid.appendChild(wk);
        }});

        const firstDay = new Date(y, m-1, 1).getDay();
        const daysInMonth = new Date(y, m, 0).getDate();
        const offset = (firstDay === 0) ? 6 : firstDay - 1;

        for(let i=0; i<offset; i++) {{
            grid.appendChild(document.createElement('div'));
        }}

        for(let i=1; i<=daysInMonth; i++) {{
            const mmdd = String(m).padStart(2, '0') + "-" + String(i).padStart(2, '0');
            const k = y + "-" + mmdd;
            const note = localStorage.getItem(k) || "";
            
            const cell = document.createElement('div');
            cell.id = "c-" + k;
            cell.style = "background:white; border:2.5px solid {t['title']}; height:110px; display:flex; flex-direction:column; border-radius:12px; overflow:hidden;";
            
            let anniHtml = "";
            if(ANNIVERSARIES[mmdd]) {{
                anniHtml = '<div style="background:{t['title']}; color:white; font-size:9px; padding:2px; text-align:center; font-weight:bold; border-radius:0px; margin-bottom:2px;">' + ANNIVERSARIES[mmdd] + '</div>';
            }}

            cell.innerHTML = 
                '<div style="font-size:10px; padding:4px; color:{t['title']}; font-weight:bold;">' + String(i).padStart(2, '0') + '</div>' +
                '<div style="padding: 0 4px;">' + anniHtml + '</div>' +
                '<textarea id="i-' + k + '" style="flex:1; border:none; outline:none; font-size:11px; padding:5px; resize:none; background:transparent; width:100%; box-sizing:border-box; font-family:inherit;">' + note + '</textarea>';

            cell.onclick = function() {{
                selId = k;
            }};

            const area = cell.querySelector('textarea');
            area.oninput = function() {{
                localStorage.setItem(k, this.value);
            }};
            area.onfocus = function() {{
                selId = k;
            }};

            grid.appendChild(cell);
        }}
    }}

    function changeMonth(s) {{
        curM += s;
        if(curM > 12) {{ curM = 1; curY++; }} 
        else if(curM < 1) {{ curM = 12; curY--; }}
        render(curY, curM);
    }}

    function addTag(tag) {{
        if(!selId) {{ alert("請先點選日期格！"); return; }}
        const el = document.getElementById("i-" + selId);
        if(el) {{
            el.value = (el.value + " " + tag).trim();
            localStorage.setItem(selId, el.value);
        }}
    }}

    render(curY, curM);
</script>
"""

st.components.v1.html(html_code, height=950, scrolling=True)
