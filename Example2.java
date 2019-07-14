import java.util.Scanner;

public class Example2 {

	public static int AddSubtract(int x, int y) {
		int result1 = x + y;
		int result2 = x - y;
		System.out.println("1st + 2nd: " + result1);
		System.out.println("2nd - 1st: " + result2);
		return (result1 + result2);
	}

	public static int Multiply(int a, int b) {
		return (a * b);
	}

	public static void main(String args[]) {

		Scanner input = new Scanner(System.in);

		System.out.print("Enter 1st number:  ");
		int num1 = input.nextInt();
		System.out.print("Enter 2nd number: ");
		int num2 = input.nextInt();

		int newResult1 = AddSubtract(num1, num2);
		System.out.println("Addition of both operations: " + newResult1);

		System.out.print("Enter a 3rd number: ");
		int num3 = input.nextInt();
		input.close();

		int newResult2 = Multiply(num1, num3);
		int newResult3 = Multiply(num2, num3);

		System.out.println("1st * 3rd: " + newResult2);
		System.out.println("2nd * 3rd: " + newResult3);

		return;
	}
}
