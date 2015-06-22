#!/usr/bin/python
import argparse
from src import attack
from src import header
from src import header 
import sys

#
#	This class is treated like a struct to pass information in a convinent object from the command line interface into defining request behaviour. 
#	Stager is a simple switch like statement to call the appropriate object
#	WordlistServer is used to create a generator for the request class that is shared between all instances of request (ensuring each word only gets checked once)
#	WordListExhausted is used to catch exception when the wordlist generator has reached it's end

class ArgList(object):
	def __init__(self):
		self.wordlist = None
		self.headerFile = None
		self.successCriteria = None
		self.successValue = None
		self.stop = False
		self.debug = None 
		self.attack = None

def stager(argObj):
	if argObj.attack == 1:
		sniperObj = attack.SniperAttack(argObj)
		sniperObj.run()
	elif argObj.attack == 2:
		prongedObj = attack.ProngedAttack(argObj)
		prongedObj.run()

def wordlistServer(wordlist):
	with open(wordlist,'r') as f:
		for line in f:
			yield line

class WordListExhausted(Exception):
	pass

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description='Designed to attack customized header requests')
parser.add_argument("-w","--wordlist", help="Select the wordlist you wish to use for the attack\n\n")
parser.add_argument("-H","--header", help="Select the header file to attack\n\n")
parser.add_argument("-s","--success", type=int, help="Success criteria.\n(1) Keyword Present \n(2) Keyword Not Present \n(3) Greater than Size \n(4) Smaller than Size\n(5) Response code recieved \n(6) Response code avoided\n\n",choices=[1,2,3,4,5,6])
successgroup = parser.add_mutually_exclusive_group()
successgroup.add_argument("-k","--keyword", help="Keyword existing / not existing will define success\n\n")
successgroup.add_argument("-z", "--size", type=int, help="Minimum / maximum content-length of response to determine success\n\n")
successgroup.add_argument("-r", "--response", type=int, help="Response Code to obtain / avoid to determine success\n\n")
parser.add_argument("-n","--nostop", help="If set it will continue testing all values instead of stopping at the first success\n\n", action="store_true", default=False)
parser.add_argument("-d","--debug", help="--debug will process the single entry given and print detailed header responese. This should simulate 1 line in your file\n")
parser.add_argument("-a","--attack", type=int, help="Type of attack desired. \n(1) Sniper - Replace each marker sequentially once the previous position's enumeration has been exhausted.\n(2) Pronged Attack - Will replace multiple markers at once with values marked seperated by space in the wordlist.\nI.e. 'username password' would replace a username marker and password marker at the same time.\n\n", choices=[1,2])

args = parser.parse_args()

if args.wordlist == None or args.header == None or args.success == None or args.attack == None:
	print "[+] Error, mandatory command line options not specified. Please see --help"
	sys.exit(0)

if args.success == 1 or args.success == 2:
	value = args.keyword
elif args.success == 3 or args.success == 4:
	value = args.size
elif args.success == 5 or args.success == 6:
	value = args.response
else:
	print "[+] Invalid success criteria specified. Please see --help"
	sys.exit(0)

argObj = ArgList()
argObj.wordlist = args.wordlist
argObj.headerFile = args.header
argObj.successCriteria = args.success
argObj.successValue = value
argObj.stop = args.nostop
argObj.debug = args.debug
argObj.attack = args.attack

stager(argObj)
