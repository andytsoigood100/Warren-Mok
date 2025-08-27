import streamlit as st
import random

# 隨機生成的評價列表
negative_ratings = [
    "沽售評價", "極度悲觀", "等變恒大牆紙", "IFC天台見", "等破産", 
    "割韭菜", "接火棒", "接刀", "坐艇", "鐵達尼號", 
    "留返啲錢嚟搭巴士都好", "瞓天橋底", "送外賣維生", "點心紙變廢紙"
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

# Streamlit 標題
st.title("莫菲特報告生成器")

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
        st.markdown(f"**著名投資人莫菲特給予:** {company_name} 的目標價格從 {old_price:.2f} 元調整至 {new_price:.2f} 元 （變動: {percentage_change:+.2f}%），{'上升' if price_change > 0 else '下降'}。")

        if price_change > 0:
            rating = random.choice(positive_ratings)
            action = random.choice(positive_actions)
            st.markdown(f"**維持:** {rating}")
            st.markdown(f"**評級 上升 至:** {action}")
        elif price_change < 0:
            rating = random.choice(negative_ratings)
            action = random.choice(negative_actions)
            st.markdown(f"**維持:** {rating}")
            st.markdown(f"**評級 下降 至:** {action}")
        else:
            rating = random.choice(neutral_ratings)
            st.markdown(f"**維持:** {rating}")

# Streamlit 執行方式
# 在終端運行以下命令：
# streamlit run your_script_name.py
