import streamlit as st import pandas as pd import yfinance as yf

사이드바: 필터 조정 UI

st.sidebar.header('벤저민 그레이엄 스크리너 설정')

필터 파라미터

max_per = st.sidebar.slider('최대 PER', 0.0, 50.0, 20.0) max_pbr = st.sidebar.slider('최대 PBR', 0.0, 5.0, 2.5) max_perpbr = st.sidebar.slider('PER×PBR 최대값', 0.0, 100.0, 40.0) min_dy = st.sidebar.slider('최소 배당수익률(%)', 0.0, 20.0, 2.0) min_market_cap = st.sidebar.number_input('최소 시가총액(10억 달러)', 0.0, 1000.0, 10.0)

티커 업로드 또는 기본 리스트 입력

uploaded_file = st.sidebar.file_uploader('CSV 티커 리스트 업로드', type=['csv']) if uploaded_file: df_t = pd.read_csv(uploaded_file) tickers = df_t['Symbol'].dropna().tolist() else: tickers = st.sidebar.text_area('티커 콤마 구분 입력', 'AAPL,MSFT,GOOG').split(',')

스크리닝 수행

if st.sidebar.button('스크리닝 시작'): results = [] for symbol in tickers: try: info = yf.Ticker(symbol).info pe = info.get('trailingPE') pb = info.get('priceToBook') dy = info.get('dividendYield') mc = info.get('marketCap') # 필수 지표 확인 if pe is None or pb is None or dy is None or mc is None: continue # 배당수익률 %단위 보정 dy_pct = dy * 100 if dy < 1 else dy # 필터 조건 적용 if ( pe < max_per and pb < max_pbr and pe * pb < max_perpbr and dy_pct >= min_dy and mc / 1e9 >= min_market_cap ): results.append({ 'Symbol': symbol, 'PER': round(pe, 2), 'PBR': round(pb, 2), 'PER×PBR': round(pe * pb, 2), 'Dividend Yield (%)': round(dy_pct, 2), 'Market Cap (Billion $)': round(mc / 1e9, 2) }) except Exception: continue

# 결과 표시 및 다운로드
if results:
    df_res = pd.DataFrame(results)
    st.dataframe(df_res)
    excel_data = df_res.to_excel(index=False)
    st.sidebar.download_button('결과 엑셀로 저장', data=excel_data, file_name='graham_screener.xlsx')
else:
    st.write('조건을 만족하는 종목이 없습니다.')

