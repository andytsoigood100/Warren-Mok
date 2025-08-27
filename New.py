import streamlit as st
import random
from datetime import datetime

# 隨機生成的評價列表
negative_ratings = [
    "沽售評價", "極度悲觀", "等變恒大牆紙", "IFC天台見", "等破産", 
    "割韭菜", "接火棒", "接刀", "坐艇", "鐵達尼號", 
    "留返啲錢嚟瞓天橋底", "送外賣維生", "點心紙變廢紙"
]

negative_actions = [
    "恒大清倉散貨", "輸間廠", "慘過做X", "跑輸大市九條街", "等变大閘蟹"
]

positive_ratings = [
    "借爆孖展買入", "跑赢大盤", "訓身買入", "All-in", "十倍孖展", 
    "增大力持", "強烈買入", "唔买走宝", "時代既選擇", "財富自由", 
    "極度看多", "槓桿狂熱", "確信買入", "估值重大重估"
]

positive_actions = [
    "長線投資", "贏間廠", "魚翅撈飯", "食大糊", "與大市同步上升", "终极乐观信号"
]

neutral_ratings = ["中性評級", "按兵不動"]

# 投資箴言（調侃韭菜）
investment_quotes = [
    "韭菜的宿命：割了一茬，還會長出新的一茬。",
    "新手入場三步曲：買高、套牢、割肉。",
    "股市就像一場派對，韭菜永遠是最後一個知道的。",
    "不要和韭菜談風險，他們只關心暴富。",
    "韭菜漲。",
    "股市的真相：韭菜的錢包是主力的提款機。",
    "韭菜的特長：在最高點買入，在最低點賣出。",
    "韭菜的口頭禪：再等等，應該會漲回來的。",
    "主力吃肉，韭菜喝湯；主力撤退，韭菜進場。",
    "每位韭菜的心聲：我就是那個例外。",
    "韭菜的優勢：虧錢的速度比別人快。",
    "韭菜的日常：追高殺跌，反覆被收割。",
    "股市最大的謊言：我是為了價值投資而來的。",
    "韭菜的夢想：一夜暴富；韭菜的現實：一夜歸零。",
    "不是每棵韭菜都能成為參天大樹，大多數都被割掉了。",
    "韭菜的信仰崩塌：原來我不會賺錢，只會虧錢。",
    "韭菜的生存法則：越跌越買，直到彈盡糧絕。",
    "股市裡的成功秘訣：當別人都是韭菜時，你已經是莊家了。",
    "韭菜的終極目標：從小韭菜變成老韭菜，再到被割乾淨。",
    "股市的本質：主力做局，韭菜入局，最後韭菜出局。",
]

# Streamlit 標題
st.title("莫菲特報告生成器")

# 自動顯示日期().strftime("%Y年%m月%d日")  # 格式化為繁體中文日期
st.markdown(f"**報告日期:** {current_date}")

# 使用者輸入
company_name = st.text_input("1. 公司名稱:")
old_price = st.number_input("2. 舊價格 (元):", min_value=0.0, format="%.2f")
new_price = st.number_input("3. 新價格 (元):", min_value=0.0, format="%.2f")

if st.button("生成報告"):
    if not company_name:
        st.error("請填寫公司名稱！")
    elif old_price == 0 and new_price == 0:
        st.error("請填寫有效的價格！")
    else:
        # 計算百分比變化
        price_change = new_price - old_price
        percentage_change = (price_change / old_price) * 100 if old_price != 0 else 0

        # 報告內容
        report = f"""
**著名投資人莫菲特給予:**  
{company_name} 的目標價格從 {old_price:.2f} 元調整至 {new_price:.2f} 元 （變動: {percentage_change:+.2f}%），{'上升' if price_change > 0 else '下降'}。

"""
        if            rating = random.choice(positive_ratings)
            action = random.choice(positive_actions)
            report += f"**維持:** {rating}\n"
            report += f"**評級 上升 至:** {action}\n"
        elif price_change < 0:
            rating = random.choice(negative_ratings)
            action = random.choice(negative_actions)
            report += f"**維持:** {rating}\n"
            report += f"**評級 下降 至:** {action}\n"
        else:
            rating = random.choice(neutral_ratings)
            report += f"**維持:** {rating}\n"

        # 添加投資箴言
        quote = random.choice(investment_quotes)
        report += f"\n**——莫菲特箴言**\n> {quote}\n"

        # 添加莫菲特資歷
        report += """
**——莫菲特資歷**  
- 對沖基金莫郡創辦人, CEO, 董事長;  
- 華爾街工作25年+ (1979-2004年);  
- 天使投資人;
"""

        # 在文本框中顯示完整的報告
        st.text_area("完整報告（可複製）:", report, height=300)
