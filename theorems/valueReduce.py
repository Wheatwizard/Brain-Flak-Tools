from basics import *
import re

cache = {}

def isTriangular(n):
	#Triangles must be between sqrt(2n) and cbrt(2n)
	for x in range(int((2*n)**(1/3.)),int((2*n)**.5)+1):
		if (x**2+x) == 2*n:
			return True
	return False

def getTriangle(n):
	#Triangles must be between sqrt(2n) and cbrt(2n)
	for x in range(int((2*n)**(1/3.)),int((2*n)**.5)+1):
		if (x**2+x) == 2*n:
			return x
	#If we don't find one we made a mistake
	assert False

def isPrime(n):
	return not [0 for x in range(2,int(n**.5)+1) if n%x==0] and n>1

def getPrimeFactors(n):
	return [x for x in range(2,n/2) if n%x==0 and isPrime(x)]

def divHardcode(n,m):
	assert n%m == 0
	return "("*(m-1)+getBF(n/m)+")"*(m-1)+"{}"*(m-1)

def getSimpleBF(n):
	if n in cache:return cache[n]
	if n < 0:
		return "["+getSimpleBF(-n)+"]"
	elif n == 0:
		return ""
	elif n < 6:
		return "()"*n
	else:
		#Non-edge cases
		solutions = []
		if n >= 78 and isTriangular(n):
			solutions.append(min(["(("+getBF(getTriangle(n))+"){({}[()])}{})","("+getBF(getTriangle(n)+1)+")({({}[()])}{})"],key=len))
		if isPrime(n):
			return getSimpleBF(n-1) + "()"
		else:
			solutions += map(lambda m:divHardcode(n,m),getPrimeFactors(n))
			return min(solutions,key=len)

def getBF(n):
	if n in cache: return cache[n]
	result = getSimpleBF(n)
	index = n - 1
	while index > n-(len(result)/2):
		score = getSimpleBF(index)+getSimpleBF(n-index)
		if len(score) < len(result):result = score
		index -= 1
	index = n + 1
	while index < n+(len(result)/2):
		score = getSimpleBF(index)+getSimpleBF(n-index)
		if len(score) < len(result):result = score
		index += 1
	cache[n] = result
	return result

def getValue(snippet):
	assert balanced(snippet)
	while re.search("<",snippet):
		location = re.search("<",snippet).span()
		snippet = snippet[:location[0]] + snippet[findMatch(snippet,location[0])+1:]
	snippet = snippet.replace("A","()")
	atoms = filter(lambda x:x!="",atomize(snippet).split("\n"))
	sum = 0
	for atom in atoms:
		if atom == "()":
			sum += 1
		elif atom[0] == "[" and atom[-1] == "]":
			sum -= getValue(atom[1:-1])
	return sum

def substrings(snippet):
	length = len(snippet)
	return [snippet[i:j+1] for i in xrange(length) for j in xrange(i,length)]

def valueReduce(snippet):
	result = ""
	while re.search("[A\[\]<>]{2,}",snippet):
		location = re.search("[A\[\]<>]{2,}",snippet).span()
		section = snippet[location[0]:location[1]]
		#Theres got to be a better way to do this
		#I am really tired right now and I'll fix it later
		#I just want it to run
		#Currently I takes the largest balanced substring
		#It finds all the substrings
		#sorts out the unbalanced ones
		#returns the largest
		possibilities = substrings(section)
		possibilities = filter(balanced,possibilities)
		#Filter out empty strings
		possibilities = filter(lambda x:x!="",possibilities)
		if possibilities != []:
			largest = max(possibilities, key=len)
			result += snippet[:location[1]].replace(largest, clean(getBF(getValue(largest))))
			snippet = snippet[location[1]:]
		else:
			result += snippet[:location[1]]
			snippet = snippet[location[1]:]
	return result + snippet

if __name__ == "__main__":
	print valueReduce("[{}AAAA[AAAAA]]AAAAA")
