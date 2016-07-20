from basics import *
import re

'''
Find all of the matches that are reducable
'''

def reducableNegatives(snippet):
	matches = re.finditer("\[[^\[]*\[",snippet)
	#Matches that are balanced between the "["s are reduceable
	valid = lambda x: balanced(snippet[x.span()[0]+1:x.span()[1]-1])
	return filter(valid,matches)

'''
NegativeReduce cancels out negative modifiers

A negative within a negative is the same as a positive
e.g.

([[()]]) --> (())

Other more complicated cancelations can be done as well
e.g.

([[{}]()]) --> ({}[()])

'''

def negativeReduce(snippet):
	#This can be made more powerful in the future
	#Perhaps this can be combined with modifier reduce
	while reducableNegatives(snippet) != []:
		location = reducableNegatives(snippet)[0].span()
		end = findMatch(snippet,location[1]-1)
		snippet = snippet[:location[1]-1] + "]" + snippet[location[1]:end] + "[" + snippet[end+1:]
	return cleanup(snippet)

if __name__ == "__main__":
	print negativeReduce(clean("[()[()[()]()]()]"))
	print negativeReduce(clean("[()[()[()]]]"))
