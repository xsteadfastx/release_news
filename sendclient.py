import xmpp
import sys 
import time

def sendmessage(fromjid, password, tojid, message):
        jid=xmpp.protocol.JID(fromjid)
        cl=xmpp.Client(jid.getDomain(),debug=[])

        con=cl.connect()
        if not con:
                #print 'could not connect!'
                sys.exit()
        #print 'connected with',con
        auth=cl.auth(jid.getNode(),password,resource=jid.getResource())
        if not auth:
                #print 'could not authenticate!'
                sys.exit()
        #print 'authenticated using',auth

        #cl.SendInitPresence(requestRoster=0)
        id=cl.send(xmpp.protocol.Message(tojid,message))
        #print 'sent message with id',id

        time.sleep(1)

        cl.disconnect()

#sendmessage('newz@xsteadfastx.org','n3wz','marvin@xsteadfastx.org','foo bar')
