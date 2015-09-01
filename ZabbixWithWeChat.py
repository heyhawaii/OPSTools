#coding: utf-8
import urllib2
import json
import sys

'''
拥有企业号后，可以通过本脚本推送消息至关注本企业号的微信会员
这里用作zabbix告警的信息发送
zabbix 传值需要三个参数
1 空
2 空
3 内容
'''

"""
touser	否	成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。特殊情况：指定为@all，则向关注该企业应用的全部成员发送
toparty	否	部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
totag	否	标签ID列表，多个接收者用‘|’分隔。当touser为@all时忽略本参数
msgtype	是	消息类型，此时固定为：text
agentid	是	企业应用的id，整型。可在应用的设置页面查看
content	是	消息内容
safe	否	表示是否是保密消息，0表示否，1表示是，默认0
"""



class WeChatMSG(object):
    def __init__(self,content):
        self.gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'     
        self.gettoken_content = {
                            'corpid' : '企业号',
                            'corpsecret' : '管理组凭证密钥' ,
                            }
        self.main_content = {
                            "toparty":"1",
                            "agentid":"3",
                            "msgtype": "text",
                            "text":{
                            "content":content,
                                    }
                            }
                          
    def get_access_token(self,string):
        token_result = json.loads(string.read())
        access_token=  token_result['access_token']
        return access_token.encode('utf-8')

    def geturl(self,url,data):
        data = self.encodeurl(data)
        response = urllib2.urlopen('%s?%s' % (url,data))
        return response.read().decode('utf-8')
        

    def posturl(self,url,data,isjson = True):
        if isjson:
            data = json.dumps(data)
        response = urllib2.urlopen(url,data)
        return response.read().decode('utf-8')

    def encodeurl(self,dict):
        data = ''
        for k,v in dict.items():
            data += '%s=%s%s' % (k,v,'&')
        return data

if __name__ == '__main__':
    if len(sys.argv) == 4:
        touser,notuse,content = sys.argv[1:]        
    else:
        print 'error segments, now exit'
        sys.exit()
    msgsender = WeChatMSG(content)
    access_token_response = msgsender.geturl(msgsender.gettoken_url, msgsender.gettoken_content)
    access_token =  json.loads(access_token_response)['access_token']
    sendmsg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' % access_token  
    print msgsender.posturl(sendmsg_url,msgsender.main_content)
    
