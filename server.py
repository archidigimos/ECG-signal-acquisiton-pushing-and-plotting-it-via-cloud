from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

import random
webClients={}
client=0;
class MyServerProtocol(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
			print("Text message received: {0}".format(payload.decode('utf8')))
			if payload[0]=="E":
				for key in webClients:
					#print "sending to "+ str(webClients)
					webClients[key].sendMessage(payload[1:])

			if payload[0]=="W":
				#print "adding webclient"
				n=random.randint(1,1000000)
				for i in webClients:
					if str(n)==i:
						n=random.randint(1,1000000)
				webClients[str(n)]=self
				


        # echo back message verbatim
        #self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://10.124.195.10:80")
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    # note to self: if using putChild, the child must be bytes...

    reactor.listenTCP(80, factory)
    reactor.run()
