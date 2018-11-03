#python pcfg_parse_gen.py -o 20 -g S1.gr,Vocab.gr
from subprocess import call
import sys
if len(sys.argv) <= 1:
	print("Use either 'python run.py generate' or 'python run.py check' or 'python run.py compile'")
elif sys.argv[1] == "generate":
	call(["python", "innerWorkings/pcfg_parse_gen.py", "-o", "50", "-g","innerWorkings/S1.gr,innerWorkings/Vocab.gr"])
elif sys.argv[1] == "check":
	command = "python "+"innerWorkings/pcfg_parse_gen.py "+"-i "+"-g "+'"innerWorkings/*.gr" < innerWorkings/example_sentences.txt'
	call(command,shell=True)
elif sys.argv[1] == "compile":
	call(["python","contextExpander.py","CFGTemplate.txt"])
else:
	print("Please supply either 'generate' or 'check' or 'compile' as arguments.")

#with open("innerWorkings/example_sentences.txt", 'w') as outfile:
#		call(["python","innerWorkings/pcfg_parse_gen.py","-i","-g",'"innerWorkings/*.gr"'],stdout=outfile)
