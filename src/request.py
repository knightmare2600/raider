import urllib2
import zlib
import sys

#
# 	This class is responsible for making URL requsts to the server. 
#	wordlistGen - A wordlist generator object shared between all instances. 
# 	requestedid - A counter to be used by all requests to assign a unique request id
# 	run() - Fetches wor and calls the appopriate header generation algorithm to prepare itself for a response. Sends the request and recieves the response. It then decodes the response if it detects gzip encoding. 
# 	makePostRequest() - Makes the request and returns the urllib2 response
# 	decodeResponse() - Attempts to detect response encoding and decode it if gzip is detected
# 	fetchWord() - Returns the next response from the  wordlist generator object that's stored in wordlistGen (class variable) which is shared between all response instances. If finished raises WordListExhausted exception
#
class Request(object):

	wordlistGen = None
	requestid = 1 

	def __init__(self, argObj, headerObj):
		self.argObj = argObj
		self.headerObj = headerObj
		self.rid = 0

	def run(self):
		self.rid = Request.requestid
		Request.requestid += 1
		self.word = self.fetchWord()
		if self.argObj.debug == None:
			self.headerObj.transformed = self.headerObj.transform(self.word)
		else:
			self.headerObj.transformed = self.headerObj.transform(self.argObj.debug)
		self.headerObj.reqHeaders = self.headerObj.urlParse()
		self.response = Request.makePostRequest(self)
		self.contentDecoded = Request.decodeResponse(self)
	
	def makePostRequest(self):
		reqHeaders = self.headerObj.reqHeaders
		request =  urllib2.Request("http://" + reqHeaders['settings']['Host'] + reqHeaders['url'], reqHeaders['content'], reqHeaders['settings'])
		return urllib2.urlopen(request)

	def decodeResponse(self):
		pass
		if 'gzip' in self.response.headers['Content-Encoding']:
			return zlib.decompress(self.response.read(), 16+zlib.MAX_WBITS)
		else:
			return self.response.read()

	def fetchWord(self):
		try:
			return next(Request.wordlistGen).rstrip('\n')
		except StopIteration:
			print "Wordlist Exhausted\n"
			raise raider.WordListExhausted()
		except:
			raise
