import sys

def lineCounter(output): #counts the number of production rules in the final output
	count = 0
	for line in output:  #it does this by checking if a line begins with a number
		l = line.strip()
		if len(l) == 0: continue
		if l[0].isdigit: count = count + 1
	return count

if (len(sys.argv) == 2):
	allLines = open(sys.argv[1],'r').readlines()

	output = []

	for line in allLines:
		split = line.split()
		
		if len(split) > 4 and split[0].isdigit():		# This is a rule that's too big
			for i, val in enumerate(split[2:-1]):		# Loop over the parts of it that are too big
				nextRuleName = "_".join(split[(i+3):])
				ruleName = split[1] if i == 0 else "_".join(split[(i+2):])
				output.append(split[0] + " " + ruleName + " " + val + " " + nextRuleName + "\n") 
		else:
			output.append(line)
				
				
	open("CNFConversion.txt", "w").write("".join(output))
	open("S1.gr", "w").write("".join(output))
	print("Final Production Rule Quantity: " + str(lineCounter(output)))
