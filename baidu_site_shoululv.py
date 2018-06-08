#coding:utf8
# 批量查询url收录并计算收录率  开发者：李亚涛 wx:841483350
import requests,time,MySQLdb
conn=MySQLdb.connect(host="localhost",user="root",passwd="",db="fang_dict",port=3306,charset="utf8")
cursor=conn.cursor()
def get_baidu_html(url):
    yishoulu=open('yishoulu.txt','a')
    weishoulu=open('weishoulu.txt','a')
    baiduurl="http://www.baidu.com/s?wd=%s"%url
    while 1:
        try:
            html=requests.get(baiduurl).content
            if "没有找到该URL。您可以直接访问" in html:
                print url,"未收录".decode('utf8')
                weishoulu.write(url+'\n')
                # time.sleep(1)
                return 0
            elif "请检查您的输入是否正确" in html:
                print url,"未收录".decode('utf8')
                weishoulu.write(url+'\n')
                # time.sleep(1)
                return 0
            else:
                print url,"成功收录".decode('utf8'),time.ctime()
                yishoulu.write(url+'\n')
                return 1
        except:
            pass

def get_urls():  #获取URL列表的函数
    urls=[]
    # if cursor.execute("select xiaoqu_url from ershoufang WHERE city ='长沙'"): #小区URL
    if cursor.execute("select xinfang_url from loupan WHERE city ='长沙'"): #楼盘
        data=list(cursor.fetchall())
        # print len(data)
        # print data
        for x in range(0,len(data)):
            # print data[x][0]
            urls.append(data[x][0])
        # urls=open("urls.txt",'r').readlines()
        return urls

def get_shoululv():
    urls=get_urls()
    oknum=0
    lostnum=0
    for url in urls:
        if get_baidu_html(url.strip()):
            oknum+=1
        else:
            lostnum+=1
    print '\n共检测URL：'.decode('utf8'),oknum+lostnum,'个'.decode('utf8'),'\n','百度已收录:'.decode('utf8'),oknum,'个\n'.decode('utf8'),'百度未收录'.decode('utf8'),lostnum,'个\n'.decode('utf8'),"收录率：".decode('utf8') ,float(oknum)/(oknum+lostnum)*100,'%'

if __name__=="__main__":
    get_shoululv()
   
