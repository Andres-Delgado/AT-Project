import os
import json
import sys

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

	return None

def ExtractParameterVars(funcList):
	"""Finds the parameter variables names from a function definition."""

	tempList = list(funcList)
	varNames = []

	while tempList:

		if "if" in tempList[0]:
			break
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
			elif ")" in tempList[0]:
				varNames.append(tempList[0][:tempList[0].index(")")])

		# current element is the end of function definition
		elif ")" in tempList[0]:
			varNames.append(tempList[0][:tempList[0].index(")")])
			break

		# pop current element, continue with loop
		tempList.pop(0)

	print("Extracted Parameters:", varNames)
	return varNames

def ExtractLocalVars(funcList):
	"""Finds any local variables used in a function"""

	vartypes = ["byte", "short", "int", "long", "float", "double", "char", "boolean",
			  	"byte[]", "short[]", "int[]", "long[]", "float[]",
				"double[]", "char[]", "boolean[]"]

	tempList = list(funcList)
	localVars = []

	while tempList:
		#read and pop from tempList until you reach the start of the methods
		if tempList[0] != "{":
			tempList.pop(0)

		else:
			while tempList[0] != "}":
				if tempList[0] in vartypes:
					tempList.pop(0)
					#if the current element is a variable type append variable to list
					localVars.append(tempList[0])

				else: tempList.pop(0)
			break

	print("Extracted Local Variables: ", localVars)
	return localVars

def ExtractFunction(functionStr):
	"""Converts java function definitions into python function definitions."""

	# DEBUG PRINT
	fStr = ""
	for x in functionStr:
		if x == "{":
			break
		fStr += x + " "
	print("\nFound Function Definition:", fStr)
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
			functionDict[nameStr]["Local Variables"] = ExtractLocalVars(tempList)
			# create a key for the contents in the function
			functionDict[nameStr]["content"] = []
			break

		tempList.pop(0)

	print("Current Function Dictionary:")
	print(json.dumps(functionDict, indent = 2), end = '\n\n')

	return functionDict

def ExtractContents(javaContent, localVariables):
	"""Converts the statements inside a Java function
	into Python statements. The new Python statements
	are chronologically ordered inside contentList."""

	contentList = []
	tempList = list(javaContent)

	# iterate until ending '}' is found
	while "return" not in tempList[0]:

		# found the start of an if statement
		if "if" in tempList[0]:
			
			ifstatement = tempList[0]
			tempList.pop(0)

			# extract the rest of the if statemenet
			while tempList[0] != "{":
				ifstatement += " " + tempList[0]
				tempList.pop(0)

			print(ifstatement)
			contentList.append(ifstatement)

		# found else statement
		elif "else" in tempList[0]:
			elsestatment = tempList[0]
			tempList.pop(0)
			print(elsestatment)
			contentList.append(elsestatment)

		# found an ending bracket to an if or else statement
		elif tempList[0] == "}":
			contentList.append(tempList[0])
			print(tempList[0])
		
		# found output statement
		elif "System.out.print" in tempList[0]:

			newline = "println" in tempList[0]
			opString = tempList[0][tempList[0].index("\""):] + " "
			tempList.pop(0)

			# iterate through print statement until ending quotation char
			while "\"" not in tempList[0]:
				opString += tempList[0] + " "
				tempList.pop(0)

			# output is just a string
			if "\");" in tempList[0]:
				opString += tempList[0][:tempList[0].index("\");") + 1]

			# output contains more just a string
			else:

				# iterate until ';' char
				while ";" not in tempList[0]:
					opString += tempList[0] + " "
					tempList.pop(0)

				opString += "str(" + tempList[0][:tempList[0].index(";")]

			# output does not contain a new line
			if not newline:
				opString += ", end = \"\""

			opString = "print(" + opString + ")"
			contentList.append(opString)
			print("print statement:", opString)

		# found the use of a local variable
		elif tempList[0] in localVariables:
			varStatement = ""

			# extract the statement until the ';' character
			while ";" not in tempList[0]:
				varStatement += tempList[0] + " "
				tempList.pop(0)

			# found an input statement
			if "input." in tempList[0]:
				varStatement += "int(input())"

			else:
				varStatement += tempList[0][:tempList[0].index(";")]
			contentList.append(varStatement)

		# found a single element statement, eg., compare(someVar);
		elif (";" in tempList[0]) and ("input" not in tempList[0]) and ("Scanner" not in tempList[0]):
			contentList.append(tempList[0][:tempList[0].index(";")])
		tempList.pop(0)

	# reached the return statement of function
	returnStr = ""

	# iterate through elements until the ending ';' is found
	while ";" not in tempList[0]:
		returnStr += tempList[0] + " "
		tempList.pop(0)

	# add the final element exclusing the ';' char
	returnStr += tempList[0][:tempList[0].index(";")]
	contentList.append(returnStr)
	print("return statement:", returnStr, end = '\n\n')

	return contentList

def WritePython(funcDict, fileName):

	# create new python file
	path = os.getcwd() + "/" + fileName + ".py"
	file = open(path, "w")

	# iterate through the function dictionaries
	for fName, fDict in funcDict.items():

		# write main function
		if fName == "main":
			file.write("if __name__ == \"__main__\":\n")

		# write non-main function
		else:
			# write function definition
			file.write("def " + fName + "(")

			# write parameters for function
			numParameters = len(fDict["parameters"]) - 1
			for x in fDict["parameters"]:
				file.write(x)

				# write ',' if more than 1 parameter variable
				if numParameters > 0:
					file.write(", ")
					numParameters -= 1

			# close ')' for function
			file.write("):\n")

		# keep track of the indentation for if/else statements
		tabCount = 1

		# write all statements in function
		for x in fDict["content"]:

			# skip return statement if in main function
			if (x == "return") and (fName == "main"):
				continue
			
			# start of if/else, increase indentation for next lines
			if ("if" in x) or ("else" in x):
				file.write(("\t" * tabCount) + x + ":\n")
				tabCount += 1

			# if/else is finished, decrease the number of indents
			elif x == "}":
				tabCount -= 1

			# write statement
			else: file.write(("\t" * tabCount) + x + "\n")

		file.write("\n")
	file.close()

	print("Finished Python file:", fileName + ".py")
	return

def Parse(javaList):
	"""Parses through the list of strings in javaList
	and decides what actions to perform."""

	# keeps track of the number of strings we have parsed through
	strCount = len(javaList)

	importStrings = []
	functionDict = {}
	programName, currentFuncName = "", ""

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
				newFuncDict = ExtractFunction(javaList)
				functionDict.update(newFuncDict)

				# get current function name
				currentFuncName = list(newFuncDict.keys())[0]

				# pop current element until the open brack is found,
				# the definition is not needed anymore
				while javaList[0] != "{":
					javaList.pop(0)
					strCount -= 1

		# found first '{' char of a function
		if (javaList[0] == "{") and currentFuncName:
			javaList.pop(0)
			strCount -= 1

			# extract the contents of the current Java function
			functionDict[currentFuncName]["content"] = ExtractContents(javaList, functionDict[currentFuncName]["Local Variables"])
			bracketCount = functionDict[currentFuncName]["content"].count("}")

			# there were if/else statements if "content" item contains "}" elements			
			if bracketCount:
				while bracketCount > 0:
					if javaList[0] == "}":
						bracketCount -= 1
					javaList.pop(0)
					strCount -= 1

			# pop current element until the end of function
			while javaList[0] != "}":
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
	print(json.dumps(functionDict, indent = 2), end = '\n\n')

	WritePython(functionDict, programName)
	return javaList

if __name__ == "__main__":

	# check if program was called in the right format
	if len(sys.argv) != 2:
		print("Program needs to be ran with in the following format:")
		print("python automate.py <JavaProgramName.java>\n")
		exit(0)

	path = os.getcwd()
	filePath = path + "/" + sys.argv[1]
	javaStr = ""

	# attempt to open contents of java file
	try:
		with open(filePath, 'r') as f:
			# append each line to javaStr
			for i, line in enumerate(f, 1):
				javaStr += line

	# specified file does not exist
	except FileNotFoundError:
		print("File \"{}\" does not exist\n".format(sys.argv[1]))
		exit(0)

	# split the javaStr text into a list of strings, ignoring whitespace
	# start parsing through the text of java file
	pythonStr = Parse(javaStr.split())
	