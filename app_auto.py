import streamlit as st
import random
from streamlit_js_eval import streamlit_js_eval
import datetime

# 設置頁面配置
st.set_page_config(page_title="莫菲特報告生成器",
                   page_icon="📈",
                   layout="centered",
                   initial_sidebar_state="collapsed")

# 定義評級文本列表，方便後續添加更多文案
BUY_RATINGS = ['強烈買入', '增持', '跑赢大盤', '訓身買入', '借爆孖展買入']
SELL_RATINGS = ['賣出', '沽售評價', '極度悲觀', '等破産', '等變牆紙', 'IFC天台見']

# 評級變動對應的最終評級
RATING_UP = "與大市同步"
RATING_NEUTRAL = "維持中性"
RATING_DOWN = "跑輸大市九條街"

# 莫菲特的學歷背景
BACKGROUND = "牛角金會員，惠康Yuu資深會員，247fitness黑金會員，HKTVmall創始會員，香港大學space系畢業，香港理工大學cc系畢業。"

# 初始化 session state 來存儲數據
if 'report' not in st.session_state:
    st.session_state.report = ''
if 'auto_report' not in st.session_state:
    st.session_state.auto_report = ''
if 'custom_buy_rating' not in st.session_state:
    st.session_state.custom_buy_rating = ''
if 'custom_sell_rating' not in st.session_state:
    st.session_state.custom_sell_rating = ''
if 'buy_rating' not in st.session_state:
    st.session_state.buy_rating = '強烈買入'
if 'sell_rating' not in st.session_state:
    st.session_state.sell_rating = '賣出'


# 一鍵複製功能 - 改用更簡單的方法
def copy_text(text):
    # 直接將文本顯示在臨時輸入框中，方便用户手動複製
    st.code(text, language=None)
    st.info("👆 請從上方框中選擇並複製文本（Ctrl+A 全選，Ctrl+C 複製）")


# 手動生成報告
def generate_report():
    company_name = st.session_state.company_name
    old_price = st.session_state.old_price
    new_price = st.session_state.new_price
    rating_change = st.session_state.rating_change

    # 驗證必填欄位
    if not company_name:
        st.error("請填寫公司名稱")
        return

    # 確保價格是有效數字
    try:
        old_price = float(old_price)
        new_price = float(new_price)
    except ValueError:
        st.error("請輸入有效的價格數字")
        return

    # 確保價格不同
    if old_price == new_price:
        st.error("舊價格和新價格不能相同")
        return

    # 根據評級變動設置最終評級
    if rating_change == "上升":
        final_rating = RATING_UP
    elif rating_change == "中性":
        final_rating = RATING_NEUTRAL
    else:  # 下降
        final_rating = RATING_DOWN

    # 根據價格變化選擇評級
    if float(new_price) > float(old_price):
        # 使用買入評級
        if 'buy_rating' in st.session_state:
            if st.session_state.buy_rating == "自定義" and 'custom_buy_rating' in st.session_state:
                rating = st.session_state.custom_buy_rating
            else:
                rating = st.session_state.buy_rating
        else:
            rating = BUY_RATINGS[0]
        price_direction = "上升"
    else:
        # 使用沽售評級
        if 'sell_rating' in st.session_state:
            if st.session_state.sell_rating == "自定義" and 'custom_sell_rating' in st.session_state:
                rating = st.session_state.custom_sell_rating
            else:
                rating = st.session_state.sell_rating
        else:
            rating = SELL_RATINGS[0]
        price_direction = "下降"

    # 計算變動百分比
    if old_price > 0:
        price_change_percent = (new_price - old_price) / old_price * 100
        price_change_text = f"從 {old_price:.2f} 元調整至 {new_price:.2f} 元 (變動: {price_change_percent:.2f}%)"
    else:
        price_change_text = f"從 {old_price:.2f} 元調整至 {new_price:.2f} 元"

    # 生成報告文本
    report = (
        f"著名投資人莫菲特給予: {company_name} 的目標價格 {price_change_text}，{price_direction}。\n"
        f"維持 {rating} 評價。\n"
        f"評級 {rating_change} 至「{final_rating}」。\n\n"
        f"——莫菲特\n{BACKGROUND}")

    # 保存報告並顯示
    st.session_state.report = report
    st.success("報告已生成")


# 自動生成報告
def auto_generate_report():
    company_name = st.session_state.company_name_auto
    old_price = st.session_state.old_price_auto
    new_price = st.session_state.new_price_auto

    # 驗證必填欄位
    if not company_name:
        st.error("請填寫公司名稱")
        return

    # 確保價格是有效數字
    try:
        old_price = float(old_price)
        new_price = float(new_price)
    except ValueError:
        st.error("請輸入有效的價格數字")
        return

    # 計算價格變動百分比
    if old_price > 0:
        price_change_percent = (new_price - old_price) / old_price * 100
    else:
        price_change_percent = 0

    # 根據價格變化選擇評級類型和評級變動
    if new_price > old_price:
        rating = random.choice(BUY_RATINGS)
        rating_change = "上升"
        final_rating = RATING_UP
        price_direction = "上升"
    elif new_price < old_price:
        rating = random.choice(SELL_RATINGS)
        rating_change = "下降"
        final_rating = RATING_DOWN
        price_direction = "下降"
    else:
        # 價格相同時
        if random.choice([True, False]):
            rating = random.choice(BUY_RATINGS)
        else:
            rating = random.choice(SELL_RATINGS)
        rating_change = "中性"
        final_rating = RATING_NEUTRAL
        price_direction = "維持不變"

    # 生成報告文本
    price_change_text = f"從 {old_price:.2f} 元調整至 {new_price:.2f} 元 (變動: {price_change_percent:.2f}%)"
    report = (
        f"著名投資人莫菲特給予: {company_name} 的目標價格 {price_change_text}，{price_direction}。\n"
        f"維持 {rating} 評價。\n"
        f"評級 {rating_change} 至「{final_rating}」。\n\n"
        f"——莫菲特\n{BACKGROUND}")

    # 保存報告並顯示
    st.session_state.auto_report = report
    st.success("報告已自動生成")


# 設置應用程序標題和介紹
st.title("莫菲特報告生成器")
st.write("輸入股票信息，生成莫菲特專業分析報告")

# 創建兩個標籤頁
tab1, tab2 = st.tabs(["手動生成報告", "自動生成報告"])

# 手動生成報告標籤頁
with tab1:
    # 創建輸入部件
    with st.container():
        st.subheader("基本信息")
        company_name = st.text_input("公司名稱:", key="company_name")

        col1, col2 = st.columns(2)
        with col1:
            old_price = st.number_input("舊價格 (元):",
                                        min_value=0.0,
                                        value=0.0,
                                        step=0.01,
                                        format="%.2f",
                                        key="old_price")
        with col2:
            new_price = st.number_input("新價格 (元):",
                                        min_value=0.0,
                                        value=0.0,
                                        step=0.01,
                                        format="%.2f",
                                        key="new_price")

            # 計算並顯示價格變動百分比
            if old_price > 0 and new_price >= 0:
                price_change_percent = (new_price -
                                        old_price) / old_price * 100
                st.info(f"價格變動: {price_change_percent:.2f}%")

    # 評級選項
    with st.container():
        st.subheader("分析評級")

        # 比較價格變化
        try:
            old_price = float(st.session_state.get('old_price', 0))
            new_price = float(st.session_state.get('new_price', 0))
            price_comparison = new_price > old_price
        except:
            price_comparison = False

        # 買入評級選項 (只在新價格 > 舊價格時顯示)
        buy_options = BUY_RATINGS + ['自定義']
        sell_options = SELL_RATINGS + ['自定義']

        if price_comparison and old_price != 0 and new_price != 0:
            st.info("新價格大於舊價格，可選擇買入評級")
            selected_buy = st.selectbox("買入評級:", buy_options, key="buy_rating")

            # 自定義選項
            if selected_buy == "自定義":
                custom_buy = st.text_input("自定義買入評級:", key="custom_buy_rating")
        elif not price_comparison and old_price != 0 and new_price != 0:
            st.info("新價格小於舊價格，可選擇沽售評級")
            selected_sell = st.selectbox("沽售評級:",
                                         sell_options,
                                         key="sell_rating")

            # 自定義選項
            if selected_sell == "自定義":
                custom_sell = st.text_input("自定義沽售評級:",
                                            key="custom_sell_rating")
        else:
            st.warning("請先輸入不同的價格以顯示對應的評級選項")

        # 評級變動選項
        rating_change = st.radio("評級變動:", ['上升', '中性', '下降'],
                                 key="rating_change")

    # 生成報告按鈕
    if st.button("手動生成報告", use_container_width=True):
        generate_report()

    # 顯示報告區域
    if st.session_state.report:
        st.markdown("### 生成的報告")
        # 使用可選擇的文本顯示
        st.text_area("報告內容",
                     value=st.session_state.report,
                     height=180,
                     key="display_report",
                     disabled=False,
                     label_visibility="collapsed")

        # 一鍵複製按鈕
        if st.button("📋 顯示易複製報告",
                     use_container_width=True,
                     key="copy_manual_report"):
            copy_text(st.session_state.report)

        # 顯示報告生成的時間戳
        now = datetime.datetime.now()
        st.caption(f"報告生成時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 自動生成報告標籤頁
with tab2:
    st.subheader("快速生成報告")
    st.write("只需填寫基本信息，系統會自動生成報告")

    company_name_auto = st.text_input("公司名稱:", key="company_name_auto")

    col1, col2 = st.columns(2)
    with col1:
        old_price_auto = st.number_input("舊價格 (元):",
                                         min_value=0.0,
                                         value=0.0,
                                         step=0.01,
                                         format="%.2f",
                                         key="old_price_auto")
    with col2:
        new_price_auto = st.number_input("新價格 (元):",
                                         min_value=0.0,
                                         value=0.0,
                                         step=0.01,
                                         format="%.2f",
                                         key="new_price_auto")

        # 計算並顯示價格變動百分比
        if old_price_auto > 0 and new_price_auto >= 0:
            price_change_percent = (new_price_auto -
                                    old_price_auto) / old_price_auto * 100
            st.info(f"價格變動: {price_change_percent:.2f}%")

    # 自動生成報告按鈕
    if st.button("自動生成報告", use_container_width=True):
        auto_generate_report()

    # 顯示自動生成的報告
    if st.session_state.auto_report:
        st.markdown("### 自動生成的報告")
        st.text_area("報告內容",
                     value=st.session_state.auto_report,
                     height=180,
                     key="display_auto_report",
                     disabled=False,
                     label_visibility="collapsed")

        # 顯示易複製報告按鈕
        if st.button("📋 顯示易複製報告",
                     use_container_width=True,
                     key="copy_auto_report"):
            copy_text(st.session_state.auto_report)

        # 顯示報告生成的時間戳
        now = datetime.datetime.now()
        st.caption(f"報告生成時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")

# 添加底部說明
st.markdown("---")
st.caption("本應用僅供娛樂，不構成任何投資建議。")
