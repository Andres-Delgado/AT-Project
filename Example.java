import java.util.Scanner;

public class Example {
	
	public static int Add(int x, int y) {
		return (x + y);
	}

	public static int Multiply(int x, int y) {
		return (x * y);
	}

	public static void main(String args[]) {

		Scanner input = new Scanner(System.in);

		System.out.print("Enter the first number:  ");
		int num1 = input.nextInt();
		System.out.print("Enter the second number: ");
		int num2 = input.nextInt();

		input.close();

		int result1 = Add(num1, num2);
		int result2 = Multiply(num1, num2);

		System.out.println("Addition: " + result1);
		System.out.println("Multiply: " + result2);
		
		return;
	}
}