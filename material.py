# -*- coding: utf-8 -*-
# filename: material.py
import urllib2
import json
import poster.encode
from poster.streaminghttp import register_openers
from basic import Basic

class Material(object):
    def __init__(self):
        register_openers()

    def add(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        fileName = "hello"
        param = {'media': openFile, 'filename': fileName}
        #param = {'media': openFile}
        postData, postHeaders = poster.encode.multipart_encode(param)

        postUrl = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=%s" % (accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        print urlResp.read()

    def get(self, accessToken, mediaId, localPath):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print jsonDict
        else:
            buffer = urlResp.read()
            mediaFile = file(localPath, "wb")
            mediaFile.write(buffer)
            print "get successful"

    def del(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s" % accessToken
        postData = "{ \"media_id\": \"%s\" }" % mediaId
        urlResp = urllib2.urlopen(postUrl, postData)
        print urlResp.read()
    

    def get_count(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s" % accessToken
        postData = ""
        urlResp = urllib2.urlopen(postUrl, postData)
        rst = urlResp.read()
        print rst
        return json.loads(rst)

    def batch_get(self, accessToken, mediaType, offset=0, count=1):
        postUrl = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s" % accessToken
        postData = "{ \"type\": \"%s\", \"offset\": %d, \"count\": %d }" % (mediaType, offset, count)
        urlResp = urllib2.urlopen(postUrl, postData)
        rst = urlResp.read()
        print rst
        return json.loads(rst)

if __name__ == '__main__':
    myMaterial = Material()
    accessToken = Basic().get_access_token()
    mediaType = "news"
    myMaterial.batch_get(accessToken, mediaType)
