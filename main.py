import streamlit as st

# --- 1. 頁面配置 ---
st.set_page_config(page_title="MOA Diary", layout="wide")

# --- 2. 主題顏色設定 (可以自行修改) ---
THEMES = {
    "grey": {"bg": "#F5F5F5", "title": "#708090"},
    "orange": {"bg": "#FFF5EE", "title": "#E9967A"},
    "purple": {"bg": "#F8F4FF", "title": "#9370DB"},
}
theme_choice = st.sidebar.selectbox("切換主題", list(THEMES.keys()))
t = THEMES[theme_choice]

st.title("✨ MOA Diary (Mobile Fix)")

# --- 3. 核心 HTML/JS 代碼 ---
# 這裡我們用 HTML 表格強制鎖定 7 欄，不受 Streamlit 框架影響
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 10px; font-family: sans-serif; border-radius: 10px;">
    <div style="display: flex; gap: 5px; margin-bottom: 10px; overflow-x: auto; padding: 5px 0;">
        <button onclick="addTag('★生咖')" style="padding: 5px 10px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; white-space: nowrap;">★生咖</button>
        <button onclick="addTag('★演唱會')" style="padding: 5px 10px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; white-space: nowrap;">★演唱會</button>
        <button onclick="addTag('★應援')" style="padding: 5px 10px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; white-space: nowrap;">★應援</button>
        <button onclick="addTag('★回歸')" style="padding: 5px 10px; border-radius: 15px; border: 1px solid {t['title']}; background: white; color: {t['title']}; white-space: nowrap;">★回歸</button>
    </div>

    <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px;">
        <div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold;">M</div>
        <div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold;">T</div>
        <div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold;">W</div>
        <div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold;">T</div>
        <div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold;">F</div>
        <div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold;">S</div>
        <div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold;">S</div>
"""

# 自動生成 30 個格子 (以 2026/04 為例)
for i in range(1, 31):
    d_key = f"2026-04-{i:02d}"
    html_code += f"""
    <div id="cell-{d_key}" onclick="selectDay('{d_key}')" style="background: white; border: 1px solid #ddd; height: 80px; display: flex; flex-direction: column; border-radius: 4px;">
        <div style="font-size: 10px; padding: 2px; border-bottom: 1px solid #eee; background: #fafafa;">{i:02d}</div>
        <textarea id="input-{d_key}" oninput="saveData('{d_key}')" style="flex:1; border:none; outline:none; font-size:10px; padding:3px; resize:none; width:100%; box-sizing:border-box; background:transparent;"></textarea>
    </div>
    """

html_code += """
    </div>
</div>

<script>
    let selectedId = null;

    // 從本地讀取資料
    window.onload = function() {
        for (let i = 1; i <= 30; i++) {
            let key = `2026-04-${String(i).padStart(2, '0')}`;
            let saved = localStorage.getItem(key);
            if(saved) document.getElementById(`input-${key}`).value = saved;
        }
    };

    function selectDay(id) {
        if(selectedId) {
            document.getElementById(`cell-${selectedId}`).style.border = "1px solid #ddd";
            document.getElementById(`cell-${selectedId}`).style.boxShadow = "none";
        }
        selectedId = id;
        document.getElementById(`cell-${id}`).style.border = "2px solid gold";
        document.getElementById(`cell-${id}`).style.boxShadow = "inset 0 0 5px rgba(255,215,0,0.5)";
    }

    function saveData(id) {
        localStorage.setItem(id, document.getElementById(`input-${id}`).value);
    }

    function addTag(tag) {
        if(!selectedId) { alert("請先點選一個格子！"); return; }
        let el = document.getElementById(`input-${selectedId}`);
        el.value = (el.value + " " + tag).trim();
        saveData(selectedId);
    }
</script>
"""

# 使用 st.components 渲染，高度設為 800 確保手機看得到全貌
st.components.v1.html(html_code, height=800, scrolling=True)
