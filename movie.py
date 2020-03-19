import time,os,colorama
from os import system
from requests import get,RequestException
from prettytable import PrettyTable
from webbrowser import open as webopen
from sys import exit as sexit

def httpget(url):
    i=1
    while i<=3:
        try:
            headers={b'accept': b'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3', b'accept-encoding': b'gzip, deflate, br', b'accept-language': b'zh-CN,zh;q=0.9', b'cache-control': b'max-age=0', b'cookie': b'UM_distinctid=17075d85cff10a-01607eb9ead8a8-376b4502-100200-17075d85d00120; CNZZDATA1255357127=319138885-1582524254-%7C1583800577', b'referer': b'https://www.meitulu.com/', b'sec-fetch-mode': b'navigate', b'sec-fetch-site': b'same-origin', b'sec-fetch-user': b'?1', b'upgrade-insecure-requests': b'1', b'user-agent': b'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
            r=get(url=url,headers=headers,timeout=3)
            r.encoding = 'GB2312'
            r.raise_for_status()
            return r.json()
        except RequestException:
            print(colorama.Back.RED+'*从服务器获取数据失败！')
            print('[{}/3]正在尝试重连！'.format(str(i)))
            i+=1
    print(colorama.Back.RED+'*重连失败，请复制错误信息报告作者！')
    input('请按Enter键退出...')
    sexit()
    
def init():  # 初始化
    # 提示语
    colorama.init(True)
    system('title Movie Helper[v2] @吾爱破解 lihaisanhui') #设置窗口标题
    print('*欢迎使用Movie Helper[V2]！作者：吾爱破解@lihaisanhui')
    print('依赖项：ffmpeg.exe,N_m3u8DL-CLI.exe，请确认本程序与依赖项在同一个目录！')
    print(colorama.Fore.RED+'声明：本软件不生产、储存内容，有关资源均来源于网络，作者不为其中内容负法律责任\n免费软件，仅供论坛会员学习交流，请于下载后24小时内删除，请勿用于商业用途！！！\n')
    # 从服务器获取api接口、播放源数据
    url = 'https://www.ttupp.com/tv.txt'
    r =httpget(url)
    global api, ports
    api = r['远程api']
    ports = r['播放源'][0]

def get_input(text, maxint,extra=None):  # 用户输入判断
    while True:
        userin = input(text)
        if userin.lower() == 'q':  # 输入q退出程序
            sexit()
        if extra==1:    
            if userin == '+': #输入为空的处理，extra参数用于确定调用位置
                return '+'
            if userin=='-':
                return '-'
            if userin == 'c':
                return 'c'
        elif extra==2:
            if userin == '':
                return 1
        if userin.isdecimal() == True:  # 判断输入是否合法，以免发生错误
            if int(userin) <= maxint and int(userin)>0:
                return int(userin)
        print(colorama.Back.RED+'*您的输入非法，请重新输入！')


def search(port):  # 获取搜索结果
    while True:
        keyword = input('>请输入搜索关键词[源{}]： '.format(port))
        url = api+'?type=search&jiekou='+port+'&value='+keyword  # 拼接api
        r = httpget(url)  # 返回json
        if r['code']==200:
            data = r['data']  # 搜索结果
            return data
        else:print(colorama.Back.RED+'*发生错误['+str(r['code'])+']： '+r['msg'])


def prtres(res):  # 打印搜索结果
    # 输出表格
    tb = PrettyTable(['序号', '类型', '更新时间', '影片名'])
    for i in range(len(res)):
        tb.add_row([i+1, res[i]['sort'], res[i]['time'], res[i]['title']])
    #提示用户选择
    print('*共找到搜索结果 '+str(len(res))+' 条：')
    print(tb)
    i = get_input('>请输入序号选择[q=退出]： ', len(res))  # 返回用户选择
    return res[i-1]


def detail(choice, port):  # 获取播放地址
    #获取数据
    url = api+'?type=video&jiekou='+port+'&value='+choice['url']  # 拼接api
    r = httpget(url)  # 返回json
    content = r['data']['content']
    print(colorama.Back.GREEN+'*已选：【'+choice['title']+' / 共'+str(len(content))+'集】')
    while True:
        c=input('>请选择操作[1=下载,2=播放,q=退出程序,c=重新选择]： ')
        if c=='1':
            # 写入下载地址
            while True:
                c=input('>是否调用内置下载器下载？[y/n] ')
                if c.lower()=='y':
                    index = get_input('>请输入要下载的集数： ', len(content))
                    for i in range(index):
                        system('title 正在下载第{}集'.format(str(i+1)))
                        order="N_m3u8DL-CLI.exe "+content[i]['url']+" --saveName "+choice['title']+'_'+str(i+1)+" --enableDelAfterDone"
                        system(order)
                        system('title 成功下载第{}集'.format(str(i+1)))
                        time.sleep(3)
                    break
                elif c.lower()=='n':
                    with open(choice['title']+'_Dlurls.txt', 'w') as txt:  
                        for item in content:
                            txt.write(item['url']+'\n')
                    print('*下载地址获取成功！')
                    break
                else:print(colorama.Back.RED+'*没有这个选项！')
            break  
        elif c=='2':
            # 以表格形式输出剧集列表
            tb = PrettyTable(['序号', '剧集名称'])  
            for i in range(len(content)):
                tb.add_row([i+1, content[i]['name']])
            print(tb)
            # 播放视频
            i = get_input('>请选择要播放的剧集： ', len(content))
            while True:  # 播放时循环
                print(colorama.Back.GREEN+'\n*正在播放： '+choice['title']+' ['+content[i-1]['name']+']')
                print('    *正在用默认浏览器打开播放页！')
                time.sleep(1)
                webopen('https://www.m3u8play.com/?play=' + content[i-1]['url'])  # 浏览器打开播放地址
                t = get_input('    >控制栏[q=退出程序，c=退出播放，序号=切到对应剧集，加号=切下一集，减号=切上一集]： ', len(content),1)
                if t == '+':
                    if i == len(content):
                        print('*已经是最后一集！')
                        break
                    else:i += 1
                elif t == '-':
                    if i==1:
                        print('*已经是第一集！')
                        break
                    else:i -= 1
                elif t=='c':break
                else:i = t
            break
        elif c.lower()=='q':
            sexit()
        elif c.lower()=='c':
            detail(prtres(result),port)
        else:print(colorama.Back.RED+'*没有这个选项！')
        
if __name__ == "__main__": #程序入口
    init() #初始化

    print('*获取到播放源：')
    for name, num in ports.items():  # 输出播放源列表
        print(num, name)
    total = int(list(ports.values())[-1])  # 播放源总数
    while True:
        port = str(get_input('>请选择播放源[1，2，3...]： ', total,2))  # 选择播放源
        result=search(port)
        choice = prtres(result)
        detail(choice, port)
        c=input('>是否继续搜索？[y/n] ')
        if c.lower()=='n':
            input('*感谢使用Movie Helper！期待您的下次使用！\n请按[Enter]键退出...')
            break
        elif c.lower()=='y':
            continue

