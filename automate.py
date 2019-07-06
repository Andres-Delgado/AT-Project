import os
import json

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

def ExtractParameterVars(funcList):
	"""Finds the parameter variables names from a function definition."""

	tempList = list(funcList)
	varNames = []

	while tempList:
		
		# current element contains '(' character
		if "(" in tempList[0]:
			
			# current string is only the function name, eg. Add( int x)
			if tempList[0][-1] == "(":
				tempList.pop(0)

			# pop current element (variable type)
			tempList.pop(0)

			# append variable name string, excluding ',' character if present
			if tempList[0][-1] == ",":
				varNames.append(tempList[0][:-1])
			
			# in main function definition, only 1 parameter
			elif "[]" in tempList[0]:
				varNames.append(tempList[0][:tempList[0].index("[]")])
				break

			# current element is just the parameter variable name
			else: varNames.append(tempList[0])
		
		# current element is the end of function definition
		elif ")" in tempList[0]:
			varNames.append(tempList[0][:tempList[0].index(")")])
			break
		
		# pop current element, continue with loop
		tempList.pop(0)

	print("Extracted Parameters:", varNames)
	return varNames

def ExtractFunction(functionStr):
	"""Converts java function definitions into python function definitions."""

	# DEBUG PRINT
	fStr = ""
	for x in functionStr:
		if x == "{":
			break
		fStr += x + " "
	print("\nFound Class/Function Definition: ", fStr)
	# DEBUG PRINT

	functionDict = {}
	tempList = list(functionStr)

	while tempList[0] != "{":

		# found the start of the parameter definitions
		if "(" in tempList[0]:
			nameStr = tempList[0][:tempList[0].index("(")]
			functionDict[nameStr] = {}

			# extract the parameter names, add to dictionary
			functionDict[nameStr]["parameters"] = ExtractParameterVars(tempList)
			break

		# skip function and parameter prefixes
		#elif tempList[0] == "static" or tempList[0] == "int" or tempList[0] == "String": 
		#	print("skipped:", tempList[0])

		tempList.pop(0)

	print("Current Function Dictionary:")
	print(json.dumps(functionDict, indent = 2), end = '\n\n')
	return functionDict

def Parse(javaList):
	"""Parses through the list of strings in javaList
	and decides what actions to perform."""

	# keeps track of the number of strings we have parsed through 
	strCount = len(javaList)

	importStrings = []
	functionDict = {}
	programName = ""

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

			# found java program class definition
			if javaList[1] == "class":
				javaList.pop(0)
				javaList.pop(0)
				strCount -= 2

				programName = javaList[0]
				print("\nFound java class name:", programName)
				
				javaList.pop(0)
				strCount -= 1
			
			# found a function definition
			else: 
				# create function dictionary
				functionDict.update(ExtractFunction(javaList))
				
				# pop current element until the open brack is found, 
				# the definition is not needed anymore
				while javaList[0] != "{":
					javaList.pop(0)
					strCount -= 1


		# DEBUG PRINT
		print(javaList[0], end = " ")
		if javaList[0][-1] == ";" or javaList[0] == "{" or javaList[0] == "}":
			print()
		# DEBUG PRINT

		# remove first item and continue with loop
		javaList.pop(0)
		strCount -= 1

	print("\nParsing Finished\n")

	print("Import Strings:", importStrings)
	print("Program Name:", programName)
	print("Function Dictionaries:")
	print(json.dumps(functionDict, indent = 2))

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
	
	#print(type(javaStr), len(javaStr))
	#print(javaStr)
	