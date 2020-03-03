import requests,webbrowser,prettytable
def search(keyword,port): #获取搜索结果
    url='http://api.ttupp.com/cgi/qingfeng?type=search&jiekou='+port+'&value='+keyword
    r=requests.get(url).json()
    data=r['data']
    return data

def prtres(result): #打印搜索结果
    tb=prettytable.PrettyTable(['序号','类型','更新时间','影片名'])
    for i in range(len(result)):
        tb.add_row([i+1,result[i]['sort'],result[i]['time'],result[i]['title']])
    print('共找到搜索结果 '+str(len(result))+' 条：')
    print(tb)
    i=int(input('请输入结果前的序号选择： '))
    return result[i-1]

def detail(choice,port):
    url='http://api.ttupp.com/cgi/qingfeng?type=video&jiekou='+port+'&value='+choice['url']
    r=requests.get(url).json()
    content=r['data']['content']
    print('已选：【'+choice['title']+' / 共'+str(len(content))+'集】')
    tb=prettytable.PrettyTable(['序号','剧集名称'])
    for i in range(len(content)):
        tb.add_row([i+1,content[i]['name']])
    print(tb)
    while True:
        i=int(input('请输入剧集对应的序号选集： '))
        webbrowser.open(content[i-1]['url'])
        input('请不要关闭窗口，播放完后按Enter继续！')

if __name__ == "__main__":
    keyword=input('请输入搜索关键词： ')
    port=input('请选择需要调用的接口（1，2，3）： ')
    result=search(keyword,port)
    choice=prtres(result)
    detail(choice,port)
