import requests,webbrowser,prettytable,sys,time,os,colorama

def init():  # 初始化
    # 提示语
    colorama.init(True)
    os.system('title Movie Helper[v1] @吾爱破解 lihaisanhui') #设置窗口标题
    print('*欢迎使用Movie Helper[Ver:1.0]！作者：吾爱破解@lihaisanhui')
    print(colorama.Fore.RED+'声明：本软件不生产、储存内容，有关资源均来源于网络，作者不为其中内容负法律责任\n仅供论坛会员学习交流，请于下载后24小时内删除，请勿用于商业用途！！！\n')
    # 从服务器获取api接口、播放源数据
    url = 'https://www.ttupp.com/tv.txt'
    r = requests.get(url)
    r.encoding = 'GB2312'
    global api, ports
    api = r.json()['远程api']
    ports = r.json()['播放源'][0]


def get_input(text, maxint):  # 用户输入判断
    while True:
        userin = input(text)
        if userin.lower() == 'q':  # 输入q退出程序
            sys.exit()
        elif userin == '':
            return userin
        if userin.isdecimal() == True:  # 判断输入是否合法，以免发生错误
            if int(userin) <= maxint:
                return int(userin)
        print(colorama.Back.RED+'*您的输入非法，请重新输入！')


def search(port):  # 获取搜索结果
    while True:
        keyword = input('>请输入搜索关键词： ')
        url = api+'?type=search&jiekou='+port+'&value='+keyword  # 拼接api
        r = requests.get(url).json()  # 返回json
        if r['code']==200:
            data = r['data']  # 搜索结果
            return data
        else:print(colorama.Back.RED+'*发生错误['+str(r['code'])+']，错误信息：'+r['msg'])


def prtres(result):  # 打印搜索结果
    # 输出表格
    tb = prettytable.PrettyTable(['序号', '类型', '更新时间', '影片名'])
    for i in range(len(result)):
        tb.add_row([i+1, result[i]['sort'], result[i]
                    ['time'], result[i]['title']])
    #提示用户选择
    print('*共找到搜索结果 '+str(len(result))+' 条：')
    print(tb)
    i = get_input('>请输入序号选择： ', len(result))  # 返回用户选择
    return result[i-1]


def detail(choice, port):  # 获取播放地址
    #获取数据
    url = api+'?type=video&jiekou='+port+'&value='+choice['url']  # 拼接api
    r = requests.get(url).json()  # 返回json
    content = r['data']['content']
    print(colorama.Back.GREEN+'*已选：【'+choice['title']+' / 共'+str(len(content))+'集】')

    # 写入下载地址
    with open('./'+choice['title']+'_DownloadUrl.txt', 'w') as txt:  
        for item in content:
            txt.write(item['url']+'\n')
    print('*下载地址获取成功！')

    # 以表格形式输出剧集列表
    tb = prettytable.PrettyTable(['序号', '剧集名称'])  
    for i in range(len(content)):
        tb.add_row([i+1, content[i]['name']])
    print(tb)

    # 播放视频
    i = get_input('>请选择要播放的剧集： ', len(content))
    while True:  # 播放时循环
        print(colorama.Back.GREEN+'\n*正在播放： '+choice['title']+' ['+content[i-1]['name']+']')
        print('    *正在用默认浏览器打开播放页！')
        time.sleep(1)
        webbrowser.open('https://www.m3u8play.com/?play=' + content[i-1]['url'])  # 浏览器打开播放地址
        t = get_input('    >控制栏[输入q-退出软件，输入序号-换集，留空-切下一集]： ', len(content))
        if t == '':
            if i == len(content):
                print(colorama.Back.RED+'*已经是最后一集！')
                break
            else:i += 1
        else:i = t

if __name__ == "__main__": #程序入口
    init() #初始化

    print('*获取到播放源：')
    for name, num in ports.items():  # 输出播放源列表
        print(num, name)
    total = int(list(ports.values())[-1])  # 播放源总数
    port = str(get_input('>请选择播放源（1，2，3...）： ', total))  # 选择播放源
    if port == '':port = '1'  # 如输入为空，默认源1

    result=search(port)
    choice = prtres(result)
    detail(choice, port)
    input('*感谢使用本软件！请按[Enter]键退出...')
