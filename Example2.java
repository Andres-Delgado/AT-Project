import java.util.Scanner;

public class Example2 {

	public static int AddSubtract(int x, int y) {
		int result1 = x + y;
		int result2 = x - y;
		System.out.println("Addition of both numbers: " + result1);
		System.out.println("subtracting 2nd number from 1st: " + result2);
		return (result1 + result2);
	}

	public static int Multiply(int a, int b) {
		return (a * b);
	}

	public static void main(String args[]) {

		Scanner input = new Scanner(System.in);

		System.out.print("Enter the first number:  ");
		int num1 = input.nextInt();
		System.out.print("Enter the second number: ");
		int num2 = input.nextInt();

		int newResult1 = AddSubtract(num1, num2);
		System.out.println("Final Addition: " + newResult1);

		System.out.print("Enter a third number: ");
		int num3 = input.nextInt();
		input.close();

		int newResult2 = Multiply(num1, num3);
		int newResult3 = Multiply(num2, num3);

		System.out.println("Product of 1st and 3nd number: " + newResult2);
		System.out.println("Product of 2nd and 3rd number: " + newResult3);

		return;
	}
}
