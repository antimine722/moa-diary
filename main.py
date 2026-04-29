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

# 預先讀取當前主題的 6 張圖片 Base64
current_imgs = [get_img_64(img_name) for img_name in t["imgs"]]

# --- 4. 月份狀態初始化 ---
if 'year' not in st.session_state: st.session_state.year = 2026
if 'month' not in st.session_state: st.session_state.month = 4

# --- 5. 核心 HTML/JS ---
# 在 Python 的 f-string 中，JS 的大括號必須寫成 {{ }} 才能正常顯示
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 12px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; border-radius: 15px; min-height: 900px;">
    
    <div style="position: sticky; top: 0; background: {t['bg']}; z-index: 100; padding-bottom: 10px; border-bottom: 2px solid {t['title']};">
        <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 15px;">
            <div style="display: flex; gap: 5px;">
                <img src="{current_imgs[0]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid white;">
                <img src="{current_imgs[1]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid white;">
                <img src="{current_imgs[2]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid white;">
            </div>
            <h1 style="margin: 0; color: {t['title']}; font-size: 1.8rem; letter-spacing: 1px;">MOA Diary</h1>
            <div style="display: flex; gap: 5px;">
                <img src="{current_imgs[3]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid white;">
                <img src="{current_imgs[4]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid white;">
                <img src="{current_imgs[5]}" style="width:40px; height:40px; border-radius:50%; object-fit:cover; border:2px solid white;">
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 300px; margin: 0 auto;">
            <button onclick="changeMonth(-1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:8px; padding:5px 20px; cursor:pointer; font-weight:bold; transition: 0.3s;"> < </button>
            <b id="currentDisplay" style="color:{t['title']}; font-size: 1.3rem;">{st.session_state.year} / {st.session_state.month:02d}</b>
            <button onclick="changeMonth(1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:8px; padding:5px 20px; cursor:pointer; font-weight:bold; transition: 0.3s;"> > </button>
        </div>
    </div>

    <div style="display: flex; gap: 8px; margin: 15px 0; overflow-x: auto; white-space: nowrap; padding: 5px; justify-content: center;">
        <button onclick="addTag('★生咖')" style="font-size:12px; border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer; opacity:0.9;">🎂 生咖</button>
        <button onclick="addTag('★演唱會')" style="font-size:12px; border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer; opacity:0.9;">🎤 演唱會</button>
        <button onclick="addTag('★應援')" style="font-size:12px; border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer; opacity:0.9;">🪄 應援</button>
        <button onclick="addTag('★回歸')" style="font-size:12px; border-radius:20px; border:none; background:{t['title']}; color:white; padding:6px 15px; cursor:pointer; opacity:0.9;">💿 回歸</button>
    </div>

    <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px;"></div>
</div>

<script>
    let curY = {st.session_state.year}, curM = {st.session_state.month}, selId = null;

    // 紀念日清單
    const ANNIVERSARIES = {{
        "03-04": "🎉 Debut Day",
        "08-22": "💙 MOA Day",
        "09-13": "🦊 YEONJUN",
        "12-05": "🐰 SOOBIN",
        "03-13": "🧸 BEOMGYU",
        "02-05": "🐿️ TAEHYUN",
        "08-14": "🐧 HUENINGKAI"
    }};

    function render(y, m) {{
        const grid = document.getElementById('calendar-grid');
        document.getElementById('currentDisplay').innerText = y + " / " + String(m).padStart(2, '0');
        grid.innerHTML = '';
        
        // 星期標題
        ['MON','TUE','WED','THU','FRI','SAT','SUN'].forEach(n => {{
            grid.innerHTML += `<div style="text-align:center; font-size:11px; color:{t['title']}; font-weight:bold; padding:5px;">${{n}}</div>`;
        }});

        const first = new Date(y, m-1, 1).getDay();
        const days = new Date(y, m, 0).getDate();
        // 修正星期位移 (JS 0=Sun, 1=Mon...)
        const offset = (first === 0) ? 6 : first - 1;

        for(let i=0; i<offset; i++) grid.innerHTML += '<div></div>';

        for(let i=1; i<=days; i++) {{
            let mmdd = String(m).padStart(2, '0') + "-" + String(i).padStart(2, '0');
            let k = y + "-" + mmdd;
            let note = localStorage.getItem(k) || "";
            
            // 紀念日檢查
            let anniHtml = ANNIVERSARIES[mmdd] ? 
                `<div style="background:{t['title']}; color:white; font-size:9px; padding:2px; text-align:center; font-weight:bold; border-radius:2px; margin-bottom:2px;">${{ANNIVERSARIES[mmdd]}}</div>` : "";

            let cell = document.createElement('div');
            cell.id = "c-" + k;
            cell.onclick = () => {{
                if(selId) {{
                    let prev = document.getElementById("c-" + selId);
                    if(prev) prev.style.boxShadow = "none";
                    if(prev) prev.style.border = "1px solid #eee";
                }}
                selId = k;
                cell.style.border = "2px solid {t['title']}";
                cell.style.boxShadow = "0 0 8px rgba(0,0,0,0.1)";
            }};
            
            cell.style = "background:white; border:1px solid #eee; height:110px; display:flex; flex-direction:column; border-radius:8px; overflow:hidden; transition: 0.2s; cursor:pointer;";
            
            cell.innerHTML = `
                <div style="font-size:10px; padding:4px; color:#999; display:flex; justify-content:space-between; align-items:center;">
                    <span>${{String(i).padStart(2, '0')}}</span>
                </div>
                <div style="padding: 0 4px;">${{anniHtml}}</div>
                <textarea id="i-${{k}}" oninput="localStorage.setItem('${{k}}', this.value)" 
                    style="flex:1; border:none; outline:none; font-size:11px; padding:5px; resize:none; background:transparent; width:100%; box-sizing:border-box; font-family:inherit;"
                    placeholder="...">$|{note}}</textarea>
            `.replace('$|{{note}}', note); // 避免直接注入導致的語法問題
            
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
        if(!selId) {{
            alert("請先點選一個日期格！");
            return;
        }}
        let el = document.getElementById("i-" + selId);
        let currentVal = el.value.trim();
        el.value = (currentVal + " " + tag).trim();
        localStorage.setItem(selId, el.value);
    }}

    render(curY, curM);
</script>
"""

st.components.v1.html(html_code, height=1000, scrolling=True)
