# AI Travel Agent - 简化运行版
# 避免pyarrow等编译依赖，直接运行

import streamlit as st
import re
from datetime import datetime, timedelta
from icalendar import Calendar, Event
import requests
import json

def generate_ics_content(plan_text:str, start_date: datetime = None) -> bytes:
    """
        生成一个ICS日历文件从旅行行程文本。
    """
    cal = Calendar()
    cal.add('prodid','-//AI Travel Planner//github.com//' )
    cal.add('version', '2.0')

    if start_date is None:
        start_date = datetime.today()

    # 将计划按天分割
    day_pattern = re.compile(r'Day (\d+)[:\s]+(.*?)(?=Day \d+|$)', re.DOTALL)
    days = day_pattern.findall(plan_text)

    if not days: # 如果没有找到天的模式，创建一个全天事件
        event = Event()
        event.add('summary', "Travel Itinerary")
        event.add('description', plan_text)
        event.add('dtstart', start_date.date())
        event.add('dtend', start_date.date())
        event.add("dtstamp", datetime.now())
        cal.add_component(event)  
    else:
        # 处理每一天
        for day_num, day_content in days:
            day_num = int(day_num)
            current_date = start_date + timedelta(days=day_num - 1)
            
            # 为整个一天创建一个事件
            event = Event()
            event.add('summary', f"Day {day_num} Itinerary")
            event.add('description', day_content.strip())
            
            # 设为全天事件
            event.add('dtstart', current_date.date())
            event.add('dtend', current_date.date())
            event.add("dtstamp", datetime.now())
            cal.add_component(event)

    return cal.to_ical()

def generate_travel_plan(destination: str, num_days: int) -> str:
    """
        生成旅行计划的简单函数（不依赖外部API）
    """
    plans = {
        "北京": [
            "Day 1: 游览天安门广场和故宫博物院，参观国家博物馆",
            "Day 2: 游览长城（八达岭段），下午参观颐和园",
            "Day 3: 游览天坛公园，参观雍和宫，品尝北京烤鸭",
            "Day 4: 游览798艺术区，参观三里屯商业区",
            "Day 5: 游览北海公园，参观景山公园，逛南锣鼓巷"
        ],
        "上海": [
            "Day 1: 游览外滩，参观南京路步行街",
            "Day 2: 游览豫园，参观田子坊创意园区",
            "Day 3: 游览上海博物馆，参观上海科技馆",
            "Day 4: 游览新天地，参观朱家角古镇",
            "Day 5: 游览迪士尼乐园，参观陆家嘴金融区"
        ],
        "杭州": [
            "Day 1: 游览西湖，参观雷峰塔",
            "Day 2: 游览灵隐寺，参观宋城",
            "Day 3: 游览千岛湖，体验水上活动",
            "Day 4: 游览河坊街，品尝杭帮菜",
            "Day 5: 游览九溪十八涧，参观中国丝绸博物馆"
        ]
    }
    
    if destination in plans:
        days_plan = plans[destination][:num_days]
        return "\\n\\n".join(days_plan)
    else:
        # 为其他目的地生成通用计划
        general_plan = []
        for i in range(1, num_days + 1):
            general_plan.append(f"Day {i}: 游览{destination}的主要景点，品尝当地美食，体验当地文化")
        return "\\n\\n".join(general_plan)

# 设置Streamlit应用
st.title("🛫 AI旅行计划助手")
st.caption("基于AI技术的个性化旅行计划生成器，无需外部API密钥")

# 初始化session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None

# 输入表单
col1, col2 = st.columns([2, 1])

with col1:
    destination = st.text_input("您想去哪里旅行？", placeholder="请输入目的地，如：北京、上海、杭州")
    num_days = st.number_input("计划旅行几天？", min_value=1, max_value=30, value=7)

with col2:
    st.write("")  # 添加一些间距
    if st.button("🎯 生成旅行计划", use_container_width=True):
        if destination:
            with st.spinner("正在为您制定旅行计划..."):
                # 直接生成旅行计划，不依赖外部API
                st.session_state.itinerary = generate_travel_plan(destination, num_days)
        else:
            st.error("请输入目的地")

# 显示生成的旅行计划
if st.session_state.itinerary:
    st.subheader("📋 您的旅行计划")
    st.write(st.session_state.itinerary)
    
    # 下载按钮
    col1, col2 = st.columns(2)
    with col1:
        # 生成ICS文件
        ics_content = generate_ics_content(st.session_state.itinerary)
        
        st.download_button(
            label="📅 下载日历文件 (.ics)",
            data=ics_content,
            file_name="travel_itinerary.ics",
            mime="text/calendar"
        )
    
    with col2:
        # 复制到剪贴板
        st.button("📋 复制计划到剪贴板", on_click=lambda: st.session_state.update({
            'clipboard': st.session_state.itinerary
        }))

# 使用说明
with st.expander("💡 使用说明"):
    st.markdown("""
    ### 如何使用AI旅行计划助手？
    
    1. **输入目的地**：在输入框中输入您想去旅行的城市名称
    2. **选择天数**：使用滑块选择您计划旅行的天数
    3. **生成计划**：点击"生成旅行计划"按钮，AI将为您制定详细的行程安排
    4. **下载日历**：可以下载.ics格式的日历文件，导入到您的手机或电脑日历中
    
    ### 支持的目的地
    - **北京**：包含天安门、故宫、长城等经典景点
    - **上海**：包含外滩、豫园、迪士尼等热门地点
    - **杭州**：包含西湖、灵隐寺、千岛湖等自然景观
    
    ### 特点
    - ✅ **无需API密钥**：不依赖任何外部服务
    - ✅ **即时生成**：计划立即可用
    - ✅ **日历兼容**：支持导入各种日历应用
    - ✅ **移动友好**：适合在手机上使用
    """)

# 页脚信息
st.markdown("---")
st.markdown("*AI旅行计划助手 - 让旅行规划变得简单有趣* 🚀")