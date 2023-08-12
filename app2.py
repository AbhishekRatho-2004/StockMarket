import streamlit as st
import openai
import streamlit_authenticator as stauth
from dependancies import fetch_users,signup
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import time
import random
import yfinance as yf
from streamlit_lottie import st_lottie
import json
import requests
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import pandas_ta as ta
from PIL import Image
import requests
from io import BytesIO


th_props = [
  ('font-size', '25px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', 'White')
  ]
                               
td_props = [
  ('font-size', '20px')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]
def load_lottiefile(filepath: str):
    with open(filepath,"r") as f:
        return json.load(f)
    
def load_lottieur(url: str):
    r=requests.get(url)
    if r.status_code!=200:
        return None
    return r.json()

def stock_data(symbol,start,end):
    stock=yf.Ticker(symbol)
    data=stock.history(start=start,end=end)
    return data
def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'white'
    return 'color: %s' % color


st.set_page_config(page_title='Streamlit', page_icon='🐍',layout='wide',initial_sidebar_state='collapsed')
selected=option_menu(
                    menu_title=None,
                    menu_icon="cast",
                    default_index=0,
                    options=['Home','Company','Stocks','Predict','Dashboard','Course','Indicators','Bot'],
                    orientation='horizontal',
                    styles={
                        'container':{"background-color":"black","border":'1px','font-weight':'bold',},
                        'nav-link':{'font-size':'15px','text-align':'left','margin':'0px','color':'cyan','--hover-color':'red'},
                        'nav-link-selected':{"background-color":'green','color':'white'}
                    }
                )


try:
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []
    
    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[Login]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        signup()
    
    if username:
        if username in usernames:
            if authentication_status:
                
                # let User see app
                st.sidebar.subheader(f'Welcome {username}')
                Authenticator.logout('Log Out', 'sidebar')

                st.markdown("""
                <style>
                header.css-1avcm0n.ezrtsby2{
                            visibility:hidden;
                }
                </style>
                """,unsafe_allow_html=True)
                
                if selected=='Home':
                    st.header('Stock Market')
                    tata,reliance,microsoft,apple=st.columns(4)
                    with tata:
                        st.markdown('''
                        <html>
                                <body>
                                    <div class="grid2" style="border:4px solid white;border-radius:5px;text-align:center"><img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR37dLVRht1Z5IqL7L_iL_O80B30HUAcktfbA&usqp=CAU" style="height:140px;width:309px;"><br><p style="margin-top:10px;font-weight:bold;font-size:20px"> The Reliance Group is an Indian multinational conglomerate headquartered in Mumbai. Established in 1868, it is India's largest conglomerate, with products and services in over 150 countries, and operations in 100 countries across six continents</p><a href="https://economictimes.indiatimes.com/tata-investment-corporation-ltd/stocks/companyid-13540.cms" style="font-size:23px;font-weight:bold;padding:3px;margin-top:-3px">Invest now</a></div>
                                </body>
                        </html>
                    ''',unsafe_allow_html=True)
                    with reliance:
                        st.markdown('''
                        <html>
                                <body>
                                    <div class="grid1" style="border:4px solid white;text-align:center"><img src="data:image/png;base64,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" style="width:313px;height:140px"> <br> <p style="margin-top:10px;font-weight:bold;font-size:20px">The Tata Group is an Indian multinational conglomerate headquartered in Mumbai. Established in 1868, it is India's largest conglomerate, with products and services in over 150 countries, and operations in 100 countries across six continents</p><a href="https://economictimes.indiatimes.com/tata-investment-corporation-ltd/stocks/companyid-13540.cms" style="font-size:23px;font-weight:bold;padding:3px;margin-top:10px">Invest now</a></div>
                                </body>
                        </html>
                    ''',unsafe_allow_html=True)
                    with microsoft:
                        st.markdown('''
                        <html>
                                <body>
                                    <div class="grid3" style="border:4px solid white;text-align:center"><img src="https://tse3.mm.bing.net/th/id/OIP.lkqtEZbLSCp-42v8s_Q-dgHaEK?w=300&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7" style="border:0px solid white;width:310px;height:140px;margin-top:0px;"><br><p style="margin-top:10px;font-weight:bold;font-size:20px">The Microsoft is an Indian multinational conglomerate headquartered in Mumbai. Established in 1868, it is India's largest conglomerate, with products and services in over 150 countries, and operations in 100 countries across six continents</p><a href="https://economictimes.indiatimes.com/tata-investment-corporation-ltd/stocks/companyid-13540.cms" style="font-size:23px;font-weight:bold;padding:3px;margin-top:-3px">Invest now</a></div>
                                </body>
                        </html>
                    ''',unsafe_allow_html=True)
                    with apple:
                        st.markdown('''
                        <html>
                                <body>
                                    <div class="grid4" style="border:4px solid white;text-align:center"><img src="https://tse2.mm.bing.net/th/id/OIP.7YSDSH3nNnYYlNdI6uJ1ygHaEo?w=283&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7" style="width:310px;
                    height:140px;"><br><p style="margin-top:10px;font-weight:bold;font-size:20px">The Reliance Group is an Indian multinational conglomerate headquartered in Mumbai. Established in 1868, it is India's largest conglomerate, with products and services in over 150 countries, and operations in 100 countries across six continents</p><a href="https://economictimes.indiatimes.com/tata-investment-corporation-ltd/stocks/companyid-13540.cms" style="font-size:23px;font-weight:bold;padding:3px;margin-top:-3px">Invest now</a></div>
                                </body>
                        </html>
                    ''',unsafe_allow_html=True)
                    st.markdown("""
                    <html>
                            <body>
                            <html>
                            <body>
                                <h4 style="text-align:center;color:red; font-size:37px;margin-top:20px;">FAQ</h4>
                                <details>
                                <summary style="font-weight:bold;font-size:28px;">Can a beginner trade in unlisted stocks?</summary>
                                <p style="color:cyan;font-size:24px;margin-left:30px;margin-top:14px;">A beginner can trade in unlisted stocks, but financial experts advise against them. As unlisted stocks are not with the market regulating authority – the Securities and Exchange Board of India (SEBI), it is not safe to invest in them</p>
                                </details>
                                <details>
                                <summary style="font-weight:bold;font-size:28px">How to find good companies as there are thousands of publicly listed companies in the Indian stock market?</summary>
                                <p style="color:cyan;font-size:24px;margin-left:30px;margin-top:14px;">An easier approach would be to use a stock screener. By using stock screeners, you can apply a few filters (like PE ratio, debt to equity ratio, market cap, etc) specific to the industry which you are investigating and get a list of limited stocks based on the criteria applied.</p>
                                </details>
                                <details>
                                <summary style="font-weight:bold;font-size:28px">Is investing in small caps more profitable than large caps?</summary>
                                <p style="color:cyan;font-size:24px;margin-left:30px;margin-top:14px;">Small caps companies have the caliber to grow faster compared to large caps. There can be a number of hidden gems in the small-cap industry which might not have been discovered by the market yet. However, their true potential is still untested. On the other hand, large-cap companies have already proved their worth to the market.
                    Anyways, the quality of stock is more important than the size of the company. There are a number of large-cap companies which has consistently given good returns to their shareholders. Overall, investing in small caps can be more profitable than large caps if you are investing in the right stocks</p>
                                </details>
                                <details>
                                <summary style="font-weight:bold;font-size:28px">How many returns can I expect from the market?  </summary>
                                <p style="color:cyan;font-size:24px;margin-left:30px;margin-top:14px;">During a good market, your portfolio can give you a return as high as 30-35% (the benchmark index Nifty alone gave a return of over 50.20% in the last year till Sept 2021). However, during a bad market- the returns can be as low as 2-5% or maybe even negative.

                    If you sum up everything, you can expect an annual return of 15-18%, depending on how good you were at picking stocks. Nevertheless, you can generate an even better return if you are ready to put in some hard work.</p>
                                </details>
                                <details>
                                <summary style="font-weight:bold;font-size:28px">What kind of stocks should be avoided for investment?  </summary>
                                <p style="color:cyan;font-size:24px;margin-left:30px;margin-top:14px;">The individual should avoid investing in stocks having low liquidity. The low liquidity makes it hard to trade in these stocks. Additionally, finding the data for analysing these companies might be hard as information on public platforms is generally not easily available. Thus, lack of research may result in loss-making investments. Additionally, one should also avoid investing in penny stocks.</p>
                                </details>
                                <details>
                                <summary style="font-weight:bold;font-size:28px"> What is a Rolling Settlement? </summary>
                                <p style="color:cyan;font-size:24px;margin-left:30px;margin-top:14px;">Rolling settlement determines the trading price of each day and settles on a certain day during the settlement period. Currently exchanges follows T+2 rolling settlement cycle. T stands for trading day & 2 stands for another two working days</p>
                                </details>
                            </body>    
                    </html>
                            </body>    
                    </html>
                    """,unsafe_allow_html=True)
                if selected=='Company':
                    st.markdown("""
                    <html>
                        <body>
                            <h4 style="color: red; font-size: 37px;justify-content:center;text-align:center;">What's Trending</h4>
                            <div class="grid-cont" style="margin-top:10px;grid-template-columns:repeat(3,90px);display:grid;grid-auto-rows:38px;grid-gap:12px;justify-content:center;text-align:center;">
                            <div class="grid1" style="background-color:white;color:black;border-radius:11px;text-align:center;margin-top:3px;padding-top:6px;font-weight:bold;text-decoration:none;"><a href="https://www.google.com/finance/quote/ITC:NSE">ITC</a></div>
                            <div class="grid1" style="background-color:white;color:black;border-radius:11px;text-align:center;margin-top:3px;padding-top:6px;font-weight:bold;"><a href="https://www.google.com/finance/quote/RELIANCE:NSE">Reliance</a></div>
                            <div class="grid1" style="background-color:white;color:black;border-radius:11px;text-align:center;margin-top:3px;padding-top:6px;font-weight:bold;"><a href="https://www.google.com/finance/quote/MSFT:NASDAQ">Microsoft</a></div>
                            <div class="grid1" style="background-color:white;color:black;border-radius:11px;text-align:center;margin-top:3px;padding-top:6px;font-weight:bold;"><a href="https://www.google.com/finance/quote/AGRITECH:NSE">Agritech</a></div>
                            <div class="grid1" style="background-color:white;color:black;border-radius:11px;text-align:center;margin-top:3px;padding-top:6px;font-weight:bold;"><a href="https://www.google.com/finance/quote/SBIN:NSE">SBI</a></div>
                            <div class="grid1" style="background-color:white;color:black;border-radius:11px;text-align:center;margin-top:3px;padding-top:6px;font-weight:bold;"><a href="https://www.google.com/finance/quote/AAPL:NASDAQ">Apple</a></div>
                            </div>
                        </body>    
                    </html>
                    """,unsafe_allow_html=True)
                    sea=st.text_input('',placeholder='Enter a company')
                    st.title(f'Details of the {sea}')
                    sym=yf.Ticker(sea)
                    information=pd.Series(sym.info)
                    details=pd.DataFrame(information)
                    x=details.iloc[11,0]
                    st.subheader(x)

                    info,actions,holders,news=st.tabs(['Information','Actions','Holders','News'])
                    with info:
                        df2=details.head(10)
                        df3=details.tail(30)
                        df3=pd.concat([df2,df3],axis=0)
                        st.table(df3.style.set_table_styles(styles))
                    with actions:
                        st.title(':red[Actions]')
                        st.write('In the context of the stock market, the term "actions" is not a commonly used term to refer to specific concepts. It is possible that you might be referring to "transactions" or "trades." Let us clarify these terms:')
                        st.table(sym.actions.head(15).style.set_table_styles(styles))
                        div,spl=st.columns(2)
                        with div:
                            dividend=pd.DataFrame(sym.actions.Dividends)
                            st.metric('Average Dividends',value=dividend.Dividends.mean().round(2))
                            st.line_chart(dividend)
                            st.table(dividend.head(10).style.set_table_styles(styles))
                        with spl:
                            split=pd.DataFrame(sym.actions['Stock Splits'])
                            st.metric('Average splits',value=split['Stock Splits'].mean().round(2))
                            st.line_chart(split)
                            st.table(split.head(10).style.set_table_styles(styles))
                    with holders:
                        st.title(":red[Holders]")
                        st.subheader(f'the holders of the company {sea}')
                        st.table(sym.major_holders.style.set_table_styles(styles))
                        st.subheader(f'The instituational holders of the company {sea}')
                        st.table(sym.institutional_holders.style.set_table_styles(styles))
                    with news:
                                
                        st.title(f":blue[Trending News]")
                        i=0
                        j=0
                        for new in sym.news:    
                            st.subheader(sym.news[i]['title'])
                            image_url=sym.news[i]['thumbnail']['resolutions'][0]['url']
                            try:
                                response = requests.get(image_url)
                                img = Image.open(BytesIO(response.content))
                                st.image(img, caption=sym.news[i]['publisher'], use_column_width=True)
                            except Exception as e:
                                st.error("Error loading the image. Please check the URL and try again.")                
                            st.write(sym.news[i]['link'])
                            i=i+1
                if selected=='Stocks':
                    search=st.text_input('',placeholder='Search for a company')
                    
                    company = yf.download(search, period='1d',interval='1m')
                    
                    t1,t2,t3,t4=st.tabs(['General','Moving Average','Price Change','Intraday Range'])
                    with t1:
                        cl,op,hg,lw=st.columns(4)
                        with cl:
                            st.metric(":cyan[Avg Closing Price]",value=company['Close'].mean().round(2),delta="4%")
                        with op:
                            st.metric("Avg Opening Price",value=company['Open'].mean().round(2),delta="-2%")
                        with hg:
                            st.metric("Avg Highest Price",value=company['High'].mean().round(2),delta="-1%")
                        with lw:
                            st.metric("Avg lowest Price",value=company['Low'].mean(),delta="1%")
                        st.header(f"The stock details of the {search}")
                        st.table(company.head(20).style.set_table_styles(styles))
                        st.title(f'Stock trends of {search}')
                        st.text(f"This is the information regarding the company {search}")
                        fig = go.Figure(data=[go.Candlestick(x=company.index,
                                open=company['Open'],
                                high=company['High'],
                                low=company['Low'],
                                close=company['Close'])])
                        st.plotly_chart(fig)

                    with t2:
                        company['30mins']=company['Close'].rolling(window=30).mean()
                        company['60mins']=company['Close'].rolling(window=60).mean()
                        m30,m60,mc=st.columns(3)
                        with m30:
                            st.metric("30m Avg",value=company['30mins'].mean().round(2))
                        with m60:
                            st.metric("60m Avg",value=company['60mins'].mean().round(2))
                        with mc:
                            st.metric("Days Avg",value=company['Close'].mean().round(2))
                        min30,min60=st.tabs(['30m','60m'])
                        fig=px.line(company,y=['Close'])
                        st.plotly_chart(fig)
                        with min30:
                            st.title('Closing price with Price change 30mins')
                            fig=px.line(company,y=['Close','30mins'])
                            st.plotly_chart(fig)
                        with min60:
                            st.title('Closing price with Price change 60mins')
                            fig=px.line(company,y=['Close','60mins'])
                            st.plotly_chart(fig)
                    with t3:
                        company['PriceChange']=company['Close']-company['Open']
                        mn,ad=st.columns(2)
                        with mn:
                            st.metric('Avg Open',value=company['Open'].mean().round(2),delta='1.1%')
                        with ad:
                            st.metric('Avg Adj Close',value=company['Adj Close'].mean().round(2),delta='-0.1%')
                        mnc,mnp=st.columns(2)
                        with mnc:
                            st.metric("Avg Close",value=company['Close'].mean().round(2),delta='2%')
                        with mnp:
                            st.metric('Avg Price Change',value=company['PriceChange'].mean().round(2),delta='-1.3%')
                        bar_colors = ['green' if val >= 0 else 'red' for val in company['PriceChange']]
                        bar_trace = go.Bar(
                        x=company.index,
                        y=company['PriceChange'],
                        marker=dict(color=bar_colors)
                        )

                        # Create the layout
                        layout = go.Layout(
                            title='Positive and Negative Bar Graph',
                            xaxis=dict(title='Categories'),
                            yaxis=dict(title='Values')
                        )

                        # Create the figure
                        fig = go.Figure(data=[bar_trace], layout=layout)
                        st.plotly_chart(fig)
                        df2 = -company[['Open','Close','Adj Close','PriceChange']]
                        style1 = company[['Open','Close','Adj Close','PriceChange']].style.applymap(color_negative_red)
                        st.table(style1)
                    with t4:
                        company['Intraday_Range'] = company['High'] - company['Low']
                        st.table(company[['Open','Close','Adj Close','Intraday_Range']].head(20).style.set_table_styles(styles))
                        company['GapUp'] = company['Open'] > company['Close'].shift(1)
                        company['GapDown'] = company['Open'] < company['Close'].shift(1)
                        st.title(f'The gapup and gapdown of the company{search}')
                        gup,gdwn=st.columns(2)
                        with gup:
                            
                            st.metric('Avg',company['Intraday_Range'].mean().round(2))
                            st.table(company[['Open', 'Close','Intraday_Range','GapUp']].head(10).style.set_table_styles(styles))
                        with gdwn:
                            st.metric('Avg',company['Intraday_Range'].mean().round(2))
                            st.table(company[['Open', 'Close','Intraday_Range','GapDown']].head(10).style.set_table_styles(styles))

                if selected=='Predict':
                    st.header('This is Predict')
                if selected=='Dashboard':
                    lottie_coding=load_lottiefile("animation_ll4zaxpf.json")
                    lottie_anni=load_lottiefile("animation_ll4z00j3.json")
                    lottie_url='https://lottie.host/0c99d6f8-ab79-43d6-b188-f14713ed7b05/r0xUnkKdpF.json'
                    anni='https://lottie.host/77578782-ff7a-4a54-bd0e-00d0e6629fb4/Z8UI5WKH6x.json'
                    lottie2=load_lottieur(anni)
                    lottie1=load_lottieur(lottie_url)
                    st.markdown("<marquee><h2 style='color:white;'>Stock Market</h2></marquee>",unsafe_allow_html=True)
                    a,b,c=st.columns(3)
                    with a:
                        st.markdown("<br> </br>",unsafe_allow_html=True)
                        st.markdown("<br> </br>",unsafe_allow_html=True)
                        st_lottie(
                            lottie1,
                            loop=True
                        )
                    with b:
                        st.markdown("<br> </br>",unsafe_allow_html=True)
                        st.markdown("<br> </br>",unsafe_allow_html=True)
                        symbol=st.text_input('',placeholder='Search for a Company')
                        start=st.date_input("Start")
                        end=st.date_input("End") 
                    with c:
                        st_lottie(
                                lottie2,
                                loop=True,
                                height=None,
                                width=None
                            )
                    data=stock_data(symbol,start,end)
                    stoc= data.iloc[::-1]
                    stock=stoc[['Open','Close','High','Low','Volume']]
                    st.markdown("<h1 style='color:green;'><center>Stock values</center></h1>",unsafe_allow_html=True)
    
                    c1,c2=st.columns(2)
                    with c1:
                        st.subheader("Opening and Closeing prices")
                        st.table(stock[['Close','Open','Volume']].head())
                        select=option_menu(
                            menu_title='Close Open',
                            orientation='horizontal',
                            options=['1w','2w','1m','3m','6m']
                        )
                        if select=='1w':
                            st.line_chart(stock.iloc[0:8,0:2],y=['Close','Open'])
                        if select=='2w':
                            st.line_chart(stock.iloc[0:15,0:2],y=['Close','Open'])
                        if select=='1m':
                            st.line_chart(stock.iloc[0:31,0:2],y=['Close','Open'])        
                        if select=='3m':
                            st.line_chart(stock.iloc[0:91,0:2],y=['Close','Open'])
                        if select=='6m':
                            st.line_chart(stock.iloc[0:183,0:2],y=['Close','Open'])
                    with c2:
                        st.subheader("Highest and Lowest prices")
                        st.table(stock[['High','Low','Volume']].head())
                        select=option_menu(
                            menu_title='High Low',
                            orientation='horizontal',
                            options=['1w','2w','1m','3m','6m']
                        )    
                        if select=='1w':
                            st.line_chart(stock.iloc[0:8,2:5],y=['High','Low'])
                        if select=='2w':
                            st.line_chart(stock.iloc[0:15,2:5],y=['High','Low'])        
                        if select=='1m':
                            st.line_chart(stock.iloc[0:31,2:5],y=['High','Low'])
                        if select=='3m':
                            st.line_chart(stock.iloc[0:91,2:5],y=['High','Low'])
                        if select=='6m':
                            st.line_chart(stock.iloc[0:183,2:5],y=['High','Low'])
                    plt.figure(figsize=(12,6))
                    fig=px.line(stock)
                    st.plotly_chart(fig)
                
                if selected=='Indicators':
                    st.subheader(':blue[Technical Indicators Analysis]')
                    st.markdown('<h3>Technical Indicator</h3>',unsafe_allow_html=True)
                    st.markdown('<p>A technical indicator is a mathematical calculation or pattern derived from price, volume, or open interest of a security (such as stocks, currencies, commodities, etc.) in financial markets. These indicators are used by traders and analysts to gain insights into the markets trend, momentum, volatility, and potential reversal points. Technical indicators are applied to charts to help traders make more informed decisions about when to buy, sell, or hold a particular security.</p>',unsafe_allow_html=True)
                    symbol=st.text_input('')
                    per=st.selectbox('Period',options=['1d','2d','1w','1mo','3mo','6mo','1y'])
                    inter=st.selectbox('Interval',options=['1d','5d','1wk'])
                    tech=yf.download(symbol,period=per,interval=inter)

                    df=pd.DataFrame()
                    ind_list=df.ta.indicators(as_list=True)
                    technical_indicator=st.selectbox('Tech Indicators',options=ind_list)
                    method=technical_indicator
                    indicator=pd.DataFrame(getattr(ta,method)(low=tech['Low'],close=tech['Close'],high=tech['High'],open=tech['Open'],volume=tech['Volume']))
                    indcl,indop=st.columns(2)
                    with indcl:
                        st.metric(':blue[Closing Price]',value=tech.Close.mean().round(2),delta='1%')
                    with indop:
                        st.metric(':blue[Opening Price]',value=tech.Open.mean().round(2),delta='-3%')
                    indh,indl=st.columns(2)
                    with indh:
                        st.metric(':blue[High Price]',value=tech.High.mean().round(2),delta='-1%')
                    with indl:
                        st.metric(':blue[Lowest Price]',value=tech.Low.mean().round(2),delta='-1.4%')
                    indicator['Close']=tech['Close']
                    fig_ind_new=px.line(indicator)
                    st.plotly_chart(fig_ind_new)
                    st.table(indicator.head(10).style.set_table_styles(styles))
                if selected=='Bot':
                    st.title("ChatGPT-like clone")

                    openai.api_key = st.secrets['OPENAI_API_KEY']

                    if "openai_model" not in st.session_state:
                        st.session_state["openai_model"] = "gpt-3.5-turbo"

                    if "messages" not in st.session_state:
                        st.session_state.messages = []

                    for message in st.session_state.messages:
                        with st.chat_message(message["role"]):
                            st.markdown(message["content"])

                    if prompt := st.chat_input("What is up?"):
                        st.session_state.messages.append({"role": "user", "content": prompt})
                        with st.chat_message("user"):
                            st.markdown(prompt)

                        with st.chat_message("assistant"):
                            message_placeholder = st.empty()
                            full_response = ""
                            for response in openai.ChatCompletion.create(
                                model=st.session_state["openai_model"],
                                messages=[
                                    {"role": m["role"], "content": m["content"]}
                                    for m in st.session_state.messages
                                ],
                                stream=True,
                            ):
                                full_response += response.choices[0].delta.get("content", "")
                                message_placeholder.markdown(full_response + "▌")
                            message_placeholder.markdown(full_response)
                        st.session_state.messages.append({"role": "assistant", "content": full_response})

            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')
except:
    st.success('Refresh Page')
st.markdown('---')
f1,f2,f3,f4=st.columns(4)
with f1:
    st.subheader(':red[Company]')
    st.text('About Us')
    st.text('Services')
    st.text('Privacy Policy')
    st.text('T&c')
with f2:
    st.subheader(':red[Get Help]')
    st.text('FAQ')
    st.text('Return')
    st.text('Stocks')
    st.text('Companies')
with f3:
    st.subheader(':red[Online Trading]')
    st.text('Algorithmic Trading')
    st.text('Upstox Trading')
    st.text('Relaince')
    st.text('TATA')
with f4:
    st.subheader(':red[Connect Us]')
    st.text('Email')
    st.text('FaceBook')
    st.text('LinkedIn')
    st.text('Twitter')
