from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *


#---------------- self define module ----------------
import text_push as text_push
import requests
from pyquery import PyQuery as pq
import datetime
import math
import numpy as np
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import pyimgur
import six
import strategyAndMPT as MPT
def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False
def render_mpl_table(data, col_width=2.0, row_height=1.0, font_size=15,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
    myfont = fm.FontProperties(fname="/app/微軟正黑體.ttf")
    if ax is None:
        size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
        fig, ax = plt.subplots(figsize=size)
        ax.axis('off')
    mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    mpl_table.auto_set_font_size(False)
    for k, cell in  six.iteritems(mpl_table._cells):
        cell.set_edgecolor(edge_color)
        if k[0] == 0 or k[1] < header_columns:
            cell.set_text_props(weight='bold', color='w', fontproperties = myfont)
            cell.set_facecolor(header_color)
        else:
            cell.set_text_props(fontproperties = myfont)
            cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
    mpl_table.set_fontsize(font_size)
    return plt.savefig("table_analysis.png",bbox_inches='tight')

#---------------- end of define module ----------------
def wanwan(user_message):

# 使用說明-----------------------------------------------------------------------------------------------------------
    if user_message == "使用說明":
        output_message = "你好～我是你的理柴小幫手，我的使用說明如下：\n\
    \n\
    1. 填寫風險評估問卷：\n\
    點下填寫風險評估問卷，我會讓你填寫一份問卷，以了解你的風險偏好程度與報酬型態。\n\
    \n\
    2. 智能選股：\n\
    點下智能選股，我會讓你選擇選股指標，並呈現前幾名給你參考。\n\
    \n\
    3. 投資組合建構：\n\
    點下投資組合建構，我會讓你選擇交易策略，最後利用投資組合理論計算出最適權重給你參考。\n\
    \n\
    4. 股票報價：\n\
    點下股票報價，我會提供個股報價與分析，以及更多的功能！\n\
    \n\
    5. 全球行情：\n\
    點下全球行情，我會為你提供即時的台灣加權指數以及全球主要金融市場股價指數的成交行情。\n\
    \n\
    6. 原物料報價：\n\
    點下原物料報價，我會為你提供主要貴金屬與能源的報價行情。\n\
    \n\
    7. 匯率報價：\n\
    點下匯率報價，我會為你提供美元指數以及美元兌新台幣的走勢。\n\
    \n\
    8. 總體經濟指標：\n\
    點下總體經濟指標，我會為你提供美國十年期與兩年期利差、非農數據、VIX走勢以及台美利差走勢。\n\
    \n\
    9. 個股基本面：\n\
    將欲搜尋的股票加入至自選股，點下個股基本面，我會為你提供該個股重要財務比率一覽表。\n\
    \n\
    10. 個股技術分析：\n\
    點下欲搜尋的股票欄位的個股技術分析，我會為你提供KD/RSI/DIF-MACD/DMI/BIAS/均線扣抵等指標，並會將訊號展示在線圖上。\n\
    \n\
    11. 個股籌碼面：\n\
    點下欲搜尋的股票欄位的個股籌碼面，我會為你提供該個股券資狀況以及主力動向。\n\
    \n\
    12. 個股消息面：\n\
    點下欲搜尋的股票欄位的個股消息面，我會為你提供該個股最近的幾則新聞供參考。\n\
    \n\
    13. 指標介紹：\n\
    輸入指標介紹，我會教你怎麼看財務比率以及技術指標，以及其他指標、理論的介紹！"

    # ------------------------------------------------------------------------------------------------------------------

    # 今日行情-----------------------------------------------------------------------------------------------------------
    elif user_message == "全球行情":
        dfIndex = pd.read_csv("全球指數資料庫.csv", encoding = "utf-8")
        dfIndex["漲跌點數"] = [round(i,2)for i in dfIndex["漲跌點數"]]
        dfIndex["漲跌幅(%)"] = [round(i,2)for i in dfIndex["漲跌幅(%)"]]
        render_mpl_table(dfIndex, col_width=3.0)
        CLIENT_ID = "XXXXX"
        index_path = os.path.abspath("table_analysis.png")
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(index_path, title="全球股市行情")
        index_URL = uploaded_image.link
        output_message = index_URL
    # 原物料商品指數行情-----------------------------------------------------------------------------------------------------
    elif user_message == "原物料報價":    
        dfMaterial = pd.read_csv("原物料指數資料庫.csv", encoding = "utf-8")
        render_mpl_table(dfMaterial, col_width=3.0)
        CLIENT_ID = "XXXXX"
        Material_path = os.path.abspath("table_analysis.png")
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(Material_path, title="原物料商品指數報價")
        Material_URL = uploaded_image.link
        output_message = Material_URL
    # 匯率行情----------------------------------------------------------------------------------------------------
    elif user_message == "匯率報價": 
        df = pd.read_csv("匯率資料庫.csv", encoding = "utf-8")
        dfTWDUSD = df[df["匯兌名稱"]=="美元兌台幣"]
        dfUSDI = df[df["匯兌名稱"]=="美元指數"]
        # 畫圖
        myfont = fm.FontProperties(fname='/app/微軟正黑體.ttf')
        plt.subplots(2,1,figsize=(10,10))
        plt.subplot(2,1,1)
        plt.title("匯率行情\n\n美元指數", fontproperties = myfont, fontsize = 15)
        plt.plot(dfUSDI["Close"], "r-", linewidth = 3, label = "美元指數走勢") 
        plt.ylabel("指數", fontproperties = myfont, fontsize = 15)
        plt.legend(prop = myfont, fontsize=15)
        plt.subplot(2,1,2)
        plt.title("美元兑新台幣", fontproperties = myfont, fontsize = 15)
        plt.plot(dfTWDUSD["Close"], "g-", linewidth = 3, label = "美元兌新台幣走勢")
        plt.ylabel("匯價", fontproperties = myfont, fontsize = 15)
        plt.legend(prop = myfont, fontsize=15)
        plt.xlabel("日期", fontproperties = myfont, fontsize = 18)
        plt.legend(prop = myfont, fontsize=15)
        plt.savefig("exchange.jpg")
        # print(os.path.abspath("test.jpg"))

        # 用Imgur API 上傳圖片，並得到圖片網址！
        CLIENT_ID = "XXXXX"
        exchange_path = os.path.abspath("exchange.jpg")
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(exchange_path, title="匯率報價圖")
        exchange_URL = uploaded_image.link
        output_message = exchange_URL
    # ------------------------------------------------------------------------------------------------------------------
    # 總體經濟指標----------------------------------------------------------------------------------------------------
    elif user_message == "總體經濟指標":
        dfUSYD = pd.read_csv("美國10-2利差資料庫.csv", encoding = "utf-8")
        dfNF = pd.read_csv("非農資料庫.csv", encoding = "utf-8")
        dfVIX = pd.read_csv("VIX資料庫.csv", encoding = "utf-8")
        dfTWUSYD = pd.read_csv("台美利差資料庫.csv", encoding = "utf-8")
        # 畫圖
        myfont = fm.FontProperties(fname='/app/微軟正黑體.ttf')
        plt.subplots(4,1,figsize=(10,20))
        plt.subplot(4,1,1)
        plt.title("總體經濟指標\n\n美國10年期-2年期利差", fontproperties = myfont, fontsize = 15)
        plt.plot(dfUSYD["10-2"], "m-", linewidth = 3, label = "美國十年期-兩年期利差")
        plt.ylabel("利差值", fontproperties = myfont, fontsize = 15)
        plt.legend(prop = myfont, fontsize=10)
        plt.subplot(4,1,2)
        plt.title("美國非農數據", fontproperties = myfont, fontsize = 15)
        plt.plot(dfNF["Release Date"], dfNF["Actual"], "y-", linewidth = 3, label = "實際非農數據")
        plt.plot(dfNF["Release Date"], dfNF["Forecast"], "c-", linewidth = 3, label = "預測非農數據")
        plt.ylabel("千為單位", fontproperties = myfont, fontsize = 15)
        plt.legend(prop = myfont, fontsize=15)
        plt.subplot(4,1,3)
        plt.title("VIX走勢圖", fontproperties = myfont, fontsize = 15)
        plt.plot(dfVIX["close"], "r-", linewidth = 3, label = "VIX指數")
        plt.ylabel("VIX值", fontproperties = myfont, fontsize = 15)
        plt.legend(prop = myfont, fontsize=15)
        plt.subplot(4,1,4)
        plt.title("台美十年期利差", fontproperties = myfont, fontsize = 15)
        plt.plot(dfTWUSYD["Date"], dfTWUSYD["Price"], "y-", linewidth = 3, label = "台美十年期公債殖利率")
        plt.ylabel("殖利率值", fontproperties = myfont, fontsize = 15)
        plt.xlabel("日期", fontproperties = myfont, fontsize = 18)
        plt.legend(prop = myfont, fontsize=15)
        plt.savefig("macro.jpg")
        # print(os.path.abspath("test.jpg"))

        # 用Imgur API 上傳圖片，並得到圖片網址！
        CLIENT_ID = "XXXXX"
        macro_path = os.path.abspath("macro.jpg")
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(macro_path, title="總體經濟")
        macro_URL = uploaded_image.link
        #  print(tech_URL)
        output_message = macro_URL
    # ------------------------------------------------------------------------------------------------------------------
    # 以下為股票技術分析-----------------------------------------------------------------------------------------------

    elif "tech" in user_message:
        user_message = user_message.replace("tech","")
        dfTech = pd.read_csv("價量資料庫.csv", encoding = "utf-8")
        dfTech.rename(columns = {"證券代號":"股票代號", "證券名稱":"股票名稱"}, inplace = True)
        dfTech["股票代號"] = [str(i) for i in dfTech["股票代號"]]
        dfTech["證券代碼"] = dfTech["股票代號"] + " " + dfTech["股票名稱"]
        name_dict = {}
        symbol_dict = {}
        StockList = sorted(set(list(dfTech["證券代碼"])))
        for i in StockList:
            name_dict[i.split(" ")[0]] = i.split(" ")[1]
            symbol_dict[i.split(" ")[1]] = i.split(" ")[0]
    # -以下做若使用者用股票名稱輸入(考量未必知股票代碼)，將其轉成股票代碼再去做，若輸錯股票名稱或其餘中文訊息，一律叫他們重新去讀使用說明。-

        if (is_chinese(user_message) == True) or ("KY" in user_message.upper()) or ("DR" in user_message.upper()):
        # 外國設立之公司來台掛牌時股票名稱會附註KY，存託憑證則是會附註DR，若使用者誤輸入小寫，我們也幫他轉成大寫去做查詢。
            try:
                user_message = user_message.upper()
                name = user_message
                stockNum = symbol_dict[name]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票名稱，請再次確認名稱是否正確。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        #  若使用者股票名稱輸錯或是他亂打一些中文詞，告訴他輸錯了或是給他查詢使用說明的方法。
        elif user_message.isalnum() == True:
            stockNum = user_message
            try:
                name = name_dict[stockNum]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票代碼，請再次確認代碼是否正確或直接輸入股票名稱。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        #  若使用者股票代碼輸錯或是他亂打一些英文或數字，告訴他輸錯了或是給他查詢使用說明的方法。
        else:
            stockNum = 0
            output_message = "若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
            
    # 股票技術分析---------------------------------------------------------------------------------------------------

        if stockNum != 0:
            stockFullName = str(stockNum) + " " + name_dict[str(stockNum)]
            if stockFullName in StockList:
                df1 = dfTech[dfTech["證券代碼"]==stockFullName]
                #  均線扣抵
                if list(df1["MA5DIFFE"])[-1] > 0:
                    maSuggest_0 = "新增日收盤價>週線扣抵值，週線趨勢向上。"
                elif list(df1["MA5DIFFE"])[-1] < 0:
                    maSuggest_0 = "新增日收盤價<週線扣抵值，週線趨勢向下。"
                else:
                    maSuggest_0 = "新增日收盤價=週線扣抵值，週線持平。"
                if list(df1["MA20DIFFE"])[-1] > 0:
                    maSuggest_1 = "新增日收盤價>月線扣抵值，月線趨勢向上。"
                elif list(df1["MA20DIFFE"])[-1] < 0:
                    maSuggest_1 = "新增日收盤價<月線扣抵值，月線趨勢向下。"
                else:
                    maSuggest_1 = "新增日收盤價=月線扣抵值，月線持平。"
                if list(df1["MA60DIFFE"])[-1] > 0:
                    maSuggest_2 = "新增日收盤價>季線扣抵值，季線趨勢向上。"
                elif list(df1["MA60DIFFE"])[-1] < 0:
                    maSuggest_2 = "新增日收盤價<季線扣抵值，季線趨勢向下。"
                else:
                    maSuggest_2 = "新增日收盤價=季線扣抵值，季線持平。"
                maSuggest = "*均線扣抵：\n{}\n{}\n{}\n".format(maSuggest_0, maSuggest_1, maSuggest_2)
                
                #  乖離率
                ma6Bias = list(df1["MA6BIAS"])
                ma12Bias = list(df1["MA12BIAS"])
                ma24Bias = list(df1["MA24BIAS"])
                ma72Bias = list(df1["MA72BIAS"])
                
                # KD訊號如下
                if (list(df1["K9"])[-1]>80)&(list(df1["K9"])[-2]>80)&(list(df1["K9"])[-3]>80):
                    kdSuggest_1 = "KD出現高檔鈍化，超買會續漲～"
                elif (list(df1["K9"])[-1]<20)&(list(df1["K9"])[-2]<20)&(list(df1["K9"])[-3]<20):
                    kdSuggest_1 = "KD出現低檔鈍化，超賣會續跌！！！"
                elif list(df1["K9"])[-1]>80:
                    kdSuggest_1 = "KD出現高檔超買訊號，可能會反轉下跌！！！"
                elif list(df1["K9"])[-1]<20:
                    kdSuggest_1 = "KD出現低檔超賣訊號，可能會反彈上漲～"
                else:
                    kdSuggest_1 = ""
                if (list(df1["K9"])[-1]>list(df1["D9"])[-1]) & (list(df1["K9"])[-2]<list(df1["D9"])[-2]):
                    kdSuggest_2 = "KD剛出現黃金交叉，短線上的多頭訊號～"
                elif (list(df1["K9"])[-1]<list(df1["D9"])[-1]) & (list(df1["K9"])[-2]>list(df1["D9"])[-2]):
                    kdSuggest_2 = "KD剛出現死亡交叉，短線上的空頭訊號！！！"
                elif list(df1["K9"])[-1]>list(df1["D9"])[-1]:
                    kdSuggest_2 = "K值大於D值，短線上多方較強勢～"
                elif list(df1["K9"])[-1]<list(df1["D9"])[-1]:
                    kdSuggest_2 = "K值小於D值，短線上空方較強勢！！！"
                elif list(df1["K9"])[-1]==list(df1["D9"])[-1]:
                    kdSuggest_2 = "K線與D線交纏中！！！"
                else:
                    kdSuggest_2 = ""
                kdSuggest = "\n{}\n{}".format(kdSuggest_2, kdSuggest_1)
                
                # RSI訊號如下
                if list(df1["RSI6"])[-1]>80:
                    rsiSuggest_1 = "RSI出現高檔超買訊號，可能會反轉下跌！！！"
                elif list(df1["RSI6"])[-1]<20:
                    rsiSuggest_1 = "RSI出現低檔超賣訊號，可能會反彈上漲～"
                else:
                    rsiSuggest_1 = ""
                if (list(df1["RSI6"])[-1]>list(df1["RSI12"])[-1]) & (list(df1["RSI6"])[-2]<list(df1["RSI12"])[-2]):
                    rsiSuggest_2 = "RSI剛出現黃金交叉，短線上的多頭訊號～"
                elif (list(df1["RSI6"])[-1]<list(df1["RSI12"])[-1]) & (list(df1["RSI6"])[-2]>list(df1["RSI12"])[-2]):
                    rsiSuggest_2 = "RSI剛出現死亡交叉，短線上的空頭訊號！！！"
                elif list(df1["RSI6"])[-1]>list(df1["RSI12"])[-1]:
                    rsiSuggest_2 = "短週期RSI大於長週期RSI，短線上多方較強勢～"
                elif list(df1["RSI6"])[-1]<list(df1["RSI12"])[-1]:
                    rsiSuggest_2 = "短週期RSI小於長週期RSI，短線上空方較強勢！！！"
                else:
                    rsiSuggest_2 = ""
                rsiSuggest = "\n{}\n{}".format(rsiSuggest_2, rsiSuggest_1)
                
                # MACD訊號如下
                if (list(df1["DIF12-26"])[-1]>list(df1["MACD9"])[-1]) & (list(df1["DIF12-26"])[-2]<list(df1["MACD9"])[-2]):
                    macdSuggest = "\nMACD由負翻正，短線上的多頭訊號～"
                elif (list(df1["DIF12-26"])[-1]<list(df1["MACD9"])[-1]) & (list(df1["DIF12-26"])[-2]>list(df1["MACD9"])[-2]):
                    macdSuggest = "\nMACD由正翻負，短線上的空頭訊號！！！"
                elif list(df1["DIF12-26"])[-1]>list(df1["MACD9"])[-1]:
                    macdSuggest = "\nDIF線在MACD線之上，短線上多方較強勢～"
                elif list(df1["DIF12-26"])[-1]<list(df1["MACD9"])[-1]:
                    macdSuggest = "\nDIF線在MACD線之下，短線上空方較強勢！！！"
                else:
                    macdSuggest = ""
                    
                # 視覺化             
                if list(df1["收盤價"])[-1] < 10:
                    spread = 0.01
                elif list(df1["收盤價"])[-1] < 50:
                    spread = 0.05
                elif list(df1["收盤價"])[-1] < 100:
                    spread = 0.1
                elif list(df1["收盤價"])[-1] < 500:
                    spread = 0.5
                elif list(df1["收盤價"])[-1] < 1000:
                    spread = 1
                else:
                    spread = 5
                    
                datesList = [i.split("/")[1]+"/"+i.split("/")[2] for i in df1["年月日"]][-1:-13:-1][::-1]
                ma6BiasList = list(df1["MA6BIAS"])[-1:-13:-1][::-1]
                ma12BiasList = list(df1["MA12BIAS"])[-1:-13:-1][::-1]
                ma24BiasList = list(df1["MA24BIAS"])[-1:-13:-1][::-1]
                ma72BiasList = list(df1["MA72BIAS"])[-1:-13:-1][::-1]
                K9List = list(df1["K9"])[-1:-13:-1][::-1]
                D9List = list(df1["D9"])[-1:-13:-1][::-1]
                RSI6List = list(df1["RSI6"])[-1:-13:-1][::-1]
                RSI12List = list(df1["RSI12"])[-1:-13:-1][::-1]
                DIFList = list(df1["DIF12-26"])[-1:-13:-1][::-1]
                MACDList = list(df1["MACD9"])[-1:-13:-1][::-1]
                PositiveDI14List = list(df1["PositiveDI14"])[-1:-13:-1][::-1]
                NegativeDI14List = list(df1["NegativeDI14"])[-1:-13:-1][::-1]
                ADXList = list(df1["ADX"])[-1:-13:-1][::-1]
                # 畫圖
                myfont = fm.FontProperties(fname='/app/微軟正黑體.ttf')
                plt.subplots(5,1,figsize=(10,20))
                plt.subplot(5,1,1)
                plt.title("{}({}) 技術分析結果\n\n乖離率".format(name_dict[stockNum], stockNum), fontproperties = myfont, fontsize = 15)
                plt.plot(datesList, ma6BiasList, "r-", linewidth = 3, label = "六日乖離線") 
                plt.plot(datesList, ma12BiasList, "g-", linewidth = 3, label = "十二日乖離線")
                plt.plot(datesList, ma24BiasList, "b-", linewidth = 3, label = "二十四日乖離線")
                plt.plot(datesList, ma72BiasList, "m-", linewidth = 3, label = "七十二日乖離線")
                plt.ylabel("乖離率", fontproperties = myfont, fontsize = 15)
                plt.yticks(np.arange(0.5 * min(ma24BiasList), 1.5 * max(ma24BiasList),  0.01))
                plt.legend(prop = myfont, fontsize=10)
                plt.subplot(5,1,2)
                plt.title("九日KD線圖", fontproperties = myfont, fontsize = 15)
                plt.plot(datesList, K9List, "y-", linewidth = 3, label = "K線")
                plt.plot(datesList, D9List, "c-", linewidth = 3, label = "D線")
                plt.ylabel("KD值", fontproperties = myfont, fontsize = 15)
                plt.yticks(np.arange(min(K9List), max(K9List)+1, 3.0))
                plt.text(datesList[-7],0.9* min(K9List),"*KD訊號：{}".format(kdSuggest), fontproperties = myfont, fontsize = 16)
                plt.legend(prop = myfont, fontsize=15)
                plt.subplot(5,1,3)
                plt.title("六日&十二日RSI線圖", fontproperties = myfont, fontsize = 15)
                plt.plot(datesList, RSI6List, "r-", linewidth = 3, label = "六日RSI")
                plt.plot(datesList, RSI12List, "g-", linewidth = 3, label = "十二日RSI")
                plt.ylabel("RSI值", fontproperties = myfont, fontsize = 15)
                plt.yticks(np.arange(min(RSI6List), max(RSI6List)+1, 2.0))
                plt.text(datesList[-7],0.9* min(RSI6List),"*RSI訊號：{}".format(rsiSuggest), fontproperties = myfont, fontsize = 16)
                plt.legend(prop = myfont, fontsize=15)
                plt.subplot(5,1,4)
                plt.title("DIF-MACD線圖", fontproperties = myfont, fontsize = 15)
                plt.plot(datesList, DIFList, "y-", linewidth = 3, label = "DIF線")
                plt.plot(datesList, MACDList, "c-", linewidth = 3, label = "MACD線")
                plt.ylabel("DIF-MACD值", fontproperties = myfont, fontsize = 15)
                plt.yticks(np.arange(min(MACDList), max(MACDList), -1.0))
                plt.text(datesList[-7],0.975* min(DIFList),"*MACD訊號：{}".format(macdSuggest), fontproperties = myfont, fontsize = 16)
                plt.legend(prop = myfont, fontsize=15)
                plt.subplot(5,1,5)
                plt.title("DMI線圖", fontproperties = myfont, fontsize = 15)
                plt.plot(datesList, PositiveDI14List, "y-", linewidth = 3, label = "+DI14")
                plt.plot(datesList, NegativeDI14List, "c-", linewidth = 3, label = "-DI14")
                plt.plot(datesList, ADXList, "r-", linewidth = 3, label = "ADX")
                plt.ylabel("DI14-ADX值", fontproperties = myfont, fontsize = 15)
                plt.yticks(np.arange(min(ADXList), max(ADXList), -1.0))
                plt.xlabel("日期", fontproperties = myfont, fontsize = 18)
                plt.legend(prop = myfont, fontsize=15)
                plt.savefig("stock_Tech.jpg")
                # print(os.path.abspath("test.jpg"))

                # 用Imgur API 上傳圖片，並得到圖片網址！
                CLIENT_ID = "XXXXX"
                tech_path = os.path.abspath("stock_Tech.jpg")
                im = pyimgur.Imgur(CLIENT_ID)
                uploaded_image = im.upload_image(tech_path, title="技術分析圖")
                tech_URL = uploaded_image.link
                #  print(tech_URL)
                output_message = tech_URL
                
    # 以下為基本面分析
    # -----------------------------------------------------------------------------------------------------------------
    elif "fund" in user_message:
        user_message = user_message.replace("fund","")
        dfFund = pd.read_csv("財報資料庫.csv", encoding = "utf-8")
        dfTech = pd.read_csv("價量資料庫.csv", encoding = "utf-8")
        dfTech.rename(columns = {"證券代號":"股票代號", "證券名稱":"股票名稱"}, inplace = True)
        dfTech["股票代號"] = [str(i) for i in dfTech["股票代號"]]
        dfTech["證券代碼"] = dfTech["股票代號"] + " " + dfTech["股票名稱"]
        name_dict = {}
        symbol_dict = {}
        StockList = sorted(set(list(dfTech["證券代碼"])))
        for i in StockList:
            name_dict[i.split(" ")[0]] = i.split(" ")[1]
            symbol_dict[i.split(" ")[1]] = i.split(" ")[0]
        if (is_chinese(user_message) == True) or ("KY" in user_message.upper()) or ("DR" in user_message.upper()):
            try:
                user_message = user_message.upper()
                name = user_message
                stockNum = symbol_dict[name]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票名稱，請再次確認名稱是否正確。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        elif user_message.isalnum() == True:
            stockNum = user_message
            try:
                name = name_dict[stockNum]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票代碼，請再次確認代碼是否正確或直接輸入股票名稱。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        else:
            stockNum = 0
            output_message = "若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        if stockNum != 0:
            dfFund = dfFund[dfFund["股票代號"] == int(stockNum)]
            dfFund.drop(index=dfFund.index[0:4],inplace=True)
            df_fund = pd.DataFrame()
            df_fund[" "] = ['資產總額(百萬元)', '負債總額(百萬元)', '權益總額(百萬元)',
                   '每股參考淨值', '單季EPS', '單季營收(百萬元)', '單季毛利率(%)', '單季營業利益率(%)', '單季稅後純益率(%)',
                   '營收年增率(%)', '每股盈餘年增率(%)', 'ROE(%)', 'ROE年增率(%)', '毛利率季增率(%)',
                   '營業利益年增率(%)', '稅後純益年增率(%)', '負債佔資產比(%)']
            df_fund[str(dfFund.values[0][2])+" Q"+str(dfFund.values[0][3])] = dfFund.values[0][4::]
            df_fund[str(dfFund.values[1][2])+" Q"+str(dfFund.values[1][3])] = dfFund.values[1][4::]
            df_fund[str(dfFund.values[2][2])+" Q"+str(dfFund.values[2][3])] = dfFund.values[2][4::]
            df_fund[str(dfFund.values[3][2])+" Q"+str(dfFund.values[3][3])] = dfFund.values[3][4::]
            df_fund["107 Q4"] = [round(i,2) for i in df_fund["107 Q4"]]
            df_fund["108 Q1"] = [round(i,2) for i in df_fund["108 Q1"]]
            df_fund["108 Q2"] = [round(i,2) for i in df_fund["108 Q2"]]
            df_fund["108 Q3"] = [round(i,2) for i in df_fund["108 Q3"]]
            render_mpl_table(df_fund, col_width=3.0)
            CLIENT_ID = "XXXXX"
            fund_path = os.path.abspath("table_analysis.png")
            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image(fund_path, title="個股財務比率表")
            fund_URL = uploaded_image.link
            output_message = fund_URL
    # 以下為籌碼面分析
    # -----------------------------------------------------------------------------------------------------------------
    elif "chip" in user_message:
        user_message = user_message.replace("chip","")
        dfChip = pd.read_csv("理柴汪汪籌碼資料庫.csv", encoding = "utf-8")
        dfTech = pd.read_csv("理柴汪汪價量資料庫.csv", encoding = "utf-8")
        dfTech.rename(columns = {"證券代號":"股票代號", "證券名稱":"股票名稱"}, inplace = True)
        dfTech["股票代號"] = [str(i) for i in dfTech["股票代號"]]
        dfTech["證券代碼"] = dfTech["股票代號"] + " " + dfTech["股票名稱"]
        name_dict = {}
        symbol_dict = {}
        StockList = sorted(set(list(dfTech["證券代碼"])))
        for i in StockList:
            name_dict[i.split(" ")[0]] = i.split(" ")[1]
            symbol_dict[i.split(" ")[1]] = i.split(" ")[0]
        if (is_chinese(user_message) == True) or ("KY" in user_message.upper()) or ("DR" in user_message.upper()):
            try:
                user_message = user_message.upper()
                name = user_message
                stockNum = symbol_dict[name]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票名稱，請再次確認名稱是否正確。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        elif user_message.isalnum() == True:
            stockNum = user_message
            try:
                name = name_dict[stockNum]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票代碼，請再次確認代碼是否正確或直接輸入股票名稱。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        else:
            stockNum = 0
            output_message = "若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        if stockNum != 0:
            dfChip = dfChip[dfChip["股票代號"] == int(stockNum)]
            dfChip.rename(columns = {'外陸資買賣超股數(不含外資自營商)':"外陸資買賣超",'外資自營商買賣超股數':"外資自營買賣超",'投信買賣超股數':"投信買賣超",
                                    '自營商買賣超股數(自行買賣)':"自營商買賣超(自營)","自營商買賣超股數(避險)":"自營商買賣超(避險)","三大法人合計買賣超":"三大法人合計"} ,inplace = True)
            dfChip = dfChip[["外陸資買賣超","外資自營買賣超","投信買賣超","自營商買賣超(自營)","自營商買賣超(避險)","三大法人合計",
                            "今日資餘","資增","今日券餘","券增","券資比(%)","日期"]]
            dfChip.reset_index(drop = True, inplace = True)
            df_chip = pd.DataFrame()
            df_chip[" "] = ['外陸資買賣超', '外資自營買賣超', '投信買賣超', '自營商買賣超(自營)', '自營商買賣超(避險)', '三大法人合計',
                   '今日資餘', '資增', '今日券餘', '券增', '券資比(%)']
            df_chip[str(dfChip["日期"][0])] = dfChip.values[0][0:11]
            df_chip[str(dfChip["日期"][1])] = dfChip.values[1][0:11]
            df_chip[str(dfChip["日期"][2])] = dfChip.values[2][0:11]
            df_chip[str(dfChip["日期"][3])] = dfChip.values[3][0:11]
            df_chip[str(dfChip["日期"][4])] = dfChip.values[4][0:11]
            render_mpl_table(df_chip, header_columns=0, col_width=2.0,font_size=17)
            CLIENT_ID = "XXXXX"
            chip_path = os.path.abspath("table_analysis.png")
            im = pyimgur.Imgur(CLIENT_ID)
            uploaded_image = im.upload_image(chip_path, title="三大法人近五日個股買賣超/券資比")
            chip_URL = uploaded_image.link
            output_message = chip_URL
    # 以下為消息面分析
    # -----------------------------------------------------------------------------------------------------------------
    elif "news" in user_message:
        user_message = user_message.replace("news","")
        dfTech = pd.read_csv("理柴汪汪價量資料庫.csv", encoding = "utf-8")
        dfTech.rename(columns = {"證券代號":"股票代號", "證券名稱":"股票名稱"}, inplace = True)
        dfTech["股票代號"] = [str(i) for i in dfTech["股票代號"]]
        dfTech["證券代碼"] = dfTech["股票代號"] + " " + dfTech["股票名稱"]
        name_dict = {}
        symbol_dict = {}
        StockList = sorted(set(list(dfTech["證券代碼"])))
        for i in StockList:
            name_dict[i.split(" ")[0]] = i.split(" ")[1]
            symbol_dict[i.split(" ")[1]] = i.split(" ")[0]
        if (is_chinese(user_message) == True) or ("KY" in user_message.upper()) or ("DR" in user_message.upper()):
            try:
                user_message = user_message.upper()
                name = user_message
                stockNum = symbol_dict[name]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票名稱，請再次確認名稱是否正確。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        elif user_message.isalnum() == True:
            stockNum = user_message
            try:
                name = name_dict[stockNum]
            except KeyError:
                stockNum = 0
                output_message = "查無此股票代碼，請再次確認代碼是否正確或直接輸入股票名稱。\n若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        else:
            stockNum = 0
            output_message = "若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
        if stockNum != 0:
            response_news = requests.get("https://tw.stock.yahoo.com/q/h?s={}".format(stockNum))
            doc_news = pq(response_news.text)
            name = doc_news("body > center > table:nth-child(10) > tbody > tr > td:nth-child(1) > table:nth-child(3) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody").text()
            headlineList = name.replace("•","1").split("\n")[1::3]
            mediaList = name.replace("•","1").split("\n")[2::3]
            hrefList = []
            doc_news.make_links_absolute(base_url=response_news.url)
            for eachCate in doc_news("body > center > table:nth-child(10) > tbody > tr > td:nth-child(1) > table:nth-child(3) > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr:nth-child(n+2) > td:nth-child(2) > a").items():
                hrefList.append(eachCate.attr("href"))
            output_message = "*{}({})新聞連結：\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}\n{}\n\n{}\n{}\n{}"\
            .format(name_dict[stockNum], stockNum, headlineList[0],mediaList[0],hrefList[0], headlineList[1],mediaList[1],hrefList[1]\
            , headlineList[2],mediaList[2],hrefList[2], headlineList[3],mediaList[3],hrefList[3], headlineList[4],mediaList[4],hrefList[4]\
            , headlineList[5],mediaList[5],hrefList[5], headlineList[6],mediaList[6],hrefList[6], headlineList[7],mediaList[7],hrefList[7]\
            , headlineList[8],mediaList[8],hrefList[8])
            print(len(output_message))
    elif user_message=="指標介紹":
        output_message="*指標介紹如下：\n\n{}".format("https://docs.google.com/document/d/e/2PACX-1vQ48la9uYwEagfHYt_JewFHjnG1cNLljTyRoYyzDvD2UgchFzAYYt2VbQeWLxZN8SD__S5RLm7-JRLq/pub")
    elif user_message=="個股報價與分析":
        dfIndex = pd.read_csv("全球指數資料庫.csv", encoding = "utf-8")
        indexPrice = str(dfIndex.values[0][5])
        indexRate = str(round(dfIndex.values[0][6],2)) + " (" + str(dfIndex.values[0][7]) + "%)"
        output_message = [indexPrice, indexRate]
    elif "add" in user_message:
        user_message = user_message.replace("add","")
        df = pd.read_csv("價量資料庫.csv", encoding = "utf-8")
        df["證券代號"] = [str(i) for i in df["股票代號"]]
        df = df[df["證券代號"]==user_message]
        df.reset_index(drop = True, inplace = True)
        stockName = df.values[-1][0]
        stockPrice = str(df.values[-1][5])
        stockRate = df.values[-1][7] + " (" + str(df.values[-1][8]) + "%)"
        output_message = [stockName, stockPrice, stockRate]
    elif user_message == "KD黃金交叉&RSI黃金交叉&OSC負翻正":
        output_message = MPT.smartChoseStock(user_message)[0]
    #基本面智能選股
    elif user_message == "營收年增率前五高":
        output_message = MPT.smartChoseStock(user_message)[0]
    elif user_message == "ROE前五高":
        output_message = MPT.smartChoseStock(user_message)[0]
    elif user_message == "EPS年增率前五高":
        output_message = MPT.smartChoseStock(user_message)[0]
    #籌碼面智能選股
    elif user_message == "投信近一日買超前五":
        output_message = MPT.smartChoseStock(user_message)[0]
    elif user_message == "券資比前五":
        output_message = MPT.smartChoseStock(user_message)[0]
    elif user_message == "三大法人合計前五":
        output_message = MPT.smartChoseStock(user_message)[0]
    elif user_message == "KD黃金交叉&RSI黃金交叉&OSC負翻正_MPT建構投資組合":
        inline = user_message.split("_")[0]
        output_message = MPT.MarkowitzPortfolioTheory(MPT.smartChoseStock(inline)[0], MPT.smartChoseStock(inline)[1])
    elif user_message == "營收年增率前五高_MPT建構投資組合":
        inline = user_message.split("_")[0]
        output_message = MPT.MarkowitzPortfolioTheory(MPT.smartChoseStock(inline)[0], MPT.smartChoseStock(inline)[1])
    elif user_message == "ROE前五高_MPT建構投資組合":
        inline = user_message.split("_")[0]
        output_message = MPT.MarkowitzPortfolioTheory(MPT.smartChoseStock(inline)[0], MPT.smartChoseStock(inline)[1])
    elif user_message == "EPS年增率前五高_MPT建構投資組合":
        inline = user_message.split("_")[0]
        output_message = MPT.MarkowitzPortfolioTheory(MPT.smartChoseStock(inline)[0], MPT.smartChoseStock(inline)[1])
    elif user_message == "投信近一日買超前五_MPT建構投資組合":
        inline = user_message.split("_")[0]
        output_message = MPT.MarkowitzPortfolioTheory(MPT.smartChoseStock(inline)[0], MPT.smartChoseStock(inline)[1])
    elif user_message == "券資比前五_MPT建構投資組合":
        inline = user_message.split("_")[0]
        output_message = MPT.MarkowitzPortfolioTheory(MPT.smartChoseStock(inline)[0], MPT.smartChoseStock(inline)[1])
    elif user_message == "三大法人合計前五_MPT建構投資組合":
        inline = user_message.split("_")[0]
        output_message = MPT.MarkowitzPortfolioTheory(MPT.smartChoseStock(inline)[0], MPT.smartChoseStock(inline)[1])
    else:
        output_message="若不清楚使用方法，請輸入「使用說明」，謝謝(´・ω・`)"
    # reply--------------------------------------------------------------------------------------------------------------
    return output_message