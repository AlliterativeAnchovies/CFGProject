# -*- coding: utf-8 -*-
import sys

print("\nConverting To CNF...")

def lineCounter(output): #counts the number of production rules in the final output
	count = 0
	for line in output:  #it does this by checking if a line begins with a number
		l = line.strip()
		if len(l) == 0: continue
		if l[0].isdigit(): count = count + 1
	return count

if (len(sys.argv) == 2):
	allLines = open(sys.argv[1],'r').readlines()

	output = []

	for line in allLines:
		split = line.split()
		
		if len(split) > 4 and split[0].isdigit():		# This is a rule that's too big
			for i, val in enumerate(split[2:-1]):		# Loop over the parts of it that are too big
				nextRuleName = "|".join(split[(i+3):])
				ruleName = split[1] if i == 0 else "|".join(split[(i+2):])
				output.append(split[0] + " " + ruleName + " " + val + " " + nextRuleName + "\n") 
		else:
			output.append(line)
			
	
	disallowedMatches = ["FromTakersPP_1st_Sng_Transitive", "Noun_2nd_Plr", "Possessive_1st_Plr", "Noun_1st_Plr", "Noun_2nd_Sng", "Pronoun_1st_Plr_IndObj", "Noun_1st_Sng", "Determiner_1st_Plr", "FromTakersContinuous_Intransitive", "time_Sng"]
			
	disallowedRemoved = 0
	lhsRemoved = set([])
	for line in output:
		split = line.split()
		if len(split) == 0 or not split[0].isdigit(): continue
		for rhs in split[2:]:
			if rhs in disallowedMatches:
				output.remove(line)
				disallowedRemoved += 1
				lhsRemoved.add(split[1])
				break
			
	print("Removed: " + str(disallowedRemoved))
			
	lastLength = 0
	while (len(output) != lastLength):
		lastLength = len(output)
				
		for line in output:
			split = line.split()
			if len(split) == 0 or not split[0].isdigit(): continue
			
			if split[1] in lhsRemoved:
				lhsRemoved.remove(split[1])
		
		for line in output:
			split = line.split()
			if len(split) == 0 or not split[0].isdigit(): continue
			
			for rhs in split[2:]:
				if rhs in lhsRemoved:
					output.remove(line)
					lhsRemoved.add(split[1])
					break
	
				
	open("CNFConversion.txt", "w").write("".join(output))
	open("innerWorkings/S1.gr", "w").write("".join(output))
	print("Final Production Rule Quantity:" + str(lineCounter(output)))
	print("")

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
