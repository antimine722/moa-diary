# --- 5. 核心 HTML/JS ---
html_code = f"""
<div id="moa-app" style="background: {t['bg']}; padding: 8px; font-family: sans-serif; border-radius: 10px;">
    
    <div style="position: sticky; top: 0; background: {t['bg']}; z-index: 100; padding-bottom: 10px; border-bottom: 1px solid {t['title']};">
        <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 10px;">
            <div style="display: flex; gap: 3px;">
                <img src="{current_imgs[0]}" style="width:32px; height:32px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[1]}" style="width:32px; height:32px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[2]}" style="width:32px; height:32px; border-radius:50%; object-fit:cover;">
            </div>
            <h1 style="margin: 0; color: {t['title']}; font-size: 1.4rem; white-space: nowrap;">MOA Diary</h1>
            <div style="display: flex; gap: 3px;">
                <img src="{current_imgs[3]}" style="width:32px; height:32px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[4]}" style="width:32px; height:32px; border-radius:50%; object-fit:cover;">
                <img src="{current_imgs[5]}" style="width:32px; height:32px; border-radius:50%; object-fit:cover;">
            </div>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: center; max-width: 260px; margin: 0 auto;">
            <button onclick="changeMonth(-1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:5px; padding:3px 15px; cursor:pointer; font-weight:bold;"> < </button>
            <b id="currentDisplay" style="color:{t['title']}; font-size: 1.1rem;">{st.session_state.year} / {st.session_state.month:02d}</b>
            <button onclick="changeMonth(1)" style="border:1px solid {t['title']}; background:white; color:{t['title']}; border-radius:5px; padding:3px 15px; cursor:pointer; font-weight:bold;"> > </button>
        </div>
    </div>

    <div style="display: flex; gap: 5px; margin: 12px 0; overflow-x: auto; white-space: nowrap; padding-bottom: 5px; justify-content: center;">
        <button onclick="addTag('★生咖')" style="font-size:12px; border-radius:4px; border:none; background:{t['title']}; color:white; padding:5px 12px; cursor:pointer; opacity:0.8;">生咖</button>
        <button onclick="addTag('★演唱會')" style="font-size:12px; border-radius:4px; border:none; background:{t['title']}; color:white; padding:5px 12px; cursor:pointer; opacity:0.8;">演唱會</button>
        <button onclick="addTag('★應援')" style="font-size:12px; border-radius:4px; border:none; background:{t['title']}; color:white; padding:5px 12px; cursor:pointer; opacity:0.8;">應援</button>
        <button onclick="addTag('★回歸')" style="font-size:12px; border-radius:4px; border:none; background:{t['title']}; color:white; padding:5px 12px; cursor:pointer; opacity:0.8;">回歸</button>
    </div>

    <div id="calendar-grid" style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 3px;"></div>
</div>

<script>
    let curY = {st.session_state.year}, curM = {st.session_state.month}, selId = null;

    // --- 紀念日設定清單 ---
    const ANNIVERSARIES = {{
        "03-04": "🎂 Debut Day",
        "08-22": "💙 MOA Day",
        "09-13": "🦊 YEONJUN Day",
        "12-05": "🐰 SOOBIN Day",
        "03-13": "🧸 BEOMGYU Day",
        "02-05": "🐿️ TAEHYUN Day",
        "08-14": "🐧 HUENINGKAI Day"
    }};

    function render(y, m) {{
        const grid = document.getElementById('calendar-grid');
        document.getElementById('currentDisplay').innerText = `${{y}} / ${{String(m).padStart(2, '0')}}`;
        grid.innerHTML = '';
        
        ['MON','TUE','WED','THU','FRI','SAT','SUN'].forEach(n => {{
            grid.innerHTML += `<div style="text-align:center; font-size:10px; color:{t['title']}; font-weight:bold; margin-bottom:5px;">${{n}}</div>`;
        }});

        const first = new Date(y, m-1, 1).getDay();
        const days = new Date(y, m, 0).getDate();
        const offset = first === 0 ? 6 : first - 1;

        for(let i=0; i<offset; i++) grid.innerHTML += '<div></div>';

        for(let i=1; i<=days; i++) {{
            let mmdd = `${{String(m).padStart(2, '0')}}-${{String(i).padStart(2, '0')}}`;
            let k = `${{y}}-${{mmdd}}`;
            let note = localStorage.getItem(k) || "";
            
            // 檢查是否有紀念日
            let anniTag = ANNIVERSARIES[mmdd] ? 
                `<div style="background:{t['title']}; color:white; font-size:8px; padding:1px 4px; text-align:center; font-weight:bold;">${{ANNIVERSARIES[mmdd]}}</div>` : "";

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
            
            cell.style = "background:white; border:1px solid #ddd; height:95px; display:flex; flex-direction:column; border-radius:4px; overflow:hidden; transition: 0.2s;";
            
            cell.innerHTML = `
                ${{anniTag}}
                <div style="font-size:10px; padding:2px; color:{t['title']}; border-bottom:1px solid #eee; background:#fafafa; display:flex; justify-content:space-between;">
                    <span>${{String(i).padStart(2, '0')}}</span>
                </div>
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
        if(!selId) return alert("請先點選日期！");
        let el = document.getElementById(`i-${{selId}}`);
        el.value = (el.value + " " + t).trim();
        localStorage.setItem(selId, el.value);
    }}

    render(curY, curM);
</script>
"""
