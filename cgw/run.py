#python pcfg_parse_gen.py -o 20 -g S1.gr,Vocab.gr
from subprocess import call
from subprocess import check_output, CalledProcessError
import sys

checkCommand = "python "+"innerWorkings/pcfg_parse_gen.py "+"-i "+"-g "+'"innerWorkings/*.gr" < '#'innerWorkings/example_sentences.txt'

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
	call(["python", "innerWorkings/pcfg_parse_gen.py", "-o", "50", "-g","innerWorkings/S1.gr,innerWorkings/Vocab.gr"])
elif sys.argv[1] == "check":
	call(checkCommand+'innerWorkings/example_sentences.txt',shell=True)
elif sys.argv[1] == "compile":
	call(["python","contextExpander.py","CFGTemplate.txt"])
	call(["python","toCNF.py","contextExpanderOutput.txt"])
elif sys.argv[1] == "getUnknown":
	out = getCheckOutput()
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
		#Harry, 'out' contains exactly one string of an ugly parse tree.  This is a good starting point for you if you want.
		#Run "python run.py niceParseTree "Arthur speaks." in your console to see what is currently outputted.  Believe it
		#or not, that ungodly mess is the parse tree for that simple sentence.  A really simple example of the format would be:
		# (TOP (NP Arthur) (END (VP speaks) (PUNCTUATION .)))
		#If the rules were TOP -> NP END, NP -> Arthur, END -> VP PUNCTUATION, VP -> speaks, PUNCTUATION -> .
		#I hope that makes sense!
		print(out)
	else:
		print("Please supply an argument, either as an index into the array of example sentences, or the example sentence itself.")
		print("Example: 'python run.py niceParseTree 1' will print a nice parse tree for the example sentence at index 1.")
		print("'python run.py niceParseTree \"Arthur speaks .\" will provide a parse tree for the given input specifically.")
else:
	print("Please supply either 'generate', 'check', 'compile', 'getUnknown', or 'niceParseTree' as arguments.")

#with open("innerWorkings/example_sentences.txt", 'w') as outfile:
#		call(["python","innerWorkings/pcfg_parse_gen.py","-i","-g",'"innerWorkings/*.gr"'],stdout=outfile)
