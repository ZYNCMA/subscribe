# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply
import blacklist
import material
import random

from basic import Basic
GBASIC = Basic()

WHITELIST = ['xxx']

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "hello, this is handle view"
            signature = data.signature
            timestamp = data.timestamp
            nonce = data.nonce
            echostr = data.echostr
            token = "xxx"

            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            if hashcode == signature:
                return echostr
            else:
                return ""
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            print "Handle Post webdata is ", webData

            recMsg = receive.parse_xml(webData)

            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName
            replyMsg = reply.TextMsg(toUser, fromUser, 'I cannot recognize')

            if isinstance(recMsg, receive.Msg):
                if recMsg.MsgType == 'text':
                    content = recMsg.Content
                    replyMsg = reply.TextMsg(toUser, fromUser, content)
                elif recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                else:
                    pass
            elif isinstance(recMsg, receive.EventMsg):
                if recMsg.Event == 'CLICK':
                    if recMsg.EventKey == 'me':
                        mat = material.Material()
                        imageCount = mat.get_count(GBASIC.get_access_token())['image_count']
                        image = mat.batch_get(GBASIC.get_access_token(), 'image', random.randint(0, imageCount), 1)
                        replyMsg = reply.ImageMsg(toUser, fromUser, image['item'][0]['media_id'])
                    elif recMsg.EventKey == 'you':
                        replyMsg = reply.TextMsg(toUser, fromUser, 'of course yes')
                    else:
                        pass
                elif recMsg.Event == 'subscribe':
                    if toUser not in WHITELIST:
                        blacklist.Blacklist().add(GBASIC.get_access_token())
                        replyMsg = reply.TextMsg(toUser, fromUser, 'this is not for you, and you have been added to blacklist, please unsubscribe :)')
                    else:
                        replyMsg = reply.TextMsg(toUser, fromUser, 'nice to meet you :)')
                else:
                    pass
            else:
                pass

            return replyMsg.send()
        except Exception, e:
            return e
