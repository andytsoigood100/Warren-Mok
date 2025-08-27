app.py

-- coding: utf-8 --

#莫菲特報告生成器（Streamlit 版）

import random
import streamlit as st

st.setpageconfig(pagetitle="莫菲特報告生成器", pageicon="📈")

st.title("莫菲特報告生成器")
st.caption("快速生成股票目標價變動報告（純屬娛樂，勿作投資依據）")

隨機字串池（繁體）

NEG_EVALS = [
    "沽售評價",
    "極度悲觀",
    "等變恒大牆紙",
    "IFC天台見",
    "等破產",
    "割韭菜",
    "接火棒",
    "接刀",
    "坐艇，鐵達尼號",
    "留返啲錢嚟搭巴士都好",
    "瞓天橋底",
    "送外賣維生",
    "點心紙變廢紙",
]

NEG_LEVELS = [
    "恒大清倉散貨",
    "輸間廠",
    "慘過做X",
    "跑輸大市九條街",
    "等變大閘蟹",
]

POS_EVALS = [
    "借爆孖展買入",
    "跑贏大盤",
    "訓身買入",
    "All-in",
    "十倍孖展",
    "增大力持",
    "強烈買入",
    "唔買走寶",
    "時代既選擇",
    "財富自由",
    "極度看多",
    "槓桿狂熱",
    "確信買入",
    "估值重大重估",
]

POS_LEVELS = [
    "長線投資",
    "贏間廠",
    "魚翅撈飯",
    "食大糊",
    "與大市同步上升",
    "終極樂觀信號",
]

def formatpct(oldprice: float, new_price: float) -> tuple[str, str]:
    """
    回傳 (百分比字串, 方向詞)
    百分比以舊價格為基準。
    """
    # 方向
    if newprice > oldprice:
        direction = "上升"
    elif newprice < oldprice:
        direction = "下降"
    else:
        direction = "持平"

    # 百分比
    if old_price == 0:
        if new_price == 0:
            pct_str = "+0.00%"
        else:
            pct_str = "無法計算（舊價格為 0）"
        return pct_str, direction

    pct = (newprice - oldprice) / old_price * 100
    # 帶正負號
    pct_str = f"{pct:+.2f}%"
    return pct_str, direction

with st.form("moffett_form"):
    company = st.text_input("1）公司名稱", value="")
    oldprice = st.numberinput("2）舊價格（元）", min_value=0.0, value=0.0, step=0.1, format="%.4f")
    newprice = st.numberinput("3）新價格（元）", min_value=0.0, value=0.0, step=0.1, format="%.4f")
    submitted = st.formsubmitbutton("生成報告")

if submitted:
    if not company.strip():
        st.warning("請輸入公司名稱。")
    else:
        pctstr, direction = formatpct(oldprice, newprice)

        # 標題行
        headline = (
            f"著名投資人莫菲特給予：{company} 的目標價格 "
            f"從 {oldprice:.2f} 元調整至 {newprice:.2f} 元 "
            f"(變動：{pct_str})，{direction}。"
        )

        st.subheader("報告結果")
        st.write(headline)

        # 根據升跌持平輸出評語／評級
        if newprice < oldprice:
            evalpick = random.choice(NEGEVALS)
            levelpick = random.choice(NEGLEVELS)
            st.write(f"維持「{eval_pick}」評價。")
            st.write(f"評級 下降 至「{level_pick}」。")
        elif newprice > oldprice:
            evalpick = random.choice(POSEVALS)
            levelpick = random.choice(POSLEVELS)
            st.write(f"維持「{evalpick}」評價，評級 上升 至「{levelpick}」。")
        else:
            # 持平
            st.write("維持中性評級／按兵不動。")

        # 可選：匯總文字，方便複製
        st.divider()
        summary_lines = [headline]
        if newprice < oldprice:
            summarylines.append(f"維持「{evalpick}」評價。")
            summarylines.append(f"評級 下降 至「{levelpick}」。")
        elif newprice > oldprice:
            summarylines.append(f"維持「{evalpick}」評價，評級 上升 至「{level_pick}」。")
        else:
            summary_lines.append("維持中性評級／按兵不動。")

        fulltext = "\n".join(summarylines)

        st.textarea("報告文本（可複製）", value=fulltext, height=180)

