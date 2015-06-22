import string
import re

#
#	headerFile (variable - string): the file path given by the runtime arguments of the hedear file. 
#	rawHeader (variable - string): the raw header file read in unaltered
#	variationList (variable - list. sub-element - string): the modified raw header with only one marker per variation
# 	reqHeaders (variable - list. sub-element - dictionary): the processed variation header suitable for urllib2 calling. See: reqHeaders (sub)
#	reqHeaders (sub) (variable - dictionary. sub-element - string / dictionary): Has components method (POST / GET etc), url (Request URL), http (HTTP Version), 
#																				 settings (Header settings), content (string of content)
#	variationGen (function): Parses raw headers for markers and creates every variation with one marker per variation. Use in sniper attacks for subsequent requests.
# 	transform (function): Inserts the chosen replacement word(s) into the request markers
#	urlParse (function): Parses each variation created by variationGen to format them in a way that's suitable for urllib2 requests. See: reqHeaders
#

class Header(object):
	def __init__(self, headerFile):
		self.headerFile = headerFile
		try:
			self.rawHeader = open(headerFile,'r').read()
		except:
			print "Error, could not open file"
			raise
		self.variationList = self.variationGen()
		self.headerIndex = 0
		self.transformed = None
		self.reqHeaders = None
		
	def variationGen(self):
		variationList = list()
		markerCount = len(string.splitfields(self.rawHeader, sep="^%"))
		for marker in range(1,markerCount,2):
			splitString = string.splitfields(self.rawHeader, sep="^%")
			splitString[marker] = ''.join(('^%',splitString[marker],'^%'))
			splitString = ''.join(splitString)
			variationList.append(splitString)
		return variationList

	def transform(self, word):
		rawHeader = self.variationList[self.headerIndex]
		splitString = string.splitfields(rawHeader, sep="^%")
		splitString[1] = word
		return ''.join(splitString)	

	def urlParse(self):
		variation = self.transformed
		headerMethod, headerURL, headerHTTP = variation.partition('\r\n')[0].split(' ')
		headerSettings = re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n", variation)
		headerContent = variation.partition('\r\n\r\n')
		index = next((i for i, sublist in enumerate(headerSettings) if "Content-Length" in sublist), -1)	# Content Length not needed, urllib2 calculates
		headerSettings = headerSettings[:index]
		headerDict = {element[0]: element[1] for element in headerSettings}

		parsed = dict()
		parsed['method'] = headerMethod
		parsed['url'] = headerURL
		parsed['http'] = headerHTTP
		parsed['settings'] = headerDict 
		parsed['content'] = headerContent[2].rstrip('\r\n')
		return parsed

class SniperHeader(Header):
	pass

class ProngedHeader(Header):
	def variationGen(self):
		variationList = list()
		variationList.append(self.rawHeader)
		return variationList
	
	def transform(self, word):
		wordlist = word.split(' ')
		rawHeader = self.variationList[self.headerIndex]
		splitString = string.splitfields(rawHeader, sep="^%")
		markerIndex = 1
		for element in wordlist:
			try:
				splitString[markerIndex] = element
				markerIndex += 2
			except IndexError:
				print "[+] WARNING: A IndexError was caught and ignored. Most likely this entry had a ' ' in it"
				pass
		return ''.join(splitString)
