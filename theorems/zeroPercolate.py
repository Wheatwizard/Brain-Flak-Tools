import re
import basics

def zeroPercolate(snippet):
	while re.search("\(<",snippet):
		location = re.search("\(<",snippet).span()
		end = basics.findMatch(snippet,location[1]-1)
		snippet = snippet[:location[0]] + snippet[location[1]-1:end+1] + "(" + snippet[end+1:]
	return snippet

if __name__ == "__main__":
	print zeroPercolate("CC(<BBBDD>B)")
