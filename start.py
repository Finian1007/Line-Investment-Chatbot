from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

from PIL import Image
from io import StringIO

import requests
import random
import json
import math
import time
import datetime

#---------------- self define module ----------------
import text_push as text_push
import text_reply as text_reply

import flex as flex
import form as form

#---------------- self define variables ----------------
from mykey import *

#---------------- line settings ----------------
# Channel Access Token
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
# Channel Secret
handler = WebhookHandler(LINE_CHANNEL_SECRET)

#---------------------------------------------------

app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent)
def handle_message(event):
    print(event)
    message_send_time = float(event.timestamp)/1000
    message_get_time = float(time.time())
    msg_type = event.message.type

    if event.message.text == "info":
        output_message = TextSendMessage(text=str(event))  
        line_bot_api.reply_message(event.reply_token, output_message)

    if msg_type == "sticker":
        output_message = StickerSendMessage(package_id='2',sticker_id=str(random.randint(140,180)))
        line_bot_api.reply_message(event.reply_token, output_message) 

    elif msg_type == "text":
        user_message = event.message.text
        if user_message =='car':
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '個股報價與分析',
                    contents = flex.stockCarousel
                )
            )
        if user_message == '使用說明':
            message = TextSendMessage(text=text_reply.wanwan(user_message))
            line_bot_api.reply_message(event.reply_token, message)


        if flex.isStart:      
            message = TextSendMessage(text='請輸入「你好」以開始使用')
            line_bot_api.reply_message(event.reply_token, message)
            flex.isStart = False

        # greeting message
        if user_message == '你好':
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '理財汪汪！',
                    contents = flex.greet
                )
            )
        # 個股報價與分析
        if user_message == '個股報價與分析':
            if flex.hasInited:
                flex.stockCarousel = flex.stockCarousel
            else:
                flex.initStock(text_reply.wanwan(user_message)[0], text_reply.wanwan(user_message)[1])
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '個股報價與分析',
                    contents = flex.stockCarousel
                )
            )
        if user_message == '新增自選股':
            message = TextSendMessage(text='請輸入想新增的自選股股票代碼，Ex: add3008, add1030')
            line_bot_api.reply_message(event.reply_token, message)

        if 'add' in user_message:
            stockNum = user_message #這是用來抓data的
            flex.appendStock(text_reply.wanwan(user_message)[0], text_reply.wanwan(user_message)[1], text_reply.wanwan(user_message)[2])
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '個股報價與分析',
                    contents = flex.stockCarousel
                )
            )
        if user_message == '智能選股':
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.smartStock
                )
            )

        if user_message == '投資組合建構':
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '投資組合建構',
                    contents = flex.portfolio
                )
            )
        if user_message == '全球行情':
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == '原物料報價':
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == '匯率報價':
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == '總體經濟指標':
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if "fund" in user_message:
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if "tech" in user_message:
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if "chip" in user_message:
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
            
        if "news" in user_message:
            message = TextSendMessage(text=text_reply.wanwan(user_message))
            line_bot_api.reply_message(event.reply_token, message)


        if user_message == "KD黃金交叉&RSI黃金交叉&OSC負翻正":
            # message = TextSendMessage(text=text_reply.wanwan(user_message))
            # line_bot_api.reply_message(event.reply_token, message)
            fiveValue = text_reply.wanwan(user_message)
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.setFive('KD & RSI & OSC 黃金交叉', fiveValue[0], fiveValue[1], fiveValue[2], fiveValue[3], fiveValue[4])
                )
            )
        if user_message == "營收年增率前五高":
            # message = TextSendMessage(text=text_reply.wanwan(user_message))
            # line_bot_api.reply_message(event.reply_token, message)
            fiveValue = text_reply.wanwan(user_message)
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.setFive(user_message, fiveValue[0], fiveValue[1], fiveValue[2], fiveValue[3], fiveValue[4])
                )
            )
        if user_message == "ROE前五高":
            # message = TextSendMessage(text=text_reply.wanwan(user_message))
            # line_bot_api.reply_message(event.reply_token, message)
            fiveValue = text_reply.wanwan(user_message)
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.setFive(user_message, fiveValue[0], fiveValue[1], fiveValue[2], fiveValue[3], fiveValue[4])
                )
            )
        if user_message == "EPS年增率前五高":
            # message = TextSendMessage(text=text_reply.wanwan(user_message))
            # line_bot_api.reply_message(event.reply_token, message)
            fiveValue = text_reply.wanwan(user_message)
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.setFive(user_message, fiveValue[0], fiveValue[1], fiveValue[2], fiveValue[3], fiveValue[4])
                )
            )
        if user_message == "投信近一日買超前五":
            # message = TextSendMessage(text=text_reply.wanwan(user_message))
            # line_bot_api.reply_message(event.reply_token, message)
            fiveValue = text_reply.wanwan(user_message)
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.setFive(user_message, fiveValue[0], fiveValue[1], fiveValue[2], fiveValue[3], fiveValue[4])
                )
            )
        if user_message == "券資比前五":
            # message = TextSendMessage(text=text_reply.wanwan(user_message))
            # line_bot_api.reply_message(event.reply_token, message)
            fiveValue = text_reply.wanwan(user_message)
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.setFive(user_message, fiveValue[0], fiveValue[1], fiveValue[2], fiveValue[3], fiveValue[4])
                )
            )
        if user_message == "三大法人合計前五":
            # message = TextSendMessage(text=text_reply.wanwan(user_message))
            # line_bot_api.reply_message(event.reply_token, message)
            fiveValue = text_reply.wanwan(user_message)
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '智能選股',
                    contents = flex.setFive(user_message, fiveValue[0], fiveValue[1], fiveValue[2], fiveValue[3], fiveValue[4])
                )
            )
        if user_message == "KD黃金交叉&RSI黃金交叉&OSC負翻正_MPT建構投資組合":
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == "營收年增率前五高_MPT建構投資組合":
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == "ROE前五高_MPT建構投資組合":
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == "EPS年增率前五高_MPT建構投資組合":
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == "投信近一日買超前五_MPT建構投資組合":
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == "券資比前五_MPT建構投資組合":
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        if user_message == "三大法人合計前五_MPT建構投資組合":
            line_bot_api.reply_message(
                event.reply_token, ImageSendMessage(
                    original_content_url=text_reply.wanwan(user_message),
                    preview_image_url=text_reply.wanwan(user_message)
                )
            )
        
        # 風險評估問券
        if user_message == '風險評估問券':
            form1 = form.formDict["form1"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            )
        if "formA" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form2"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formB" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form3"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formC" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form4"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formD" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form5"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formE" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form6"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formF" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form7"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formG" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form8"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formH" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form9"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            )
        if "formI" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form10"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formJ" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form11"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formK" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form12"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formL" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form13"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if "formM" in user_message:
            form.score += int(user_message[5])
            form1 = form.formDict["form14"]
            line_bot_api.reply_message(
                event.reply_token, FlexSendMessage(
                    alt_text = '風險評估問券',
                    contents = form.createForm(form1["question"], form1["ans1"]["text"], form1["ans1"]["value"], form1["ans2"]["text"], form1["ans2"]["value"],form1["ans3"]["text"], form1["ans3"]["value"],form1["ans4"]["text"], form1["ans4"]["value"],form1["ans5"]["text"], form1["ans5"]["value"])
                )
            ) 
        if ("yes" in user_message) or ("no" in user_message):
            message = TextSendMessage(text=form.checkResult(form.score, user_message))
            line_bot_api.reply_message(event.reply_token, message)
            form.score = 0

    


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
