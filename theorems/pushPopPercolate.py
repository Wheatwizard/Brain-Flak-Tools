import re
from basics import *

'''
Find all of the matches that are reducable
'''

def percolablePushPops(snippet):
	matches = re.finditer("\[(?=\(+.+\)+B+])",snippet)
	#If there is nothing but Bs between the match of the [ and the match of the (
	#And there are more or equal matching parentheses than Bs
	#The match is valid
	selec = lambda x: snippet[x.span()[0]:findMatch(snippet,x.span()[0])+1]
	bSize = lambda x: len(re.search("(B+)]$",selec(x)).group(1))
	valid = lambda x: (
		#Might be redundant to the stricter 3rd test
		re.match("B+$",snippet[findMatch(snippet,x.span()[0]+1)+1:findMatch(snippet,x.span()[0])])
		and
		#The lookahead might be unecessary but I left it to match the regex to the one above
		re.match("\[(?="+"\("*bSize(x)+".+"+"\)"*bSize(x)+"B+])",selec(x))
		and
		balanced(selec(x)[bSize(x)+1:-2*bSize(x)-1])
	)
	return filter(valid,matches)


def pushPopPercolate(snippet):
	while percolablePushPops(snippet):
		pPP = percolablePushPops(snippet)[0].span()
		editingArea = snippet[pPP[0]:findMatch(snippet,pPP[0])+1]
		bSize = len(re.search("(B+)]$",editingArea).group(1))
		snippet = snippet[:pPP[0]] + "("*bSize + "[" + editingArea[bSize+1:-2*bSize-1] + "]" + ")"*bSize + "B"*bSize + snippet[findMatch(snippet,pPP[0])+1:]
	return snippet

if __name__ == "__main__":
	print pushPopPercolate("[((((((AAAAA))))))BBBBBBB]")
