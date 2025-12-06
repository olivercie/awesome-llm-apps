#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Travel Agent - 最小化运行版本
零依赖设计，仅使用Python标准库
"""

import datetime
import re
from typing import List, Dict

class TravelAgent:
    """最小化旅行助手类"""
    
    def __init__(self):
        self.travel_plans = {
            "北京": [
                "Day 1: 游览天安门广场和故宫博物院，参观国家博物馆",
                "Day 2: 游览长城（八达岭段），下午参观颐和园", 
                "Day 3: 游览天坛公园，参观雍和宫，品尝北京烤鸭",
                "Day 4: 游览798艺术区，参观三里屯商业区",
                "Day 5: 游览北海公园，参观景山公园，逛南锣鼓巷",
                "Day 6: 游览北京环球影城，体验主题乐园",
                "Day 7: 游览香山公园，参观清华大学，品尝护国寺小吃"
            ],
            "上海": [
                "Day 1: 游览外滩，参观南京路步行街",
                "Day 2: 游览豫园，参观田子坊创意园区", 
                "Day 3: 游览上海博物馆，参观上海科技馆",
                "Day 4: 游览新天地，参观朱家角古镇",
                "Day 5: 游览迪士尼乐园，参观陆家嘴金融区",
                "Day 6: 游览上海野生动物园，体验上海夜生活",
                "Day 7: 游览世纪公园，参观中华艺术宫，品尝本帮菜"
            ],
            "杭州": [
                "Day 1: 游览西湖，参观雷峰塔",
                "Day 2: 游览灵隐寺，参观宋城",
                "Day 3: 游览千岛湖，体验水上活动",
                "Day 4: 游览河坊街，品尝杭帮菜",
                "Day 5: 游览九溪十八涧，参观中国丝绸博物馆",
                "Day 6: 游览西溪湿地公园，体验生态旅游",
                "Day 7: 游览钱塘江大潮，体验杭州历史文化"
            ],
            "深圳": [
                "Day 1: 游览深圳湾公园，参观世界之窗",
                "Day 2: 游览欢乐谷，体验主题乐园",
                "Day 3: 游览东部华侨城，参观茶溪谷",
                "Day 4: 游览大梅沙海滨公园，品尝海鲜",
                "Day 5: 游览莲花山公园，参观深圳博物馆",
                "Day 6: 游览西涌海滩，体验海上运动",
                "Day 7: 游览华强北商业区，体验科技文化"
            ],
            "广州": [
                "Day 1: 游览珠江夜游，参观广州塔（小蛮腰）",
                "Day 2: 游览陈家祠，参观上下九步行街",
                "Day 3: 游览长隆野生动物园，体验主题乐园",
                "Day 4: 游览白云山，品尝广州早茶",
                "Day 5: 游览越秀公园，参观广州博物馆",
                "Day 6: 游览沙面岛，体验异国风情",
                "Day 7: 游览北京路步行街，品尝粤式美食"
            ]
        }
    
    def generate_itinerary(self, destination: str, num_days: int) -> List[str]:
        """
        生成旅行行程
        
        Args:
            destination: 目的地
            num_days: 天数
            
        Returns:
            行程列表
        """
        if destination in self.travel_plans:
            plans = self.travel_plans[destination]
            return plans[:num_days]
        else:
            # 为未知目的地生成通用行程
            return [f"Day {i}: 游览{destination}的主要景点，品尝当地美食，体验当地文化" 
                   for i in range(1, num_days + 1)]
    
    def generate_ics_content(self, itinerary: List[str], start_date: str = None) -> str:
        """
        生成ICS日历文件内容
        
        Args:
            itinerary: 行程列表
            start_date: 开始日期 (YYYY-MM-DD)
            
        Returns:
            ICS格式的文件内容
        """
        if start_date is None:
            start_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        start_dt = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        
        ics_lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AI Travel Planner//github.com//"
        ]
        
        for i, activity in enumerate(itinerary):
            # 提取Day和活动内容
            day_match = re.search(r'Day (\d+):\s*(.+)', activity)
            if day_match:
                day_num = int(day_match.group(1))
                activity_desc = day_match.group(2).strip()
            else:
                day_num = i + 1
                activity_desc = activity
            
            # 计算活动日期
            activity_date = start_dt + datetime.timedelta(days=day_num - 1)
            date_str = activity_date.strftime("%Y%m%d")
            
            ics_lines.extend([
                "BEGIN:VEVENT",
                f"SUMMARY:Day {day_num} - {activity_desc[:50]}",  # 限制长度
                f"DESCRIPTION:{activity_desc}",
                f"DTSTART;VALUE=DATE:{date_str}",
                f"DTEND;VALUE=DATE:{date_str}",
                f"DTSTAMP:{datetime.datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
                "END:VEVENT"
            ])
        
        ics_lines.append("END:VCALENDAR")
        return "\n".join(ics_lines)
    
    def display_itinerary(self, destination: str, num_days: int):
        """显示行程"""
        print(f"\n{'='*50}")
        print(f"🎯 {destination} {num_days}天旅行计划")
        print(f"{'='*50}")
        
        itinerary = self.generate_itinerary(destination, num_days)
        for i, activity in enumerate(itinerary, 1):
            print(f"\n📅 {activity}")
        
        return itinerary
    
    def save_to_file(self, content: str, filename: str):
        """保存内容到文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"\n✅ 文件已保存到: {filename}")
        except Exception as e:
            print(f"\n❌ 保存文件失败: {e}")

def print_banner():
    """打印欢迎横幅"""
    print("""
🛫 AI旅行计划助手 (最小化版本)
=====================================
基于Python标准库，无需外部依赖
支持目的地：北京、上海、杭州、深圳、广州

功能特点：
✅ 完全离线运行
✅ 无需API密钥  
✅ 支持ICS日历导出
✅ 跨平台兼容
=====================================
""")

def main():
    """主函数"""
    print_banner()
    
    agent = TravelAgent()
    
    while True:
        print("\n" + "-"*40)
        print("请选择操作：")
        print("1. 生成旅行计划")
        print("2. 查看支持的目的地")
        print("3. 退出")
        print("-"*40)
        
        choice = input("\n请输入选项 (1-3): ").strip()
        
        if choice == "1":
            # 生成旅行计划
            print("\n🎯 生成旅行计划")
            print("-"*30)
            
            destination = input("请输入目的地: ").strip()
            if not destination:
                print("❌ 目的地不能为空")
                continue
            
            try:
                num_days = int(input("请输入旅行天数 (1-30): ").strip())
                if num_days < 1 or num_days > 30:
                    print("❌ 天数必须在1-30之间")
                    continue
            except ValueError:
                print("❌ 请输入有效的数字")
                continue
            
            # 显示行程
            itinerary = agent.display_itinerary(destination, num_days)
            
            # 询问是否保存
            save_choice = input("\n是否保存为ICS日历文件？(y/n): ").strip().lower()
            if save_choice in ['y', 'yes', '是']:
                filename = f"{destination}_{num_days}天_旅行计划.ics"
                ics_content = agent.generate_ics_content(itinerary)
                agent.save_to_file(ics_content, filename)
            
            # 询问是否继续
            continue_choice = input("\n是否继续规划其他旅行？(y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes', '是']:
                break
                
        elif choice == "2":
            # 查看支持的目的地
            print("\n📍 支持的目的地:")
            print("-"*20)
            for city in agent.travel_plans.keys():
                print(f"• {city}")
            print("\n💡 其他城市将生成通用行程模板")
            
        elif choice == "3":
            print("\n👋 感谢使用AI旅行计划助手！")
            break
            
        else:
            print("❌ 无效选项，请重新选择")

if __name__ == "__main__":
    main()