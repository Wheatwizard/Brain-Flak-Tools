from basics import *
import re

'''
reducablePushes finds all regex matches in with a zeroReturn at the start

This will return a list of zeros that are reducable
'''

def reducableZeros(snippet):
	zeroData = zeroReturn(snippet)
	return filter(lambda x: zeroData[x.span()[0]][0],re.finditer("[^\(\{<\[][\(<\[AB]*<A>",snippet))

'''
zeroReduce makes pushing zeros to the stack more effective

It does this by capturing and zeroing zero returning code segments

e.g.
 {}(<><>)  -->   (<{}>)

({}(<><>)) --> ({}(<><>))
'''

def zeroReduce(snippet):
	while reducableZeros(snippet) != []:
		location = reducableZeros(snippet)[0].span()
		start = findMatch(snippet,location[0])
		snippet = (snippet[:start] +                        #Everything before the effected area
		           snippet[location[0]+1:location[1]-3] +   #Everything between the first character and the "<A>" (exclusive)
		           "<" +                                    #Open zeroer
		           snippet[start:location[0]+1] +           #Everything between the first character and its match (inclusive)
		           ">" +                                    #Close zeroer
		           snippet[location[1]:]                    #Everything after the effected ares
		)
	return snippet

if __name__ == "__main__":
	snippet = clean("<>(<><>)")
	print zeroReduce(snippet)
