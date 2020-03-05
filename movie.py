import requests,webbrowser,prettytable,sys
def init():
    url='https://www.ttupp.com/tv.txt'
    r=requests.get(url)
    r.encoding='GB2312'
    global api,ports
    api=r.json()['远程api']
    ports=r.json()['播放源'][0]

def get_input(text,maxint):
    while True:
        userin=input(text)
        if userin.lower()=='q':
            sys.exit()
        elif userin=='':
            return userin
        if userin.isdecimal()==True:
            if int(userin)<=maxint:
                return int(userin)
        print('您的输入非法，请重新输入！')


def search(keyword,port): #获取搜索结果
    url=api+'?type=search&jiekou='+port+'&value='+keyword
    r=requests.get(url).json()
    data=r['data']
    return data

def prtres(result): #打印搜索结果
    tb=prettytable.PrettyTable(['序号','类型','更新时间','影片名'])
    for i in range(len(result)):
        tb.add_row([i+1,result[i]['sort'],result[i]['time'],result[i]['title']])
    print('共找到搜索结果 '+str(len(result))+' 条：')
    print(tb)
    i=get_input('请输入序号选择： ',len(result))
    return result[i-1]

def detail(choice,port):
    url=api+'?type=video&jiekou='+port+'&value='+choice['url']
    r=requests.get(url).json()
    content=r['data']['content']
    print('已选：【'+choice['title']+' / 共'+str(len(content))+'集】')
    with open('./'+choice['title']+'_DownloadUrl.txt','w') as txt:
        for item in content:
            txt.write(item['url']+'\n')
    print('下载地址获取成功！')
    tb=prettytable.PrettyTable(['序号','剧集名称'])
    for i in range(len(content)):
        tb.add_row([i+1,content[i]['name']])
    print(tb)
    i=get_input('请选择要播放的剧集： ',len(content))
    while True:
        print('\n正在播放： '+choice['title']+content[i-1]['name'])
        webbrowser.open('https://www.m3u8play.com/?play='+content[i-1]['url'])
        t=get_input('控制栏(按q-退出软件，输入序号-换集，留空-切下一集)： ',len(content))
        if t=='':
            if i==len(content):
                print('已经是最后一集！')
                break
            else:i+=1
        else:i=t

if __name__ == "__main__":
    init()
    print('获取到播放源：')
    for name,num in ports.items():
        print(num,name)
    total=int(list(ports.values())[-1])
    port=get_input('请选择播放源（1，2，3...）： ',total)
    keyword=input('请输入搜索关键词： ')
    result=search(keyword,port)
    choice=prtres(result)
    detail(choice,port)
    print('感谢使用本软件！')
