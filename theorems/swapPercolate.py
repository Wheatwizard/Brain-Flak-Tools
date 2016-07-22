from basics import *
import re

'''
swapPercolate moves swaps through parenteses.
swaps are permitted to move left through "(", "<", and "["
e.g.

(<>()) --> <>(())

Because swaps return zero,
swaps are permitted to move left through "]" and ">" aswell.
e.g.

[()]<> --> [()<>]

swapPercolate helps to clump swaps together so that they can be dealt with by swapElim

(The two might be combinable into one simpler function)
'''

def swapPercolate(snippet):
	while re.search("[\(\[<]C[^\)\}>\}]",snippet):
		snippet = snippet.replace("(C)","a")
		snippet = snippet.replace("<C>","c")
		snippet = snippet.replace("[C]","d")
		snippet = snippet.replace("(C","C(")
		snippet = snippet.replace("[C","C[")
		snippet = snippet.replace("<C","C<")

	snippet = snippet.replace("a","(C)")
	snippet = snippet.replace("c","<C>")
	snippet = snippet.replace("d","[C]")

	while re.search("[\]>]C",snippet):
		snippet = snippet.replace(">C","C>")
		snippet = snippet.replace("]C","C]")

	return snippet
