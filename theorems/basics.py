import re

'''
atomize will go through a code fragment and split up pieces that are not of the same scope
e.g.
(())<>{{}{}<>}
becomes
(())
<>
{{}{}<>}
'''
def atomize(fragment):
	building = ""
	currentScope = ""
	for character in fragment:
		building += character
		currentScope += character
		if len(currentScope) > 1 and complement(currentScope[-1]) == currentScope[-2]:
			currentScope = currentScope[:-2]
		building += '\n' if currentScope == "" else ''
	if currentScope != "":
		print "Broken fragment or uneven braces"
	return building[:-1]

def complement(character):
	dict = {"(":")","{":"}","<":">","[":"]",")":"(","}":"{",">":"<","]":"["}
	return dict[character]

def findMatch(snippet, index):
	increment = 1 if snippet[index] in "({<[" else -1
	stack = []
	if snippet[index] in "(){}<>[]":
		stack.append(snippet[index])
	while len(stack) > 0 and index + increment < len(snippet):
		index += increment
		if snippet[index] in "(){}<>[]":
			if complement(snippet[index]) == stack[-1]:
				stack = stack[:-1]
			else:
				stack.append(snippet[index])
	return index

def balanced(snippet):
	stack = []
	#Remove all non brace characters
	snippet = re.sub("[^\(\)\{\}<>\[\]]","",snippet)
	if snippet == "":
		return True
	if snippet[0] in ")}>]":
		return False
	for character in snippet:
		if character in "({<[":
			stack.append(character)
		if character in ")}>]":
			#TODO make this stricter
			if stack == []:
				return False
			stack = stack[:-1]
	return stack == []

def clean(string):
	string = re.sub("[^\(\)\[\]{}<>]","", string)
	string = string.replace("()","A")
	string = string.replace("{}","B")
	string = string.replace("<>","C")
	string = string.replace("[]","D")
	return string

def flesh(string):
	string = string.replace("A","()")
	string = string.replace("B","{}")
	string = string.replace("C","<>")
	string = string.replace("D","[]")
	return string

def zeroed(stack):
	for brace in stack[::-1]:
		if brace == "<":
			return True
		if brace == "(":
			return False
	return True
'''
zeroReturn determines where in the string value is important.
It returns a list of booleans where each boolean corresponds to a character in the string
'''
def zeroReturn(string):
	stack = []
	result = []
	for character in string:
		if character in ")}>]":
			stack = stack[:-1]
		result.append(zeroed(stack))
		if character in "({<[":
			stack.append(character)
	return zip(result,string)

def cleanup(snippet):
	while re.search("(<>|\[\])",snippet):
		snippet = snippet.replace("<>","")
		snippet = snippet.replace("[]","")
	snippet = snippet.replace("{}","{A}")
	snippet = snippet.replace("()","(<A>)")
	return snippet

'''
Takes a snippet of code and decides if it returns zero or an unknown
'''

def zeroEval(snippet):
	assert balanced(snippet)

	#Pops after a loop (always zero) are ignored
	snippet = re.sub("B(?=[^B\)C]*\})","F",snippet[::-1])[::-1] #We denote zeroed pops with an "F"

	#Any code in between "<" and ">" will be zeroed and is irrelevant
	snippet = re.sub("<.*>","CC",snippet)

	#Remove all pushes because they cannot interfere with the value of the statement
	snippet = re.sub("[\(\)]","",snippet)

	#TODO use value Reduce and percolate

	#We will permit monads, "C", and "F" because they do not change the value
	return re.search("[^\(\)\{\}<>\[\]CF]",snippet) == None
