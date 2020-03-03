import requests,webbrowser,prettytable
def search(keyword,port='1'): #获取搜索结果
    url='http://api.ttupp.com/cgi/qingfeng?type=search&jiekou='+port+'&value='+keyword
    r=requests.get(url).json()
    data=r['data']
    return data

def prtres(data): #打印搜索结果
    tb=prettytable.PrettyTable(['序号','类型','更新时间','片名'])
    for i in range(len(data)):
        tb.add_row([i+1,data[i]['sort'],data[i]['time'],data[i]['title']])
    print('共找到搜索结果 '+str(len(data))+' 条：')
    print(tb)
    i=int(input('请输入你选择的序号： '))
    return data[i-1]['url']

def detail(value,port='1'):
    url='http://api.ttupp.com/cgi/qingfeng?type=video&jiekou='+port+'&value='+value
    r=requests.get(url).json()
    content=r['data']['content']
    print(content)
    print('111')

detail(prtres(search('谍影重重')))
