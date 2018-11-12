# -*- coding: utf-8 -*-
from subprocess import call
from subprocess import check_output, CalledProcessError
import sys
import re

checkCommand = "python "+"innerWorkings/pcfg_parse_gen.py "+"-i "+"-g "+'"innerWorkings/*.gr" < '#'innerWorkings/example_sentences.txt'

def createTreeFromOutputPrint(out):
	#print ("Enter: "+out)
	input = out.strip()
	foundParen = False
	if input[0] == "(":
		foundParen = True
		input = input[1:]
	if len(input) > 0 and input[-1] == ")":
		foundParen = True
		input = input[:-1]
	if not foundParen:
		#print ("Exit")
		return Tree(input)
	inputs = splitInputAtSpaceNotWithinParenthesis(input)
	if len(inputs) == 0: return None
	toReturn = Tree(inputs[0])
	for a in inputs[1:]:
		toAdd = createTreeFromOutputPrint(a)
		toReturn.addChild(toAdd)
	#print("Exit")
	return toReturn

def splitInputAtSpaceNotWithinParenthesis(input):
	toReturn = []
	curString = ""
	parenCount = 0
	for a in input:
		curString += a
		if a == "(": parenCount+=1
		elif a == ")": parenCount-=1
		elif a.isspace():
			if parenCount == 0:
				curString = curString.strip()
				if len(curString) > 0:
					toReturn.append(curString)
					curString = ""
	return toReturn

def countSize(inTree):
	if inTree == None: return 0
	if len(inTree.children) == 0:
		toReturn = len(inTree.value) + 1
		inTree.size = toReturn
		return toReturn
	else:
		toReturn = max(len(inTree.value), sum( map(countSize,inTree.children)  ) )
		inTree.size = toReturn
		return toReturn

def nSpaces(n,dots=False):
	toReturn = ""
	for a in range(n):
		toReturn = toReturn + ("≈" if dots else " ")
	return toReturn

def compressList(l):
	return [item for sublist in l for item in sublist] #this apparently turns [[a],[b,c]] -> [a,b,c]

def treeToHorizontal(inTree):
	toReturn = [ [inTree] ]
	#theLambda = lambda x : filter(None,x.children)
	while True:
		nextLayer = compressList( map(lambda x: [None] if len(x.children)==0 else x.children,filter(None,toReturn[-1])) )
		#filter(None, compressList( map(lambda x:x.children,toReturn[-1]) )) #^^^
		if len(filter(None,nextLayer))==0: break #No more children to add
		else: toReturn.append(nextLayer)
	return toReturn


def printTree(inTree):
	if inTree == None: return
	horiz = treeToHorizontal(inTree)
	maxSize = max(map(lambda x : len(x.value) if x is not None else 0,compressList(horiz)))+5
	for h in horiz:
		toPrint = ""
		prevT = None #we'll link children of the same parents with dots instead of parents to emphasize relations.
		curSpaces = 0
		for t in h:
			if t is None:
				#print("YOWZA")
				toPrint = toPrint + nSpaces(maxSize,False)
				continue
			useDots = prevT is not None and t.parent==prevT.parent
			startingSpaces = maxSize - len(t.value)
			toPrint = toPrint + nSpaces(startingSpaces,useDots) + t.value
			prevT = t
		print(toPrint)

class Tree(object):
	def __init__(self,val):
		self.value = val
		self.children = []
		self.size = 0
		self.parent = None

	def addChild(self,val):
		self.children.append(val)
		if val is not None:
			val.parent = self



def getCheckOutput(input = 'innerWorkings/stringWrapper.txt'):
	#For some reason, check_output does not capture all outputs.  In particular, it does not capture the "#No Parses Found For..." suff.
	#and for some reason that is still printed.  However, all of the parseable outputs (those that have a parse tree) are stored in the array
	#returned by this function.  So that's okay, I guess...
	global checkCommand
	try:
		return check_output(checkCommand+input,shell=True).split('\n')
	except CalledProcessError, e:
		print "Something went wrong, ya dummy:\n", e.output

if len(sys.argv) <= 1:
	print("Use either 'python run.py generate', 'python run.py check', 'python run.py compile', 'python run.py getUnknown', or 'python run.py niceParseTree'")
elif sys.argv[1] == "generate":
	call(["python", "innerWorkings/pcfg_parse_gen.py", "-o", "10", "-g","innerWorkings/S1.gr,innerWorkings/Vocab.gr"])
elif sys.argv[1] == "check":
	call(checkCommand+'innerWorkings/example_sentences.txt',shell=True)
elif sys.argv[1] == "compile":
	call(["python","contextExpander.py","CFGTemplate.txt"])
	call(["python","toCNF.py","contextExpanderOutput.txt"])
elif sys.argv[1] == "getUnknown":
	#Returns a list of all unknown things
	#Doesn't actually need to be stored in out (in fact out is NOT what we want, out is everything but what we want XD)
	out = getCheckOutput("innerWorkings/example_sentences.txt")
elif sys.argv[1] == "niceParseTree":
	if len(sys.argv) == 3:
		out = ""
		if str.isdigit(sys.argv[2]):
			out = getCheckOutput()[int(sys.argv[2])]
		else:
			#Because of how we're calling pcfg_parse_gen, we need to supply a file, not a string.
			#So, naturally, we just store the string in a temporary file.
			theString = sys.argv[2]
			#For some reason, this doesn't work unless there is a space after the last punctuation mark...
			#Also, we need a space before the punctuation marks.  Since punctuation marks occur at the end,
			#we'll just put a space right before the last char in its punctuation.  If there's too many spaces, it doesn't cause a problem.
			if not str.isalpha(theString[-1]):
				theString = theString.strip()
				theString = theString[:-1] + " " + theString[-1]
			theString = theString + " "
			fout = open("innerWorkings/stringWrapper.txt", "w")
			fout.write(theString)
			fout.close()
			out = getCheckOutput("innerWorkings/stringWrapper.txt")[0]
		print("^^^ I can't stop the above output from running, sorry. ^^^")
		out = out.replace("("," ( ").replace(")"," ) ")
		treeForm = createTreeFromOutputPrint(out)
		countSize(treeForm)
		printTree(treeForm)

	else:
		print("Please supply an argument, either as an index into the array of example sentences, or the example sentence itself.")
		print("Example: 'python run.py niceParseTree 1' will print a nice parse tree for the example sentence at index 1.")
		print("'python run.py niceParseTree \"Arthur speaks .\" will provide a parse tree for the given input specifically.")
else:
	print("Please supply either 'generate', 'check', 'compile', 'getUnknown', or 'niceParseTree' as arguments.")

#with open("innerWorkings/example_sentences.txt", 'w') as outfile:
#		call(["python","innerWorkings/pcfg_parse_gen.py","-i","-g",'"innerWorkings/*.gr"'],stdout=outfile)
