# -*- coding: utf-8 -*-
import sys
from math import floor

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
			
	
	disallowedMatches = ["FromTakersPP_1st_Sng_Transitive", "Noun_2nd_Plr", "Possessive_1st_Plr", "Noun_1st_Plr", "Noun_2nd_Sng", "Pronoun_1st_Plr_IndObj", "Noun_1st_Sng", "Determiner_1st_Plr", "FromTakersContinuous_Intransitive", "time_Sng","FromTakers_1st_Sng_Intransitive","Noun_2nd_Plr","FromTakersContinuous_Transitive","FromTakers_3rd_Plr_Intransitive","Pronoun_1st_Plr_DirObj","FromTakers_2nd_Plr_Transitive","Noun_2nd_Sng","FromTakers_2nd_Plr_Intransitive","FromTakers_1st_Plr_Intransitive","FromTakers_1st_Sng_Transitive","FromTakers_1st_Plr_Transitive","FromTakers_2nd_Sng_Intransitive","FromTakers_2nd_Sng_Transitive","FromTakersPP_1st_Plr_Intransitive","FromTakersPP_3rd_Plr_Transitive","FromTakersPP_1st_Sng_Intransitive","FromTakers_3rd_Sng_Intransitive"]
			
	disallowedRemoved = 0
	lhsRemoved = set([])
	for line in list(output):
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
				
		for line in list(output):
			split = line.split()
			if len(split) == 0 or not split[0].isdigit(): continue
			
			if split[1] in lhsRemoved:
				lhsRemoved.remove(split[1])
				
		oldLhsRemove = lhsRemoved.copy()
		for line in list(output):
			split = line.split()
			if len(split) == 0 or not split[0].isdigit(): continue
			
			for rhs in split[2:]:
				if rhs in oldLhsRemove:
					output.remove(line)
					lhsRemoved.add(split[1])
					break


	#We have now removed the expanded templates (contextExpander.py), turned to CNF, and removed all nonterminals that did not have an associated terminal
	#The final step is to normalize the probabilities so that their sum is at most 100
	#For laziness reasons we will not make it exactly 100, since the code given to us for generating only accepts integer weights
	#and it would add an annoying layer of complexity to not simply round down every noninteger weight.
	#Us adding this renormalization has the added benefit of allowing us to use non-integer values in the pre-compiled CFGTemplate.txt :)
	def getSums(output):
		sums = {}
		for line in output:
			splt = line.split()
			if len(splt) == 0: continue
			if not splt[0].isdigit(): continue
			if not splt[1] in sums: #if we haven't started counting this yet, initialize it
				sums[splt[1]] = float(splt[0])
			else:#otherwise, just increment it
				sums[splt[1]] += float(split[0])
		return sums

	sums = getSums(output)
	for a in range(len(output)): #need to keep track of the index
		line = output[a]
		splt = line.split()
		if len(splt) == 0: continue
		if not splt[0].isdigit(): continue
		splt[0] = str(int(floor(100* float(splt[0])/sums[splt[1]]  )))
		if splt[0] == "0":
			splt[0] = "1"
		output[a] = "\n"+" ".join(splt)

	#because of "if splt[0] == 0: splt[0] = 1", sum could still be >100
	#so we will do one more pass and, if we find any, we will subtract the amount from the greatest weighted thing.
	print("Pruning All Sums > 100")
	while True:
		sums = getSums(output)
		overSums = {key: value for key, value in sums.iteritems() if value > 100}
		if len(overSums) == 0: break
		print(overSums)
		for LHS, value in overSums.iteritems():
			indxOfMax = -1
			valOfMax = 0
			for a in range(len(output)):
				splt = output[a].split()
				if len(splt) == 0: continue
				if not splt[0].isdigit(): continue
				if splt[1] != LHS: continue
				v = int(splt[0])
				if v > valOfMax:
					valOfMax = v
					indxOfMax = a
			if indxOfMax == -1: continue
			newOutput_a = output[indxOfMax].split()
			newOutput_a[0] = str(int(newOutput_a[0])-1)
			if newOutput_a[0] == 0:
				print("Error: " + LHS)
			output[indxOfMax] = "\n"+" ".join(newOutput_a)


	open("CNFConversion.txt", "w").write("".join(output))
	open("innerWorkings/S1.gr", "w").write("".join(output))
	print("Final Production Rule Quantity:" + str(lineCounter(output)))
	print("")

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
