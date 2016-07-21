from basics import *
import re

'''
reducableModifiers finds all the modifiers (it can) attempting to modify a zeroed value
'''

def reducableModifiers(snippet):
	#Regex for all modifiers, filter out the unbalanced matches, and filter out the irreducable matches
	pattern = "<" #Matches the opening brace for a "<>" or "[]" monad
	return filter(
		#If the code from the open to its match is nonzero it is filtered out
		lambda x:zeroEval(snippet[x.span()[0]+1:findMatch(snippet,x.span()[0])]),
		re.finditer(pattern,snippet)
	)

'''
ModifierElim removes value modifiers ("<>" and "[]") that serve no purpose

It removes either modifiers that are in a zeroed context
e.g.

<({})> --> ({})

or modifiers modifying a already zeroed value
e.g

[(<>)] --> (<>)
'''

def modifierElim(snippet):
	zeroData = zeroReturn(snippet)
	if zeroData == []: return ""
	#Filter out zeroed modifiers
	zeroData[:] = [x for x in zeroData if not (x[0] and x[1] in "[]<>")]
	snippet = cleanup(reduce(lambda x,y:x+y,zip(*zeroData)[1]))
	#Value modifiers wrapped around a already zeroed value have no effect
	while reducableModifiers(snippet) != []:
		start = reducableModifiers(snippet)[0].span()[0]
		location = (start, findMatch(snippet,start)+1)
		#Remove the modifier keep the inside
		snippet = snippet[:location[0]] + snippet[location[0]+1:location[1]-1] + snippet[location[1]:]
 	return snippet

if __name__ == "__main__":
	print modifierElim(clean("(<(<(<>)>())>)"))
