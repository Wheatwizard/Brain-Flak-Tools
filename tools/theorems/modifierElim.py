from basics import *
import re

'''
reducableModifiers finds all the modifiers (it can) attempting to modify a zeroed value
'''

def reducableModifiers(snippet):
	#Finding problem
	#Regex for all modifiers, filter out the unbalanced matches, and filter out the irreducable matches
	#The problem is that regex is greedy and it returns the largest it can find we want every example
	#When I fix this it will solve the example in the main (This problem might occur elsewhere as well)
	return filter(
		lambda x:zeroEval(snippet[x.span()[0]:x.span()[1]]),
		filter(
			lambda x:balanced(snippet[x.span()[0]:x.span()[1]]),
			re.finditer("[\[<].*[\]>]",snippet)
		)
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
		location = reducableModifiers(snippet)[0].span()
		#Remove the modifier keep the inside
		snippet = snippet[:location[0]] + snippet[location[0]+1:location[1]-1] + snippet[location[1]:]
 	return snippet

if __name__ == "__main__":
	#TODO make this example work
	print modifierElim(clean("(<(<(<>)>())>)"))
