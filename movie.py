import requests,webbrowser,prettytable,chardet
def init():
    url='https://www.ttupp.com/tv.txt'
    r=requests.get(url)
    r.encoding='GB2312'
    global api,ports
    api=r.json()['远程api']
    ports=r.json()['播放源'][0]

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
    i=int(input('请输入序号选择： '))
    return result[i-1]

def detail(choice,port):
    url=api+'?type=video&jiekou='+port+'&value='+choice['url']
    r=requests.get(url).json()
    content=r['data']['content']
    print('已选：【'+choice['title']+' / 共'+str(len(content))+'集】')
    tb=prettytable.PrettyTable(['序号','剧集名称'])
    for i in range(len(content)):
        tb.add_row([i+1,content[i]['name']])
    print(tb)
    i=input('请输入要下载的集数： ')
    with open('./'+choice['title']+'_DownloadUrl.txt','a') as txt:
        for item in content[:int(i)]:
            txt.write(item['url']+'\n')
    print('下载地址获取成功！已输出到当前目录下的 '+choice['title']+'_DownloadUrl.txt')
if __name__ == "__main__":
    init()
    print('获取到播放源：')
    for name,num in ports.items():
        print(num,name)
    port=input('请选择播放源（1，2，3...）： ')
    keyword=input('请输入搜索关键词： ')
    result=search(keyword,port)
    choice=prtres(result)
    detail(choice,port)

