from basics import *
import re

#TODO comment this unreadable grabage for godsakes

def reducableModifiers(snippet):
	basicFinder = "(\[<.*>\]|<\[.*\]>)" #The pattern we care about
	finder = re.compile("(?=" + basicFinder +  ").") #Matches the first character of any matches to the pattern
	matches = re.finditer(finder, snippet)
	matches = filter(
		#Let the code through if the start to the end matches the pattern
		lambda x:re.match(
			basicFinder + "$",
			snippet[x.span()[0]:findMatch(snippet,x.span()[0])+1]
		),
		matches
	)
	return matches

def modifierReduce(snippet):
	snippet = snippet.replace("><","")
	snippet = snippet.replace("][","")
	finder = re.compile("[<\[]C*[>\]]")
	while re.search(finder, snippet):
		location = re.search(finder, snippet).span()
		snippet = snippet[:location[0]] + snippet[location[0]+1:location[1]-1] + snippet[location[1]:]
	while reducableModifiers(snippet) != []:
		start = reducableModifiers(snippet)[0].span()[0]
		location = (start, findMatch(snippet,start)+1)
		snippet = snippet[:location[0]] + "<" + snippet[location[0]+2:location[1]-2] + ">" + snippet[location[1]:]
	return snippet

if __name__ == "__main__":
	print modifierReduce(clean("(<[()<{}[()]>]>)"))
