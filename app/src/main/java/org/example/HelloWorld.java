package org.example;

public class HelloWorld {

    public static void main(String[] args) {
        System.out.println("Hello, World2!");
        var firstText ="aaa";
        System.out.println(firstText);
        var secondText ="bbb";
        System.out.println(secondText);

        var sumResult2 = sum(10,20);
        System.out.println(sumResult2);

    }
    public static int sum(int firstNumber, int secondNumber){
        return firstNumber + secondNumber;
    }
}