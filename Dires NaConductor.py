import re #正则表达式
import os #操作系统模块
import urllib #进行SQLite数据库操作
from urllib import parse
from urllib import request


'''

Python版本 3.9.6 64-bit
最后编写时间 2021-10-15
作者 icloudsheep
平台 Visual Studio Code
工作室 Dires Studio

注 以下人名均为虚拟 如有雷同 纯属巧合
注 学校信息仅供参考

'''


names = [] #存入所有名字数据 方便后续与网页数据做对比

# ~原网址（代码不显示排名）~ url = "http://dxx.ahyouth.org.cn/#/pages/class/ranking/ranking?table_name=reason_stage145&level1=直属高校&level2=（2）&level3=（3）&level4=（4）"
# ~示例网址（实际加载排名的网页）~ url = "http://dxx.ahyouth.org.cn/api/peopleRankStage?table_name=reason_stage（此处为青年大学习期数）&level1=（此处为第一层级 例：直属高校）&level2=（此处为第二层级 例：合肥工业大学）&level3=（此处为第三层级 例：土木与水利工程学院团委）&level4=（此处为第四层级 例：2021级研44班团支部）"

url1 = "http://dxx.ahyouth.org.cn/api/peopleRankStage?table_name=reason_stage"
url2 = "&level1="
url3 = "&level2="
url4 = "&level3="
url5 = "&level4="
url_num = "145" #第12-3为 145 往后为单数 例147 149 ~
url_level1 = ""
url_level2 = ""
url_level3 = ""
url_level4 = ""


findname = re.compile(r'\"username\":\"(.*?)\",\"addtime\":\"') #正则表达式 用于提取姓名的unicode码
findtime = re.compile(r'\",\"addtime\":\"(.*?)\"}') #正则表达式 用于提取完成时间


def iosafety(): #保障软件基本运行文件存在 如果不存在则创建并赋予默认值
    if os.path.exists("pyConfig.txt"):
        print()
    else:
        fileRepair_pyConfig = open("pyConfig.txt","w",encoding="utf-8")
        fileRepair_pyConfig.write(fileRepair_pyConfig_FileContext)
        fileRepair_pyConfig.close
    if os.path.exists("nameAll.txt"):
        print()
    else:
        fileRepair_nameAll = open("nameAll.txt","w",encoding="utf-8")
        fileRepair_nameAll.write(fileRepair_nameAll_FileContext)
        fileRepair_nameAll.close


def main():

    iosafety() #执行IO保护
    
    f4 = open("pyConfig.txt","r",encoding="utf-8") #读取pyConfig.txt来为软件进行基本配置
    outputInfo("文件打开: pyConfig.txt")
    config = [line.strip("\n") for line in f4.readlines()]
    url1 = config[1]
    url2 = config[3]
    url3 = config[5]
    url4 = config[7]
    url5 = config[9]
    url_num = config[11]
    url_level1 = config[13]
    url_level2 = config[15]
    url_level3 = config[17]
    url_level4 = config[19]
    outputInfo("配置导入完成")
    f4.close
    outputInfo("文件关闭: pyConfig.txt")
    
    oriurl = url1 + url_num + url2 + url_level1 + url3 + url_level2 + url4 + url_level3 + url5 + url_level4 #oriurl：只进行简单相加但并未执行url编码的初始网址
    url = url1 + url_num + url2 + parse.quote(url_level1) + url3 + parse.quote(url_level2) + url4 + parse.quote(url_level3) + url5 + parse.quote(url_level4) #进行url编码
    outputInfo("初始网址合成完成: " + oriurl)
    outputInfo("网址合成完成: " + url)

    f2 = open("nameAll.txt","r",encoding="utf-8") #读取所有名字信息 并将其存入names 方便后续比对
    outputInfo("文件打开: nameAll.txt")
    names = [line.strip("\n") for line in f2.readlines()]
    f2.close
    outputInfo("文件关闭: nameAll.txt")

    print(names)
    print(oriurl)
    print(url)

    getData(url) #开始网页操作
    outputInfo("方法调用: getData(url)")


def getData(baseurl):

    f2 = open("nameAll.txt","r",encoding="utf-8") #重新赋值 确保names值正确
    outputInfo("文件打开: nameAll.txt")
    names = [line.strip("\n") for line in f2.readlines()]
    f2.close
    outputInfo("文件关闭: nameAll.txt")
    
    rawHtml = askurl(baseurl) #网页初始源代码
    nhtml = rawHtml.encode().decode("unicode_escape") #网页转码后代码
    outputInfo("代码获取完成")

    f = open("name.txt","w") #存储名字文件创建
    f3 = open("lastname.txt","w") #储存未做人员名字文件
    outputInfo("文件打开: name.txt , lastname.txt")

    nameresults = re.findall(findname,rawHtml) 
    timeresults = re.findall(findtime,rawHtml)
    outputInfo("name与time寻找完毕")

    i = 0 #匹配人员与日期

    for result in nameresults:
        result = result.encode().decode("unicode_escape")

        for name in names:
            if name == result:
                names.remove(name)
                print("人名删除: " + result)

        f.write(result + "\n")
        f.write(timeresults[i] + "\n")

        i = i + 1
    outputInfo("name与time写入完成")

    for lastname in names:
        f3.write(lastname + "\n")
    outputInfo("lastname寻找与写入完成")
    
    print(names)

    f3.close
    f.close
    outputInfo("文件关闭: name.txt , lastname.txt")
    

def outputInfo(info): #打印输出信息
    f5 = open("outputInfo.txt","a")
    f5.write(info + "\n\n")


def askurl(url):
    head = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.73"}
    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except Exception as error:
        print(error)
    return html


fileRepair_pyConfig_FileContext = "1:url1:\nhttp://dxx.ahyouth.org.cn/api/peopleRankStage?table_name=reason_stage\n3:url2:\n&level1=\n5:url3:\n&level2=\n7:url4:\n&level3=\n9:url5:\n&level4=\n11:url_num: 145 12季3期\n145\n13:url_level1:\n直属高校\n15:url_level2:\n合肥工业大学\n17:url_level3:\n土木与水利工程学院团委\n19:url_level4:\n2021级研44班团支部\n:)"
fileRepair_nameAll_FileContext = "张三\n李四\n王五\n上甲\n如乙\n大丙\n二丁\n瑞敏\n储意\n亚磊\n刘训\n汲世\n静如\n琼玉"


main() #运行程序