
def createForm(question, ans1text, ans1value, ans2text, ans2value, ans3text, ans3value, ans4text, ans4value, ans5text, ans5value) :
    form = {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "text": "風險評估問券",
            "weight": "bold",
            "color": "#1DB446",
            "size": "sm"
        },
        {
            "type": "text",
            "text": question,
            "weight": "bold",
            "size": "sm",
            "margin": "md"
        },
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "button",
            "height": "xs",
            "style": "link",
            "color": "#398CCD",
            "action": {
            "type": "message",
            "label": ans1text,
            "text": ans1value
            }
        },
        {
            "type": "button",
            "height": "xs",
            "style": "link",
            "color": "#398CCD",
            "action": {
            "type": "message",
            "label": ans2text,
            "text": ans2value
            }
        },
        {
            "type": "button",
            "height": "xs",
            "style": "link",
            "color": "#398CCD",
            "action": {
            "type": "message",
            "label": ans3text,
            "text": ans3value
            }
        },
        {
            "type": "button",
            "height": "xs",
            "style": "link",
            "color": "#398CCD",
            "action": {
            "type": "message",
            "label": ans4text,
            "text": ans4value
            }
        },
        {
            "type": "button",
            "height": "xs",
            "style": "link",
            "color": "#398CCD",
            "action": {
            "type": "message",
            "label": ans5text,
            "text": ans5value
            }
        }
        ]
    }
    }
    return form


formDict = {
    "form1": {
        "question" : "1.你的主要收入來源是：",
        "ans1" : {
            "text" : "無固定收入",
            "value" : "formA0"
        },
        "ans2" : {
            "text" : "非金融性資產收入",
            "value" : "formA2"
        },
        "ans3" : {
            "text" : "金融性資產收入",
            "value" : "formA4"
        },
        "ans4" : {
            "text" : "生產經營所得",
            "value" : "formA6"
        },
        "ans5" : {
            "text" : "工資、勞務報酬",
            "value" : "formA8"
        },
    },
    "form2": {
        "question" : "2.你的家庭就業狀況是：",
        "ans1" : {
            "text" : "未婚、暫無穩定收入",
            "value" : "formB0"
        },
        "ans2" : {
            "text" : "未婚、有穩定收入",
            "value" : "formB2"
        },
        "ans3" : {
            "text" : "與配偶無穩定收入或已退休",
            "value" : "formB4"
        },
        "ans4" : {
            "text" : "與配偶其中一人有穩定收入",
            "value" : "formB6"
        },
        "ans5" : {
            "text" : "與配偶皆有穩定收入",
            "value" : "formB8"
        },
    },
    "form3": {
        "question" : "3.你主要想將自己的投資回報用於：",
        "ans1" : {
            "text" : "償還債務",
            "value" : "formC0"
        },
        "ans2" : {
            "text" : "本人養老或醫療",
            "value" : "formC2"
        },
        "ans3" : {
            "text" : "履行扶養或贍養義務",
            "value" : "formC4"
        },
        "ans4" : {
            "text" : "工作或證券以外的投資行為",
            "value" : "formC6"
        },
        "ans5" : {
            "text" : "改善生活",
            "value" : "formC8"
        },
    },
    "form4": {
        "question" : "4.您的家庭可支配年收入(TWD)為：",
        "ans1" : {
            "text" : "250萬以下",
            "value" : "formD0"
        },
        "ans2" : {
            "text" : "250萬~500萬",
            "value" : "formD2"
        },
        "ans3" : {
            "text" : "500萬~2500萬",
            "value" : "formD4"
        },
        "ans4" : {
            "text" : "2500萬~5000萬",
            "value" : "formD6"
        },
        "ans5" : {
            "text" : "5000萬以上",
            "value" : "formD8"
        },
    },
    "form5": {
        "question" : "5.你可用來投資的資產總額：",
        "ans1" : {
            "text" : "250萬以下",
            "value" : "formE0"
        },
        "ans2" : {
            "text" : "250萬~500萬",
            "value" : "formE2"
        },
        "ans3" : {
            "text" : "500萬~2500萬",
            "value" : "formE4"
        },
        "ans4" : {
            "text" : "2500萬~5000萬",
            "value" : "formE6"
        },
        "ans5" : {
            "text" : "5000萬以上",
            "value" : "formE8"
        },
    },
    "form6": {
        "question" : "6.年家庭可支配收入中可投資比例為：",
        "ans1" : {
            "text" : "小於10%",
            "value" : "formF2"
        },
        "ans2" : {
            "text" : "10% ~ 25%",
            "value" : "formF4"
        },
        "ans3" : {
            "text" : "25% ~ 50%",
            "value" : "formF6"
        },
        "ans4" : {
            "text" : "大於50%",
            "value" : "formF8"
        },
        "ans5" : {
            "text" : "x",
            "value" : "formF0"
        },
    },
    "form7": {
        "question" : "7.是否有未償還債務? 如有，性值為?",
        "ans1" : {
            "text" : "有，親朋間借款",
            "value" : "formG2"
        },
        "ans2" : {
            "text" : "有，信用卡等短期債務",
            "value" : "formG4"
        },
        "ans3" : {
            "text" : "有，房債等長期債務",
            "value" : "formG6"
        },
        "ans4" : {
            "text" : "無",
            "value" : "formG8"
        },
        "ans5" : {
            "text" : "x",
            "value" : "formG0"
        },
    },
    "form8": {
        "question" : "8.你的投資知識可描述為：",
        "ans1" : {
            "text" : "無基本金融產品知識",
            "value" : "formH0"
        },
        "ans2" : {
            "text" : "有基本金融產品知識",
            "value" : "formH3"
        },
        "ans3" : {
            "text" : "有豐富金融產品知識",
            "value" : "formH6"
        },
        "ans4" : {
            "text" : "x",
            "value" : "formH0"
        },
        "ans5" : {
            "text" : "x",
            "value" : "formH0"
        },
    },
    "form9": {
        "question" : "9.你的投資經驗可描述為：",
        "ans1" : {
            "text" : "無銀行儲蓄外的投資經驗",
            "value" : "formI2"
        },
        "ans2" : {
            "text" : "買過債券、保險等理財商品",
            "value" : "formI4"
        },
        "ans3" : {
            "text" : "參與過股票、基金等產品交易",
            "value" : "formI6"
        },
        "ans4" : {
            "text" : "參與過證券、期貨等產品交易",
            "value" : "formI8"
        },
        "ans5" : {
            "text" : "x",
            "value" : "formI0"
        },
    },
    "form10": {
        "question" : "10.你有多少年金融性產品投資經驗",
        "ans1" : {
            "text" : "無經驗",
            "value" : "formJ0"
        },
        "ans2" : {
            "text" : "低於2年",
            "value" : "formJ2"
        },
        "ans3" : {
            "text" : "2 ~ 5年",
            "value" : "formJ4"
        },
        "ans4" : {
            "text" : "5 ~ 10年",
            "value" : "formJ6"
        },
        "ans5" : {
            "text" : "10年以上",
            "value" : "formJ8"
        },
    },
    "form11": {
        "question" : "11.以下何者為你的投資態度：",
        "ans1" : {
            "text" : "厭惡風險，想有穩定收入",
            "value" : "formK0"
        },
        "ans2" : {
            "text" : "保守投資，願意承擔一定風險",
            "value" : "formK3"
        },
        "ans3" : {
            "text" : "求較高效益，願承擔較高風險",
            "value" : "formK6"
        },
        "ans4" : {
            "text" : "尋求高效益，願承擔一定損失",
            "value" : "formK9"
        },
        "ans5" : {
            "text" : "x",
            "value" : "formK0"
        },
    },
    "form12": {
        "question" : "A: 10%收益,小風險 B: 30%收益,大風險",
        "ans1" : {
            "text" : "全部投資於A",
            "value" : "formL2"
        },
        "ans2" : {
            "text" : "都投資，但大部分A",
            "value" : "formL4"
        },
        "ans3" : {
            "text" : "都投資，但大部分B",
            "value" : "formL6"
        },
        "ans4" : {
            "text" : "全部投資於B",
            "value" : "formL8"
        },
        "ans5" : {
            "text" : "x",
            "value" : "formL0"
        },
    },
    "form13": {
        "question" : "13.你認為自己能承受最大損失為",
        "ans1" : {
            "text" : "10%以內",
            "value" : "formM0"
        },
        "ans2" : {
            "text" : "10% ~ 30%",
            "value" : "formM2"
        },
        "ans3" : {
            "text" : "30% ~ 50%",
            "value" : "formM4"
        },
        "ans4" : {
            "text" : "大於50%",
            "value" : "formM6"
        },
        "ans5" : {
            "text" : "x",
            "value" : "formM0"
        },
    },
    "form14": {
        "question" : "14.你是否為以下類型投資者",
        "ans1" : {
            "text" : "沒有任何風險承受度",
            "value" : "no"
        },
        "ans2" : {
            "text" : "不能接受投資損失",
            "value" : "no"
        },
        "ans3" : {
            "text" : "以上皆非",
            "value" : "yes"
        },
        "ans4" : {
            "text" : "x",
            "value" : "no"
        },
        "ans5" : {
            "text" : "x",
            "value" : "no"
        },
    }
}


score = 0  


def checkResult(result, yesno):
    formAnswer = ''
    if result <= 20 or yesno =='no':
        formAnswer = '你的風險承受能力為C1，可購買(R1)型金融產品'
    elif result <= 40:
        formAnswer = '你的風險承受能力為C2，可購買(R1,R2)型金融產品'
    elif result <=70: 
        formAnswer = '你的風險承受能力為C3，可購買(R1,R2,R3)型金融產品'
    elif result <=85: 
        formAnswer = '你的風險承受能力為C4，可購買(R1,R2,R3,R4)型金融產品'
    else:
        formAnswer = '你的風險承受能力為C5，可購買(R1,R2,R3,R4,R5)型金融產品'
    return formAnswer