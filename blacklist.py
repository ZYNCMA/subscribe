# -*- coding: utf-8 -*-
# filename: blacklist.py
import urllib2
from basic import Basic

class Blacklist(object):
    def __init__(self):
        pass

    def add(self, accessToken, openId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/tags/members/batchblacklist?access_token=%s" % accessToken
        postData = "{ \"openid_list\": [\"%s\"] }" % openId
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()

    def del(self, accessToken, openId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/tags/members/batchunblacklist?access_token=%s" % accessToken
        postData = "{ \"openid_list\": [\"%s\"] }" % openId
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()

    def get(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/tags/members/getblacklist?access_token=%s" % accessToken
        postData = "{ \"begin_openid\": \"\" }"
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()

if __name__ == '__main__':
    blacklist = Blacklist()
    accessToken = Basic().get_access_token()
    blacklist.get(accessToken)
