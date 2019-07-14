def Add(x, y):
	return (x + y)

def Multiply(a, b):
	return (a * b)

def compare(x):
	print("Your favorite number is greater than 50")
	return

if __name__ == "__main__":
	print("Enter the first number: ", end = "")
	num1 = int(input())
	print("Enter the second number: ", end = "")
	num2 = int(input())
	print("Enter your favorite number: ", end = "")
	x = int(input())
	result1 = Add(num1, num2)
	result2 = Multiply(num1, num2)
	print("Addition: " + str(result1))
	print("Multiply: " + str(result2))

