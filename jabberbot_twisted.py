# -*- coding: utf-8 -*-

__author__ = "Yoan Blanc <yoan at dosimple dot ch>"
__revision__ = "20071110"
__license__ = "MIT"

# Twisted Imports
from twisted.words.protocols.jabber import client, jid
from twisted.words.xish import domish, xmlstream
from twisted.internet import reactor

class JabberBot(object):
	"""Basic jabber bot"""
	
	def __init__(self, jid, password, servername=None, reactor=reactor, port=5222, resource="JabberBot"):

                if not servername:
                    servername = jid[jid.find('@')+1:]
                    print("servername: %s", servername)
 
		self.jabberid = jid
		self.password = password
		self.servername = servername
		self.port = port
		self.resource = resource
		
		# internal values
		self._jid = None
		self._factory = None
		self._reactor = reactor
		self._resource = None
		self._xmlstream = None
		self.tryandregister = 1
	

	def run(self):
		self.__initFactory()
	
	def __repr__(self):
		return "<%s (%s)>" % (type(self).__name__, self.jabberid)
	
	def __initFactory(self):
		self._jid = jid.JID("%s/%s" % (self.jabberid, self.resource))
		self._factory = client.basicClientFactory(self._jid, self.password)
		
		self._factory.addBootstrap('//event/stream/authd', self._authd)
		
		self._reactor.connectTCP(self.servername, self.port, self._factory)
		self._reactor.run() 
	
	def _authd(self, xmlstream):
		if xmlstream:
			self._xmlstream = xmlstream
			
			# set it as online
			self._presence = domish.Element(('jabber:client', 'presence'))
			self._presence.addElement('status').addContent('Online')
			self._xmlstream.send(self._presence)

			self.__initOnline()
	
	def __initOnline(self):
		self._xmlstream.addObserver('/message', self._gotMessage)
		self._xmlstream.addObserver('/*', self._gotSomething)
	
	def _gotSomething(self, el):
		for e in el.elements():
			if e.name == "body":
				body = unicode(e.__str__())
				break
	
	def _gotMessage(self, el):
		"""called when a message is received"""
		from_id = el["from"]
		try:
			from_id, resource = from_id.split("/", 1)
		except:
			resource = None
	
		body = "empty"
		for e in el.elements():
			if e.name == "body":
				body = unicode(e.__str__())
				break
		
		self.gotMessage(from_id, body, resource)
	
	def gotMessage(self, jid, body, resource):
		raise NotImplementedError, "Please use gotMessage to treat the incoming message"
	
	def sendMessage(self, to, body):
		message = domish.Element(('jabber:client','message'))
		message["to"] = jid.JID(to).full()
		message["from"] = self._jid.full()
		message["type"] = "chat"
		message.addElement("body", "jabber:client", body)
		
		self._xmlstream.send(message)

