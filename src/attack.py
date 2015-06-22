import header
import request
import sys

#
#	The attack class implements the logic for each style of attack. The child classes customize any methods to behave correctly. 
#	The sniperclass acts identically to the attack class because development was based around it. 
# 	Each class has the following methods. 
# 	run() - Begin attack, get words, make requets, parse responses etc
# 	debug() - Prints out the example of a specific case passed to it along with key information, useful for troubleshooting
# 	evaluate() - Acts as a switch for success criteria specified in the argObj (command line arguments), and calls failed / response based on success
# 	successfulParse() - Prints out the information in the case of the success criteria being met and stores result in a success list to be printed on completion
#	failedParse() - Prints out information if the response fails to meet nominated criteria. 
#

class Attack(object):
	def __init__(self, argObj):
		raise NotImplementedError	

	def run(self):
		while True:
			try:
				request.Request.wordlistGen = self.wordlistServer()
				self.requestObj = request.Request(self.argObj, self.headerObj)
				if self.argObj.debug is not None:
					self.requestObj.run()
					self.debug()
					sys.exit(0)
				while True:
					self.requestObj.run()
					self.evaluate()
			except WordListExhausted:
				self.headerObj.headerIndex += 1
				if self.headerObj.headerIndex == len(self.headerObj.variationList):
					print "[+] Attack Complete\n"
					if len(self.successList) > 0:
						print "[+] Successful Response Word Summary:"
						for word in self.successList:
							print word
					else:
						print "[+] No instances of successful criteria met"
					sys.exit(0)
			except:
				raise
	
	def debug(self):
		print "[+] DEBUGGING INFORMATION"
		print "[+] Raw Header: " 
		print self.headerObj.rawHeader
		print "[+] Variation: "
		print self.headerObj.variationList[0]
		print "[+] Transformed Header: "
		print self.headerObj.transformed
		print "[+] Request Headers: "
		print self.headerObj.reqHeaders
		print "[+] Success Criteria: " + str(self.argObj.successCriteria)
		print "[+] Success Value: " + str(self.argObj.successValue)
		print "[+] Word sent: %r" % str(self.argObj.debug)
		print "[+] Response Code: " + str(self.requestObj.response.code)
		print "[+] Response Headers: " 
		for elements in self.requestObj.response.headers.items():
			print elements
		print "[+] Response Content:"
		print str(self.requestObj.contentDecoded)
	
	def evaluate(self):
		if self.argObj.successCriteria == 1:
			if self.argObj.successValue in self.requestObj.contentDecoded:
				self.successfulParse()
			else: 
				self.failedParse()
		elif self.argObj.successCriteria == 2:
			if self.argObj.successValue not in self.requestObj.contentDecoded:
				self.successfulParse()
			else: 
				self.failedParse()
		elif self.argObj.successCriteria == 3:
			if self.argObj.successValue > int(self.requestObj.response.headers['Content-Length']):
				self.successfulParse()
			else: 
				self.failedParse()
		elif self.argObj.successCriteria == 4:
			if self.argObj.successValue < int(self.requestObj.response.headers['Content-Length']):
				self.successfulParse()
			else: 
				self.failedParse()
		elif self.argObj.successCriteria == 5:
			if self.argObj.successValue is self.requestObj.response.code:
				self.successfulParse()
			else: 
				self.failedParse()
		elif self.argObj.successCriteria == 6:
			if self.argObj.successValue is not self.requestObj.response.code:
				self.successfulParse()
			else: 
				self.failedParse()
		
	def successfulParse(self):
		print "[+] Size: " + str(self.requestObj.response.headers['Content-Length']) + "\tResponse Code: " + str(self.requestObj.response.code) + "\tReq ID: " + str(self.requestObj.rid) + "\tSuccess!! Fuzz Value: " + self.requestObj.word
		self.successList.append(self.requestObj.word)
		if not self.argObj.stop:
			sys.exit(0)
		
	def failedParse(self):
		print "[-] Size: " + str(self.requestObj.response.headers['Content-Length']) + "\tResponse Code: " + str(self.requestObj.response.code) + "\tReq ID: " + str(self.requestObj.rid)

	def wordlistServer(self):
		with open(self.argObj.wordlist,'r') as f:
			for line in f:
				yield line

class WordListExhausted(Exception):
	pass


class ProngedAttack(Attack):
	def __init__(self, argObj):
		self.argObj = argObj
		self.headerObj = header.ProngedHeader(self.argObj.headerFile)		
		self.successList = list()

class SniperAttack(Attack):
	def __init__(self, argObj):
		self.argObj = argObj
		self.headerObj = header.SniperHeader(self.argObj.headerFile)
		self.successList = list()

