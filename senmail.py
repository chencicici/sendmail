import smtplib
import time
from email.mime.text import MIMEText
import requests
from lxml import etree
import datetime
from fake_useragent import UserAgent

sender_maile = ''  # 发件人地址
sender_pass = ''  # 邮件授权码
boy_name = ''  # 发件人姓名
girl_name = ''  # 收件人姓名
maile_obj = smtplib.SMTP_SSL('smtp.qq.com', 465)  # 发送的服务器
receiver_mail = ''  # 收件人邮箱
special_day = ''  # 纪念日
province = ''  # 省份 墨迹天气官网查看 示例province = 'guangxi'
city = ''  # 城市 示例city = 'jiangnan-district'
title = 's'  # 邮件主题
ua = UserAgent()
header = {
    'Referer': 'https://tianqi.moji.com/weather/china/guangxi', # 根据城市修改
    'User-Agent': ua.random
}

session = requests.session()


# 获取纪念日距今多少天
def get_day():
    d1 = datetime.datetime.strptime(special_day, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    delta = d2 - d1
    return delta.days


# 获取每日土味情话
def get_chp():
    url =  "https://api.lovelive.tools/api/SweetNothings"
    resp = requests.get(url=url)
    return resp.text


# 获取提醒
def get_weathertip():
    try:
        url = f'https://tianqi.moji.com/weather/china/{province}/{city}'
        resp = session.get(url=url, headers=header, verify=False)
        html = etree.HTML(resp.text)
        em = html.xpath('/html/body/div[4]/div[1]/div[4]/em/text()')[0]
        return em
    except:
        return False


# 获取每日天气
def get_weather():
    try:
        url = f'https://tianqi.moji.com/weather/china/{province}/{city}'
        resp = session.get(url=url, headers=header,  verify=False)
        html = ''
        htmls = etree.HTML(resp.text)
        ul = htmls.xpath('/html/body/div[5]/div[1]/div[1]/ul')
        for lis in ul:
            # 获取日期
            day = lis.xpath('./li[1]/a/text()')[0]
            # 获取天气图标
            src = lis.xpath('./li[2]/span/img/@src')[0]
            # 获取天气状况
            weather = lis.xpath('./li[2]/span/img/@alt')[0]
            # 获取温度
            temperature = lis.xpath('./li[3]/text()')[0]
            # 获取空气质量
            air = lis.xpath('./li[5]/strong/text()')[0].strip()
            # 获取空气质量对应的字体颜色
            color = str(lis.xpath('./li[5]/strong/@class')[0])
            # 判断字体颜色
            if color == 'level_1':
                color = '#8fc31f'
            elif color == 'level_2':
                color = '#d7af0e'
            elif color == 'level_3':
                color = '#f39800'
            elif color == 'level_4':
                color = '#e2361a'
            elif color == 'level_5':
                color = '#5f52a0'
            elif color == 'level_6':
                color = '#631541'
            html += """<div style="display: flex;margin-top:5px;height: 30px;line-height: 30px;justify-content: space-around;align-items: center;">
            <span style="width:15%%; text-align:center;">%s</span>
            <div style="width:10%%; text-align:center;">
                <img style="height:26px;vertical-align:middle;" src='%s' alt="">
            </div>
            <span style="width:25%%; text-align:center;">%s</span>
            <div style="width:35%%; ">
                <span style="display:inline-block;padding:0 8px;line-height:25px;color:%s; border-radius:15px; text-align:center;">%s</span>
            </div>
            </div>
            """ % (day, src, temperature, color, air)
        return html
    except:
        return False


# 获取图片
def get_image():
    url = "http://wufazhuce.com/"
    resp = requests.get(url=url)
    html = etree.HTML(resp.text)
    img_url = html.xpath('//*[@id="carousel-one"]/div/div[1]/a/img/@src')[0]
    return img_url


# 获取当天日期
def get_today():
    i = datetime.datetime.now()
    date = "%s/%s/%s" % (i.year, i.month, i.day)
    return date


mail_content = """<!DOCTYPE html>
                <html>

                <head>
                    <title>
                    </title>
                    <meta name="viewport" content="width=device-width,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
                    <meta charset="UTF-8">
                </head>

                <body style="margin:0;padding:0;">
                    <div style="width:100%; margin: 40px auto;font-size:20px; color:#5f5e5e;text-align:center">
                        <span>今天是我们在一起的第</span>
                        <span style="font-size:24px;color:rgb(221, 73, 73)"  >{0}</span>
                        <span>天</span>
                    </div>
                    <div style="width:100%; margin: 0 auto;color:#5f5e5e;text-align:center">
                        <span style="display:block;color:#676767;font-size:20px">{2}</span>
                        <br>
                        <span style="display:block;color:#676767;font-size:20px">{1}</span>
                        <span style="display:block;margin-top:15px;color:#676767;font-size:15px">近期天气预报</span>
                {3}
                    </div>
                    <div style="text-align:center;margin:35px 0;">
                            <span style="display:block;margin-top:55px;color:#676767;font-size:15px">{4} ❤️ {5}</span>
                            <span style="display:block;margin-top:25px;font-size:22px; color:#9d9d9d; ">{6}</span>
                             <img src='{7}' style="width:100%;margin-top:10px;"  alt="">
                    </div>
                </body>

                </html>""".format(str(get_day()), get_weathertip(), get_chp(), get_weather(), boy_name, girl_name,
                                  get_today(), get_image())


# 发送邮件
def send_mail():
    try:
        maile_obj.login(sender_maile, sender_pass)
        # 三个参数分别是发件人邮箱账号,收件人账号,发送的邮件内容
        msg = MIMEText(mail_content, _subtype='html', _charset='utf-8')
        msg['Subject'] = title
        msg['From'] = "发送人名称"
        msg['To'] = "接收人名称"
        maile_obj.sendmail(sender_maile, receiver_mail, msg.as_string())
        maile_obj.quit()
        return True
    except smtplib.SMTPException as e:
        return False


if __name__ == '__main__':
    send_mail()
    print('发送成功!')
    theTime = datetime.datetime.now()
    print(theTime)
