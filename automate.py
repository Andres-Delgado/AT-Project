import os

def Imports(importStr):
	"""Converts necessary java import statements
	into python import statemenets."""

	# remove ending ';' character for easier parsing
	if importStr[-1] == ";":
		importStr = importStr[:-1]

	# Scanner import, python doesn't need additional import statement
	if importStr == "java.util.Scanner":
		print("Found unneeded import:", importStr)
		return None

	#print("\nFound import:", importStr)
	return None

def Functions(functionStr):
	"""Converts java function definitions into python function definitions."""

	# DEBUG
	fStr = ""
	for x in functionStr:
		if x == "{":
			break
		fStr += x + " "
	# DEBUG

	print("\nFound Class/Function Definition: ", fStr)
	return None

def Parse(javaList):
	"""Parses through the list of strings in javaList
	and decides what actions to perform."""

	# keeps track of the number of strings we have parsed through 
	strCount = len(javaList)

	importStrings = []

	#print(*javaList, sep = '\n')
	#return	

	# begin parsing through through each text string in javaList
	while strCount > 0:	

		# found import statements
		if javaList[0] == "import":
			javaList.pop(0)
			strCount -= 1

			# extract needed python import statements
			importStrings.append(Imports(javaList[0]))
			
		# found new function or class definition
		elif (javaList[0] == "public") or (javaList[0] == "private") or (javaList[0] == "protected"):
			#javaList.pop(0)
			#strCount -= 1

			# extract needed method definitions
			Functions(javaList)

		# DEBUG PRINT
		print(javaList[0], end = " ")
		if javaList[0][-1] == ";" or javaList[0] == "{" or javaList[0] == "}":
			print()
	
		# remove first item and continue with loop
		javaList.pop(0)
		strCount -= 1

	#print("Import Strings:", importStrings)
	return javaList


if __name__ == "__main__":
	
	path = os.getcwd()
	filePath = path + "/Example.java"

	javaStr = ""

	# open contents of java file
	with open(filePath, 'r') as f:

		# append each line to javaStr
		for i, line in enumerate(f, 1):
			javaStr += line
		
	# split the javaStr text into a list of strings, ignoring whitespace
	# start parsing through the text of java file
	pythonStr = Parse(javaStr.split())
	
	print("\nParsing finished")
	
	#print(type(javaStr), len(javaStr))
	#print(javaStr)
	
