import java.util.Scanner;

public class Example {

	public static int Add(int x, int y) {
		return (x + y);
	}

	public static int Multiply(int a, int b) {
		return (a * b);
	}

	public static void compare(int x) {
		if (x < 50)
		{
			System.out.println("Your favorite number is less than 50");
		}
		else
		{
			if (x == 50) {
				System.out.println("Your favorite number is 50!");
			}
			else {
				System.out.println("Your favorite number is greater than 50");
			}
		}

		return;
	}

	public static void main(String args[]) {

		Scanner input = new Scanner(System.in);

		System.out.print("Enter the first number:  ");
		int num1 = input.nextInt();
		System.out.print("Enter the second number: ");
		int num2 = input.nextInt();
		System.out.print("Enter your favorite number: ");
		int x = input.nextInt();
		input.close();

		int result1 = Add(num1, num2);
		int result2 = Multiply(num1, num2);

		System.out.println("Addition: " + result1);
		System.out.println("Multiply: " + result2);

		compare(x);

		return;
	}
}
