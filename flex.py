# greeting message
greet = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "理財汪汪",
        "weight": "bold",
        "color": "#1DB446",
        "size": "sm"
      },
      {
        "type": "text",
        "text": "哈囉～我是理財汪汪🐶",
        "weight": "bold",
        "size": "lg",
        "margin": "md"
      },
      {
        "type": "text",
        "text": "你的理財小幫手！汪汪汪！",
        "weight": "bold",
        "size": "lg",
        "margin": "md"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "使用說明",
          "text": "使用說明"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "uri",
          "label": "指標介紹",
          "uri": "https://docs.google.com/document/d/e/2PACX-1vQ48la9uYwEagfHYt_JewFHjnG1cNLljTyRoYyzDvD2UgchFzAYYt2VbQeWLxZN8SD__S5RLm7-JRLq/pub"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "個股報價與分析",
          "text": "個股報價與分析"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "填寫風險評估問卷",
          "text": "風險評估問券"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "智能選股",
          "text": "智能選股"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "投資組合建構",
          "text": "投資組合建構"
        }
      }
    ]
  }
}
###############################################################
# empty carousel
stocks = []
mode = ''
hasInited = False
isStart = True
def initStock(indexPrice, indexRate):
    # 匯入的值要是str
    red = "#D50001"
    green = "#00C000"

    if indexRate[0] == '+':
        color = red
    if indexRate[0] == '-':
        color = green

    index = {
        "type": "bubble",
        "size": "mega",
        "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": "加權指數",
                "color": color,
                "size": "3xl",
                "flex": 4,
                "weight": "bold"
                }
            ]
            },
            {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": indexPrice,
                "color": color,
                "size": "xxl",
                "weight": "bold"
                },
                {
                "type": "text",
                "text": indexRate,
                "color": color,
                "size": "md",
                "flex": 4
                }
            ]
            }
        ],
        "paddingAll": "20px",
        "backgroundColor": "#000000",
        "spacing": "md",
        "height": "154px",
        "paddingTop": "22px"
        },
        "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
            {
            "type": "button",
            "height": "sm",
            "style": "link",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "全球行情",
                "text": "全球行情"
            }
            },
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "原物料報價",
                "text": "原物料報價"
            }
            },
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "匯率報價",
                "text": "匯率報價"
            }
            },
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "總體經濟指標",
                "text": "總體經濟指標"
            }
            },
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "新增自選股",
                "text": "新增自選股"
            }
            }
        ]
        }
    }
    global hasInited, stocks
    hasInited = True
    stocks.append(index)



# sample stock bubble
    #index sample  
def appendStock(stockName, stockPrice, stockRate):

    red = "#D50001"
    green = "#00C000"

    if stockRate[0] == '+':
        color = red
    if stockRate[0] == '-':
        color = green

    stock = {
        "type": "bubble",
        "size": "mega",
        "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
            {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": stockName,
                "color": color,
                "size": "3xl",
                "flex": 4,
                "weight": "bold"
                }
            ]
            },
            {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                "type": "text",
                "text": stockPrice,
                "color": color,
                "size": "xxl",
                "weight": "bold"
                },
                {
                "type": "text",
                "text": stockRate,
                "color": color,
                "size": "md",
                "flex": 4
                }
            ]
            }
        ],
        "paddingAll": "20px",
        "backgroundColor": "#000000",
        "spacing": "md",
        "height": "154px",
        "paddingTop": "22px"
        },
        "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
            {
            "type": "button",
            "height": "sm",
            "style": "link",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "個股基本面",
                "text": stockName[0:4]+'fund'
            }
            },
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "個股技術分析",
                "text": stockName[0:4] + 'tech'
            }
            },
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "個股籌碼面",
                "text": stockName[0:4] + 'chip'
            }
            },
            {
            "type": "button",
            "style": "link",
            "height": "sm",
            "color": "#398CCD",
            "action": {
                "type": "message",
                "label": "個股消息面",
                "text":stockName[0:4] + 'news'
            }
            }
        ]
        }
    }
    global stocks
    stocks.append(stock)
    
stockCarousel = {
    "type": "carousel",
    "contents": stocks
    }

################################################################################################
# 智能選股
smartStock = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "align": "center",
        "text": "智能選股",
        "weight": "bold",
        "color": "#1DB446",
        "size": "xs"
      },
      {
        "type": "text",
        "align": "center",
        "text": "選擇條件",
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "KD & RSI & OSC 黃金交叉",
          "text": "KD黃金交叉&RSI黃金交叉&OSC負翻正"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "營收年增率前五高",
          "text": "營收年增率前五高"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "ROE前五高",
          "text": "ROE前五高"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "EPS年增率前五高",
          "text": "EPS年增率前五高"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "投信近一日買超前五",
          "text": "投信近一日買超前五"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "券資比前五",
          "text": "券資比前五"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "三大法人合計前五",
          "text": "三大法人合計前五"
        }
      }
    ]
  }
}


################################################################################################
# 投資組合建構

portfolio = {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "align": "center",
        "text": "投資組合建構",
        "weight": "bold",
        "color": "#1DB446",
        "size": "xs"
      },
      {
        "type": "text",
        "align": "center",
        "text": "選擇策略",
        "weight": "bold",
        "size": "xxl",
        "margin": "md"
      },
      {
        "type": "separator",
        "margin": "xxl"
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "KD & RSI & OSC 黃金交叉",
          "text": "KD黃金交叉&RSI黃金交叉&OSC負翻正_MPT建構投資組合"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "營收年增率前五高",
          "text": "營收年增率前五高_MPT建構投資組合"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "ROE前五高",
          "text": "ROE前五高_MPT建構投資組合"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "EPS年增率前五高",
          "text": "EPS年增率前五高_MPT建構投資組合"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "投信近一日買超前五",
          "text": "投信近一日買超前五_MPT建構投資組合"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "券資比前五",
          "text": "券資比前五_MPT建構投資組合"
        }
      },
      {
        "type": "button",
        "height": "sm",
        "style": "link",
        "color": "#398CCD",
        "action": {
          "type": "message",
          "label": "三大法人合計前五",
          "text": "三大法人合計前五_MPT建構投資組合"
        }
      }
    ]
  }
}


################################################################################
# 前五高flex

def setFive(name, fir, sec, thir, four, fif):
  five = {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": "投資組合建構",
          "weight": "bold",
          "color": "#1DB446",
          "size": "sm"
        },
        {
          "type": "text",
          "text": name,
          "weight": "bold",
          "size": "lg",
          "margin": "md"
        },
        {
          "type": "separator",
          "margin": "xxl"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "xxl",
          "spacing": "sm",
          "contents": [
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "名次",
                  "size": "sm",
                  "color": "#398CCD",
                  "align": "center"
                },
                {
                  "type": "text",
                  "text": "股票代碼",
                  "size": "sm",
                  "color": "#398CCD",
                  "align": "center"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "第一名",
                  "size": "sm",
                  "color": "#555555",
                  "align": "center"
                },
                {
                  "type": "text",
                  "text": fir,
                  "size": "sm",
                  "color": "#111111",
                  "align": "center"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "第二名",
                  "size": "sm",
                  "color": "#555555",
                  "align": "center"
                },
                {
                  "type": "text",
                  "text": sec,
                  "size": "sm",
                  "color": "#111111",
                  "align": "center"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "第三名",
                  "size": "sm",
                  "color": "#555555",
                  "align": "center"
                },
                {
                  "type": "text",
                  "text": thir,
                  "size": "sm",
                  "color": "#111111",
                  "align": "center"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "第四名",
                  "size": "sm",
                  "color": "#555555",
                  "align": "center"
                },
                {
                  "type": "text",
                  "text": four,
                  "size": "sm",
                  "color": "#111111",
                  "align": "center"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "第五名",
                  "size": "sm",
                  "color": "#555555",
                  "align": "center"
                },
                {
                  "type": "text",
                  "text": fif,
                  "size": "sm",
                  "color": "#111111",
                  "align": "center"
                }
              ]
            }
          ]
        }
      ]
    }
  }
  return five