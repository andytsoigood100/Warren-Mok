import streamlit as st

# Set page configuration
st.set_page_config(page_title="莫菲特報告生成器",
                   page_icon="📈",
                   layout="centered",
                   initial_sidebar_state="collapsed")

# 初始化 session state 來存儲數據
if 'report' not in st.session_state:
    st.session_state.report = ''
if 'custom_buy_rating' not in st.session_state:
    st.session_state.custom_buy_rating = ''
if 'custom_sell_rating' not in st.session_state:
    st.session_state.custom_sell_rating = ''
if 'buy_rating' not in st.session_state:
    st.session_state.buy_rating = '強烈買入'
if 'sell_rating' not in st.session_state:
    st.session_state.sell_rating = '賣出'
if 'show_copy_area' not in st.session_state:
    st.session_state.show_copy_area = False


# 定義生成報告的函數
def generate_report():
    company_name = st.session_state.company_name
    old_price = st.session_state.old_price
    new_price = st.session_state.new_price
    rating_change = st.session_state.rating_change

    # 根據評級變動設置最終評級
    if rating_change == "上升":
        final_rating = "與大市同步"
    elif rating_change == "中性":
        final_rating = "維持中性"
    else:  # 下降
        final_rating = "跑輸大市九條街"

    # 根據價格變化選擇評級
    if float(new_price) > float(old_price):
        # 使用買入評級
        if 'buy_rating' in st.session_state:
            if st.session_state.buy_rating == "自定義" and 'custom_buy_rating' in st.session_state:
                rating = st.session_state.custom_buy_rating
            else:
                rating = st.session_state.buy_rating
        else:
            rating = "強烈買入"
    else:
        # 使用沽售評級
        if 'sell_rating' in st.session_state:
            if st.session_state.sell_rating == "自定義" and 'custom_sell_rating' in st.session_state:
                rating = st.session_state.custom_sell_rating
            else:
                rating = st.session_state.sell_rating
        else:
            rating = "沽售評價"

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

    # 根據價格變化來決定報告內容
    if old_price > new_price:
        price_direction = "下降"
        price_change_text = f"從 {old_price:.2f} 元調整至 {new_price:.2f} 元"
    else:  # old_price < new_price
        price_direction = "上升"
        price_change_text = f"從 {old_price:.2f} 元調整至 {new_price:.2f} 元"

    # 莫菲特的學歷背景
    background = "牛角金會員，惠康Yuu資深會員，247fitness黑金會員，HKTVmall創始會員，香港大學space系畢業，香港理工大學cc系畢業。"

    # 生成報告文本
    report = (
        f"著名投資人莫菲特給予: {company_name} 的目標價格 {price_change_text}，{price_direction}。\n"
        f"維持 {rating} 評價。\n"
        f"評級 {rating_change} 至「{final_rating}」。\n\n"
        f"——莫菲特\n{background}")

    # 保存報告並顯示
    st.session_state.report = report
    st.success("報告已生成")


# 定義顯示可複製報告的函數
def show_copyable_report():
    report = st.session_state.report
    if report:
        st.session_state.show_copy_area = True
    else:
        st.warning("沒有報告可供複製")


# 設置應用程序標題和介紹
col1, col2 = st.columns([1, 2])
with col1:
    st.image("assets/mofit.png", width=200)
with col2:
    st.title("莫菲特報告生成器")
    st.write("輸入股票信息，生成莫菲特專業分析報告")

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
    buy_options = ['強烈買入', '增持', '跑赢大盤', '訓身買入', '借爆孖展買入', '自定義']
    sell_options = ['賣出', '沽售評價', '極度悲觀', '等破産', '等變牆紙', 'IFC天台見', '自定義']

    if price_comparison and old_price != 0 and new_price != 0:
        st.info("新價格大於舊價格，可選擇買入評級")
        selected_buy = st.selectbox("買入評級:", buy_options, key="buy_rating")

        # 自定義選項
        if selected_buy == "自定義":
            custom_buy = st.text_input("自定義買入評級:", key="custom_buy_rating")
    elif not price_comparison and old_price != 0 and new_price != 0:
        st.info("新價格小於舊價格，可選擇沽售評級")
        selected_sell = st.selectbox("沽售評級:", sell_options, key="sell_rating")

        # 自定義選項
        if selected_sell == "自定義":
            custom_sell = st.text_input("自定義沽售評級:", key="custom_sell_rating")
    else:
        st.warning("請先輸入不同的價格以顯示對應的評級選項")

    # 評級變動選項
    rating_change = st.radio("評級變動:", ['上升', '中性', '下降'], key="rating_change")

# 操作按鈕
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    generate_button = st.button("生成報告",
                                use_container_width=True,
                                on_click=generate_report)
with col2:
    copy_button = st.button("顯示可複製報告",
                            use_container_width=True,
                            on_click=show_copyable_report)

# 報告顯示區域
if st.session_state.report:
    st.markdown("### 生成的報告")
    st.text_area("報告內容",
                 value=st.session_state.report,
                 height=150,
                 key="display_report",
                 disabled=True,
                 label_visibility="collapsed")
    
    # 顯示報告生成的時間戳作為參考
    import datetime
    now = datetime.datetime.now()
    st.caption(f"報告生成時間: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 顯示可複製的文本區域
    if st.session_state.show_copy_area:
        st.markdown("### 複製報告文本")
        st.info("👇 請從下方文本框中選擇並複製報告")
        st.text_area("可複製的報告",
                    value=st.session_state.report,
                    height=150,
                    key="copyable_report",
                    label_visibility="collapsed")

# 添加底部說明
st.markdown("---")
st.caption("本應用僅供娛樂，不構成任何投資建議。")
