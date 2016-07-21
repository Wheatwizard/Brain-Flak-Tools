from basics import *
import re

'''
swapElim removes two swaps in a row
e.g.

<><>{} --> {}
'''

def swapElim(snippet):
	snippet = snippet.replace("CC","")
	snippet = cleanup(snippet)
	return snippet
