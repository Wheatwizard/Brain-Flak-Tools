from .basics import *
import re

cache = {0:"<()>"}

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
			solutions += [divHardcode(n,m) for m in getPrimeFactors(n)]
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
	#Mini interpreter
	stack = []
	scope = [0]
	for character in snippet:
		if character in "([<":
			scope.append(0)
		elif character == ")":
			stack.append(scope.pop())
			scope[-1] += stack[-1]
		elif character == "]":
			scope[-1] = -scope.pop() + scope[-1]
		elif character == ">":
			scope.pop()
		elif character == "B":
			scope[-1] += stack.pop()
		else: #character == "A"
			scope[-1] += 1
	assert(len(scope) == 1)
	assert(stack == [])
	return scope[0]

def substrings(snippet):
	length = len(snippet)
	return [snippet[i:j+1] for i in range(length) for j in range(i,length)]

def pushPopStackSafe(snippet):
	height = 0
	for character in snippet:
		height += (character == ")") - (character == "B")
		if height < 0: return False
	return height == 0

def valueReduce(snippet):
	result = ""
	matchExpression = "[A\[(<][AB[\]<>()]*[AB\]>]"
	while re.search(matchExpression,snippet):
		location = re.search(matchExpression,snippet).span()
		section = snippet[location[0]:location[1]]
		#Theres got to be a better way to do this
		#I am really tired right now and I'll fix it later
		#I just want it to run
		#Currently I takes the largest balanced substring
		#It finds all the substrings
		#sorts out the unbalanced ones
		#returns the largest
		possibilities = substrings(section)
		possibilities = list(filter(lambda x: len(x) > 0 and balanced(x) and pushPopStackSafe(x),possibilities))
		if possibilities != []:
			largest = max(possibilities, key=len)
			result += snippet[:location[1]].replace(largest, clean(getBF(getValue(largest))))
			snippet = snippet[location[1]:]
		else:
			result += snippet[:location[1]]
			snippet = snippet[location[1]:]
	return result + snippet

if __name__ == "__main__":
	print(valueReduce("[{}AAAA[AAAAA]]AAAAA"))
