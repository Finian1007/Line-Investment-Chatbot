#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import pyimgur

def fillData(SecurityWanted, dfTech):
    # 補齊因為成交量為零，導致資料長度不同的情形
    tool = []
    for i in SecurityWanted:
        tool.append(dfTech[dfTech["股票代號"] == i])
    df = pd.concat(tool)
    date = sorted(set(df["年月日"].tolist()))
    for i in date:
        df_dailychecker = df[df["年月日"]==i]
        if len(df_dailychecker) < len(SecurityWanted):
            difference = list(set(SecurityWanted) - set(df_dailychecker["股票代號"].tolist()))
            for j in difference:
                df.loc[len(df)] = 0
                df["股票代號"][len(df)-1] = j
                df["年月日"][len(df)-1] = i
    df = df.sort_values(by = ["股票代號", "年月日"])
    df.reset_index(drop = True, inplace = True)
    # df為我們挑選出的股票之最近的資料，用來幫助最後的Markowitz Portfolio Theory
    return df

def MarkowitzPortfolioTheory(SecurityWanted, df_DataforMarkowitz, ImgurCLIENT_ID="XXXXX"):
    """
    You have to replace "XXXXX" into your Imgur API CLIENT_ID. Otherwise, this function will be error due to "XXXXX"!
    """
    n = len(SecurityWanted)
    m = 1
    a = np.random.dirichlet(np.ones(n), size = 100000) * m
    # where n is the number of random numbers you want to generate, m is the sum of the resulting array, and size is numbers of array you'd like to generate.
    # This approach produces positive values and is particularly useful for generating valid probabilities that sum to 1.

    # Average Return for each security we have chosen is used to estimate expected return, save these estimators into a list.
    listForReturns = []
    Estimators = []
    interval = int(len(df_DataforMarkowitz)/len(SecurityWanted))
    for i in range(len(SecurityWanted)):
        listForReturns.append(df_DataforMarkowitz["報酬率"][i * interval:(i+1) * interval].tolist())
        averageReturn = df_DataforMarkowitz["報酬率"][i * interval:(i+1) * interval].mean()
        Estimators.append(averageReturn)

    # Covariance Matrix (Sample Covariance Matrix)
    covMatrix = np.cov(np.array(listForReturns), bias=False)

    # Doing Monte Carlo Simulations base on 100,000 arrays we've generated at the begining.
    portfolioReturn = []
    portfolioVariance = []
    for i in range(100000):
        portfolioReturnValue = 0
        for j in range(len(SecurityWanted)):
            portfolioReturnValue += a[i][j] * Estimators[j]
        portfolioVarianceValue = a[i]@covMatrix@a[i].reshape((-1,1))
        portfolioReturn.append(portfolioReturnValue)
        portfolioVariance.append(portfolioVarianceValue)

    # Finding one portfolio which has largest Sharpe Ratio.
    df_Sharpe = pd.DataFrame()
    df_Sharpe["portfolioReturn"] = portfolioReturn
    df_Sharpe["portfolioSD"] = [i**0.5 for i in portfolioVariance]
    df_Sharpe["SharpeRatio(Omit risk-free rate)"] = df_Sharpe["portfolioReturn"]/df_Sharpe["portfolioSD"]
    maximum = max(df_Sharpe["SharpeRatio(Omit risk-free rate)"].tolist())
    maxSharpeIndex = df_Sharpe["SharpeRatio(Omit risk-free rate)"].tolist().index(maximum)
    portfolioReturnMAXSHARPE = portfolioReturn[maxSharpeIndex]
    portfolioVarianceMAXSHARPE = portfolioVariance[maxSharpeIndex]
    MAXSharpeWeight = [round(i,4) for i in list(a[maxSharpeIndex])]

    # Plot, and you'll see Efficient Frontier.
    plt.scatter(portfolioVariance, portfolioReturn)
    plt.scatter(portfolioVarianceMAXSHARPE, portfolioReturnMAXSHARPE, label='MAX Sharpe Ratio', marker='^', c='r', s = 150)
    plt.title("Monte Carlo Simulation")
    plt.xlabel("Daily-Return Variance")
    plt.ylabel("Daily-Return")
    word = ""
    for i in range(len(MAXSharpeWeight)):
        word += (str(SecurityWanted[i]) + ":" + str(MAXSharpeWeight[i] * 100) + "%   ")
    plt.text(portfolioVariance[0],0.95*min(portfolioReturn), word, fontsize = 10)
    plt.legend()
    plt.savefig("Monte Carlo Simulation.png")

    #上傳API, 得到回傳的URL
    CLIENT_ID = ImgurCLIENT_ID
    path = os.path.abspath("Monte Carlo Simulation.png")
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(path, title="Monte Carlo Simulation for EF")
    URL = uploaded_image.link
    return URL

def smartChoseStock(strategy):
    #技術面智能選股
    dfTech = pd.read_csv("價量資料庫.csv", encoding = "utf-8")
    dfTech.rename(columns = {"證券代號":"股票代號", "證券名稱":"股票名稱"}, inplace = True)
    if strategy == "KD黃金交叉&RSI黃金交叉&OSC負翻正":
        df1 = pd.concat([dfTech[dfTech["年月日"] == dfTech["年月日"].tolist()[-2]],dfTech[dfTech["年月日"] == dfTech["年月日"].tolist()[-1]]], ignore_index=True, sort=False)
        intervalDict = {}
        remove = []
        for key in df1['股票代號']:
            intervalDict[key] = intervalDict.get(key,0) + 1
        for i in intervalDict:
            if intervalDict[i] == 1:
                remove.append(df1[df1["股票代號"]==i].index.tolist()[-1])
        df1.drop(index=remove,inplace=True)
        df1 = df1.sort_values(by = ["股票代號", "年月日"])
        df1.reset_index(drop = True, inplace = True)
        df1["KDSign"] = df1["K9"] - df1["D9"]
        df1["RSISign"] = df1["RSI6"] - df1["RSI12"]
        SecurityWanted = []
        for i in range(int(len(df1)/2)):
            a = 2 * i
            if df1["KDSign"][a] < 0:
                if df1["KDSign"][a+1] > 0:
                    if df1["RSISign"][a] < 0:
                        if df1["RSISign"][a+1] > 0:
                            if df1["OSC"][a] < 0:
                                if df1["OSC"][a+1] > 0:
                                    SecurityWanted.append(df1["股票代號"][a])
        volumeList = []
        for i in SecurityWanted:
            volumeList.append((i, df1["成交量"][df1["股票代號"].tolist().index(i)+1], df1["成交量"][df1["股票代號"].tolist().index(i)+1] > df1["成交量"][df1["股票代號"].tolist().index(i)]))
        def takeSecond(element):
            return element[1]
        volumeList.sort(key = takeSecond, reverse = True)
        SecurityWanted = [i[0] for i in volumeList]
        if len(SecurityWanted) > 5:
            SecurityWanted = SecurityWanted[0:5]
        else:
             SecurityWanted = SecurityWanted
        df_DataforMarkowitz = fillData(SecurityWanted, dfTech)
        return (SecurityWanted, df_DataforMarkowitz)

    #基本面智能選股
    elif strategy == "營收年增率前五高":
        dfFund = pd.read_csv("財報資料庫.csv", encoding = "utf-8")
        df1 = dfFund[dfFund["年度"]==sorted(set(dfFund["年度"].tolist()))[-1]]
        df1 = df1[df1["季度"]==sorted(set(df1["季度"].tolist()))[-1]].sort_values(by = ["營收年增率(%)"],ascending=False)
        securityList = df1["股票代號"].tolist()
        SecurityWanted = []
        for i in securityList:
            df_checkFund = dfFund[dfFund["股票代號"]==i]
            checkFundList = df_checkFund["營收年增率(%)"].tolist()[-1:-5:-1]
            if len(SecurityWanted) < 5:
                if min(checkFundList) > 0:
                    SecurityWanted.append(i)
                else:
                    continue
        df_DataforMarkowitz = fillData(SecurityWanted, dfTech)
        return (SecurityWanted, df_DataforMarkowitz)
        
    elif user_message == "ROE前五高":
        dfFund = pd.read_csv("財報資料庫.csv", encoding = "utf-8")
        df1 = dfFund[dfFund["年度"]==sorted(set(dfFund["年度"].tolist()))[-1]]
        df1 = df1[df1["季度"]==sorted(set(df1["季度"].tolist()))[-1]].sort_values(by = ["ROE(%)"],ascending=False)
        securityList = df1["股票代號"].tolist()
        SecurityWanted = []
        for i in securityList:
            df_checkFund = dfFund[dfFund["股票代號"]==i]
            checkFundList = df_checkFund["ROE(%)"].tolist()[-1:-5:-1]
            if len(SecurityWanted) < 5:
                if min(checkFundList) > 0:
                    SecurityWanted.append(i)
                else:
                    continue
        df_DataforMarkowitz = fillData(SecurityWanted, dfTech)
        return (SecurityWanted, df_DataforMarkowitz)

    elif user_message == "EPS年增率前五高":
        SecurityWanted = [str(i) for i in dfFund["股票代號"]][7:12]
        dfFund = pd.read_csv("財報資料庫.csv", encoding = "utf-8")
        df1 = dfFund[dfFund["年度"]==sorted(set(dfFund["年度"].tolist()))[-1]]
        df1 = df1[df1["季度"]==sorted(set(df1["季度"].tolist()))[-1]].sort_values(by = ["每股盈餘年增率(%)"],ascending=False)
        securityList = df1["股票代號"].tolist()
        SecurityWanted = []
        for i in securityList:
            df_checkFund = dfFund[dfFund["股票代號"]==i]
            checkFundList = df_checkFund["每股盈餘年增率(%)"].tolist()[-1:-5:-1]
            if len(SecurityWanted) < 5:
                if max(checkFundList) > 1000:
                    continue
                elif min(checkFundList) > 0:
                    SecurityWanted.append(i)
                else:
                    continue
        df_DataforMarkowitz = fillData(SecurityWanted, dfTech)
        return (SecurityWanted, df_DataforMarkowitz)

    #籌碼面智能選股
    elif user_message == "投信近一日買超前五":
        dfChip = pd.read_csv("籌碼資料庫.csv", encoding = "utf-8")
        dfChip["投信買賣超股數"] = [(int(str(i).replace(",",""))/1000) for i in dfChip["投信買賣超股數"]]
        dfChip = dfChip[dfChip["日期"]==sorted(set(dfChip["日期"].tolist()))[-1]].sort_values(by =["投信買賣超股數"] ,ascending=False)
        SecurityWanted = [i for i in dfChip["股票代號"]][0:5]
        df_DataforMarkowitz = fillData(SecurityWanted, dfTech)
        return (SecurityWanted, df_DataforMarkowitz)
        
    elif user_message == "券資比前五":
        dfChip = pd.read_csv("籌碼資料庫.csv", encoding = "utf-8")
        dfChip = dfChip[dfChip["日期"]==sorted(set(dfChip["日期"].tolist()))[-1]].sort_values(by =["券資比(%)"] ,ascending=False)
        SecurityWanted = [i for i in dfChip["股票代號"]][0:5]
        df_DataforMarkowitz = fillData(SecurityWanted, dfTech)
        return (SecurityWanted, df_DataforMarkowitz)
        
    elif user_message == "三大法人合計前五":
        dfChip = pd.read_csv("籌碼資料庫.csv", encoding = "utf-8")
        dfChip["三大法人合計買賣超"] = [(int(str(i).replace(",",""))/1000) for i in dfChip["三大法人合計買賣超"]]
        dfChip = dfChip[dfChip["日期"]==sorted(set(dfChip["日期"].tolist()))[-1]].sort_values(by =["三大法人合計買賣超"] ,ascending=False)
        SecurityWanted = [i for i in dfChip["股票代號"]][0:5]
        df_DataforMarkowitz = fillData(SecurityWanted, dfTech)
        return (SecurityWanted, df_DataforMarkowitz)

