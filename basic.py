# -*- coding: utf-8 -*-
# filename: basic.py
import urllib
import time
import json

class Basic:
    def __init__(self):
        self.__accessToken = ''
        self.__leftTime = 0
        self.__accessTime = 0

    def __real_get_access_token(self):
        appId = "xxxxx"
        appSecret = "xxxxx"

        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
               "client_credential&appid=%s&secret=%s" % (appId, appSecret))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        
        self.__accessToken = urlResp['access_token']
        self.__leftTime = urlResp['expires_in']
        self.__accessTime = time.time()

    def get_access_token(self):
        if self.__leftTime + 10 < time.time() - self.__accessTime:
            self.__real_get_access_token()
        return self.__accessToken

