# -*- coding: utf-8 -*-
# filename: handle.py

import hashlib
import web
import receive
import reply

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
                if recMsg.EventKey == 'CLICK':
                    if recMsg.EventKey == 'me':
                        replyMsg = reply.TextMsg(toUser, fromUser, 'see you soon')
                    elif recMsg.EventKey == 'you':
                        replyMsg = reply.TextMsg(toUser, fromUser, 'of course yes')
                    else:
                        pass
                else:
                    pass
            else:
                pass

            return replyMsg.send()
        except Exception, e:
            return e
