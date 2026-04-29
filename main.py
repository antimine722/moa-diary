# --- 5. 快速標籤列更新 (確保邏輯連動) ---
st.write("📍 點選下方格子後，再點標籤快速填入：")
tag_cols = st.columns(len(QUICK_TAGS) + 2)
for idx, tag in enumerate(QUICK_TAGS):
    with tag_cols[idx]:
        if st.button(tag, key=f"tag-{tag}", use_container_width=True):
            if st.session_state.active_date:
                # 取得當前輸入框的值 (直接從 session_state 拿最準)
                current_val = st.session_state.get(f"input-{st.session_state.active_date}", "")
                new_text = f"{current_val} ★{tag} ".strip()
                
                # 更新狀態與筆記
                st.session_state.notes[st.session_state.active_date] = new_text
                st.session_state[f"input-{st.session_state.active_date}"] = new_text
                
                with open("grid_notes.json", 'w', encoding='utf-8') as f:
                    json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)
                st.rerun()
            else:
                st.warning("請先點一下你想輸入的那一格唷！")

# --- 6. 月曆主體 (加入 click 追蹤邏輯) ---
def set_active(d_key):
    st.session_state.active_date = d_key

cal = calendar.monthcalendar(st.session_state.curr_year, st.session_state.curr_month)
week_names = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
cols_head = st.columns(7)
for i, d in enumerate(week_names):
    cols_head[i].markdown(f"<p style='text-align:center; color:{t['title']}; font-size:0.8rem; margin:10px 0;'><b>{d}</b></p>", unsafe_allow_html=True)

for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day != 0:
            date_key = f"{st.session_state.curr_year}-{st.session_state.curr_month:02d}-{day:02d}"
            short_key = f"{st.session_state.curr_month:02d}-{day:02d}"
            is_special = short_key in SPECIAL_DAYS
            
            with cols[i]:
                # 1. 上方日期條
                header_class = "date-header special-header" if is_special else "date-header"
                # 如果這格是選中狀態，加一個小標記
                is_active = st.session_state.active_date == date_key
                active_style = "border: 2px solid gold;" if is_active else ""
                
                heart = " ❤️" if is_special else ""
                st.markdown(f'<div class="{header_class}" style="{active_style}">{day:02d}{heart}</div>', unsafe_allow_html=True)
                
                # 2. 打字方框
                # 加入 on_change=set_active 確保一點擊或輸入就鎖定日期
                st.text_area(
                    label=date_key,
                    value=st.session_state.notes.get(date_key, ""),
                    key=f"input-{date_key}",
                    height=90,
                    label_visibility="collapsed",
                    on_change=set_active,
                    args=(date_key,)
                )
                
                # 同步資料到 notes (當內容變動時)
                input_val = st.session_state[f"input-{date_key}"]
                if input_val != st.session_state.notes.get(date_key, ""):
                    st.session_state.notes[date_key] = input_val
                    with open("grid_notes.json", 'w', encoding='utf-8') as f:
                        json.dump(st.session_state.notes, f, ensure_ascii=False, indent=4)

                if is_special:
                    st.markdown(f"<p style='font-size:0.7rem; color:#FF6B6B; text-align:center; margin:0;'>{SPECIAL_DAYS[short_key]}</p>", unsafe_allow_html=True)
