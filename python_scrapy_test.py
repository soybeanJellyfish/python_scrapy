import requests
import json
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler
import smtplib
from email.mime.text import MIMEText

global instockmsg
mail_host="smtp.gmail.com"
mail_user="scriptresult1988@gmail.com"
mail_pass="*****"
sender="scriptresult1988@gmail.com"
receivers="*****"

def job():
    isSend=False
    content=""
    lancomeDict = {"1.7oz":"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3605533117217&quantity=1",
                    "2.5oz":"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3605533117279&quantity=1",
                    "3.4oz":"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3605532978871&quantity=1",
                    "1.0oz":"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3605533117156&quantity=1",
                    "3.9oz":"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3614272783478&quantity=3",
                    "0.67oz":"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3614272783478&quantity=3"
    }
    print("小黑瓶")
    for key in lancomeDict:
        url= lancomeDict[key]
        req = requests.get(url)
        if(req.status_code == 200):
            status = json.loads(req.text)['status']
            if status == "BACKORDER":
                instockmsg = json.loads(req.text)['inStockDateMsg']
            else:
                instockmsg = json.loads(req.text)['inStockMsg']
            print (key + " " + status + " " +instockmsg)
        else:
            print (key + " %s"  %req.status_code)

    lancomeCreamsDict={"1.0oz": "https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3614272325265&quantity=1",
                        "2.0oz" :"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3614272295353&quantity=1",
                        "rich cream":"https://www.lancome-usa.com/on/demandware.store/Sites-lancome-us-Site/default/Product-GetAvailability?pid=3614272295452&quantity=3"
    }

    print("面霜")
    for key in lancomeCreamsDict:
        url= lancomeCreamsDict[key]
        req = requests.get(url)
        status = json.loads(req.text)['status']
        if status == "BACKORDER":
            instockmsg = json.loads(req.text)['inStockDateMsg']
        elif(status == "IN_STOCK" and key== "rich cream"):
            isSend = True
            content += "rich cream is in stock \n https://www.lancome-usa.com/cart \n promo code inourhearts"
        else:
            instockmsg = json.loads(req.text)['inStockMsg']
        print (key + " " + status + " " +instockmsg)

    #lv bage
    url = "https://secure.louisvuitton.com/ajaxsecure/getStockLevel.jsp?storeLang=eng-us&pageType=storelocator_section&skuIdList=M44813&null&_=1588204078866"
    headers={
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
    try:
        req = requests.get(url, timeout=10,verify=True,headers = headers)
        status = json.loads(req.text)['M44813']["inStock"]
        if(status):
            isSend = True
            content += "Multi Pochette is in stock \n https://us.louisvuitton.com/eng-us/products/multi-pochette-accessoires-monogram-nvprod1770359v \n"
        print("Multi Pochette is in stock: %s"  %status)
    except requests.exceptions.RequestException as e:
        print(e)

    if(isSend):
        message = MIMEText(content,'plain','utf-8')
        #邮件主题       
        message['Subject'] = '爬虫小机器人提醒您' 
        #发送方信息
        message['From'] = sender 
        #接受方信息     
        message['To'] = receivers[0]  
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host)
            #登录到服务器
            smtpObj.login(mail_user,mail_pass) 
            #发送
            smtpObj.sendmail(
                sender,receivers,message.as_string()) 
            #退出
            smtpObj.quit() 
            content=""
            print('success')
        except smtplib.SMTPException as e:
            print('error',e) #打印错误
scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=5,start_date='2020-05-07 1:02:30')
scheduler.start()