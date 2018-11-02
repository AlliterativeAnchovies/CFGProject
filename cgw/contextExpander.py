import sys

if (len(sys.argv) < 2 ):
	print("Error - you need to supply a file to parse!")
	print("So I'm going to crash the program by dividing by zero, like a gentleman :)")
	print(5/0)

print('\nFile to Parse:', sys.argv[1],'\n')
fileToParse = open(sys.argv[1],'r')
theFile = fileToParse.read()
#print('Fun fact!  Your file looks like this:\n',theFile,'\n')

#Here's the general idea - we go through the file line by line
#until we get to a {
#At which point we look for the <s on the upcoming lines, telling us what to loop through
#It is an important rule that nothing, not even comments, come between { and the <s
#The | tell us which to ignore, and must come directly after the <s if at all
#We continue line by line, expanding each line out according to our commands.
#Until we reach }
#Then its back to normal.

allLines = theFile.split('\n')
outputString = ""
bracketMode = False
finishedReadingAngles = False
finishedReadingPipes = False
templateDict = {}
ignoreTuples = []

def checkUnorderedListEquality(s, t):
    return sorted(s) == sorted(t)

def doReplacing(line,listOfTemplators):
	global outputString
	global templateDict
	global ignoreTuples
	if listOfTemplators == []:
		splitline = line.split("∂");
		actualLine = line.split("∂")[0]
		if len(splitline) > 1:
			lineEnders = line.split("∂")[1:]
			if any([checkUnorderedListEquality(lineEnders,x) for x in ignoreTuples]):
				#It's on the ignore list!
				return
		outputString = outputString + "\n" + actualLine
		return
	else:
		curTemplateRaw = listOfTemplators[0]
		curTemplate = curTemplateRaw.split("{")[1].split("}")[0]
		listOfTemplators = listOfTemplators[1:]
		for replacement in templateDict[curTemplate]:
			realReplacement = replacement
			if realReplacement == "ε":
				realReplacement = ""
			doReplacing(line.replace(curTemplateRaw,realReplacement)+"∂"+replacement,listOfTemplators)


for line in allLines:
	trimmed = line.strip()
	if trimmed == "{":
		if bracketMode:
			print("Double brackets error!!!")
			print(5/0)
		bracketMode = True
		continue
	elif trimmed == "}":
		finishedReadingAngles = False
		finishedReadingPipes = False
		templateDict = {}
		ignoreTuples = []
		if not bracketMode:
			print("Missing opening bracket")
			print(5/0)
		bracketMode = False
		continue
	elif not bracketMode:
		outputString = outputString + "\n" + line
	else:
		if len(trimmed) == 0:
			outputString = outputString + "\n"
			continue
		firstChar = trimmed[0]
		if firstChar == '<':
			if finishedReadingAngles:
				print("Angle bracket too late")
				print(5/0)
			#Readin here
			contents = trimmed.split('<')[1].split('>')[0].split() #split on whitespace
			templateDict[contents[0]] = contents[1:]
		else:
			finishedReadingAngles = True
			if firstChar == '|':
				if finishedReadingPipes:
					print("Pipe too late")
					print(5/0)
				#Readin here
				contents = trimmed.split('|')[1].split()[1:]
				ignoreTuples.append(contents)
			else:
				finishedReadingPipes = True
				#Now we are on the normal stuff
				#Copy each line unless it contains one of the templates
				#In which case perform the template
				listOfTemplators = ["{" + x + "}" for x in templateDict.keys() if "{" + x + "}" in line]
				doReplacing(line,listOfTemplators)


#print(outputString)
outputString = "# The start symbol is TOP.\n# These two rules are required; choose their weights carefully!\n99  TOP  S1\n#1   TOP  S2\n" + outputString
outputString = outputString + "\n# in case you use S1.gr by itself\n1   S2   Misc"
fout = open("S1.gr", "w")
print(outputString)
fout.write(outputString)
