import requests
import os
import datetime
import sys
import time


#输入用户名和密码
def GetTheUserInfo():
    global Username , Password, Title
    Username = input('请输入你的学号:')
    Password = input('请输入你的密码:')
    Title=input('title(optinal)')
#获取验证码
def GetTheCheckCode():
    #获取当前绝对路径
    path1 = os.path.abspath('.')
    #设置图片保存路径
    pic_path = path1+'/checkcode.jpg'
    #获取并写入验证码
    pic =session.get('http://bkxk.xmu.edu.cn/xsxk/getCheckCode',headers=header)
    f = open(pic_path, 'wb')
    f.write(pic.content)
    f.close()
    #弹出验证码
    os.system(pic_path)
    
    #人工输入验证码
    global CheckCode
    CheckCode = input('please input check code:')

#输入课程信息
def GetCourseInfo():
    global CourseCode,CourseType
    CourseCode = input('请输入课程编码(右键点击要选的课的选课按钮选审查元素，输入PrepareSelectCourse()括号内的字符串：')
    CourseType = input('请输入选课类型代码（1为全校必修课，2为院系必修课，3为全校选修课,4为院系选修课，5为公共课 ）:')

#设置请求头
header = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
#创建session
session = requests.Session()
#输入用户名密码与验证码
GetTheUserInfo()
GetTheCheckCode()

#初始化POST数据
data = {'username':Username,
        'password':Password,
        'checkCode':CheckCode
        }


#登录时表单提交到的地址
login_url = 'http://bkxk.xmu.edu.cn/xsxk/login.html'

#发送登陆请求POST
#可以用print(session.cookies.get_dict())查看Cookies
session.post(login_url,data)

#不确定有用的headers
header = {'Referer':'http://bkxk.xmu.edu.cn/xsxk/qxxxx.html','Host':'bkxk.xmu.edu.cn','Content-Type':'application/x-www-form-urlencoded'
    ,'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.'
    ,'X-Requested-With':'XMLHttpRequest','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Connection':'keep-alive'
    ,'Accept-Encoding':'gzip, deflate','Upgrade-Insecure-Requests':'1'}


# 未知作用------------重要！
# 登录后跳转主页的页面
url = 'http://bkxk.xmu.edu.cn/xsxk/localInfo.html'
#发送访问请求
Check = session.get(url,headers=header)
# 未知作用------------重要！

#检查是否登陆成功
if '验证码' in Check.content.decode('utf-8'):
    print('用户名或密码错误，或验证码错误')
    sys.exit()

#登陆成功后获取选课信息
GetCourseInfo()
count=1
count1=0
#构成选课url 
url = 'http://bkxk.xmu.edu.cn/xsxk/elect.html?method=handleZxxk&jxbid='+CourseCode+'&xxlx='+CourseType+'&xklc=2017302'
print(url)
while True:
    count+=1
    resp = session.get(url,headers=header)
    FinalString = resp.content.decode('utf-8')
    time.sleep(0.005)
    if "错误" in FinalString:
        print('参数错误，检查参数与尾巴xklc=(选课轮次)')
        print('页面返回:', FinalString)
        sys.exit()
    if "超出" in FinalString:
        print(FinalString)
        sys.exit()
    if "true" in FinalString:
        print('选课成功！',datetime.datetime.now())
        sys.exit()
    if count == 20:
        count1 += 1
        count=0
        print(FinalString+str(count1)+Title)


