"""
new Env('GlaDOS签到')；
cron: 30 */4 * * * python3 glados.py
"""

import requests,json,os
import sys

sendContent = ''
cookies= os.environ.get("GLADOS_COOKIE", []).split("&")
if cookies[0] == "":
    print('未获取到COOKIE变量') 
    cookies = []
    exit(0)

def load_send():
    global send
    global hadsend
    cur_path = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(cur_path)
    if os.path.exists(cur_path + "/notify.py"):
        try:
            from notify import send
            hadsend=True
        except:
            printf("加载notify.py的通知服务失败，请检查~")
            hadsend=False
    else:
        printf("加载通知服务失败,缺少notify.py文件")
        hadsend=False
load_send()

def start():    
    checkin_url= "https://glados.rocks/api/user/checkin"
    status_url= "https://glados.rocks/api/user/status"
    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
    payload={
        'token': 'glados.one'
    }
    cookie_index = 0
    for cookie in cookies:
        cookie_index += 1
        checkin = requests.post(checkin_url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent,'content-type':'application/json;charset=UTF-8'},data=json.dumps(payload))
        status =  requests.get(status_url,headers={'cookie': cookie ,'referer': referer,'origin':origin,'user-agent':useragent})
    #--------------------------------------------------------------------------------------------------------#  
        time = status.json()['data']['leftDays']
        time = time.split('.')[0]
        email = status.json()['data']['email']
        global sendContent
        if 'message' in checkin.text:
            mess = checkin.json()['message']
            if mess == 'Please Try Tomorrow':
                mess = '今日已签到'
            else :
                mess = '签到成功'
            print('【账号'+str(cookie_index)+' '+email+'】'+mess+'，当前剩余('+time+')天')  # 日志输出
            sendContent += '【账号'+str(cookie_index)+' '+email+'】'+mess+'，当前剩余('+time+')天\n'
        else:
            print('【账号'+str(cookie_index)+' '+email+'】Cookie疑似失效，请更新Cookie！')  # 日志输出
            sendContent += '【账号'+str(cookie_index)+' '+email+'】Cookie疑似失效，请更新Cookie！\n'
     #--------------------------------------------------------------------------------------------------------#   
    if hadsend:
        send("GLaDOS签到通知",sendContent)


def main_handler(event, context):
  return start()

if __name__ == '__main__':
    start()