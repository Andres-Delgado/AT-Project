import java.util.Scanner;

public class Example1 {

	public static void AnalyzeNumber(int num) {

		if (num % 2 == 0) {
			
			if (num == 100) {
				System.out.println("Congrats! You entered 100!");
			}
			else {
				System.out.println("You did not enter the winning number...");
			}
			
		}
		else {
			System.out.println("The winning number is not odd");
			
			if (num > 100) {
				System.out.println("It is also too big...");
			}
			else {
				System.out.println("It is also too small...");
			}
		}
		return;
	}

	public static void main(String args[]) {

		Scanner input = new Scanner(System.in);

		System.out.print("Guess the winning number: ");
		int userNum = input.nextInt();
		input.close();

		System.out.println("Analyzing number: " + userNum);
		AnalyzeNumber(userNum);

		return;
	}
}