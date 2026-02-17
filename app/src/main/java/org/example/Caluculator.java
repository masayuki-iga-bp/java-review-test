package org.example;

public class Caluculator {
    /**
     * 割り算を行います.
     * @param a 割られる数
     * @param b 割る数
     * @return 割り算の結果
     */
    public int divide(int a, int b) {
        return a / b;
    }
    /**
     * 足し算を行います.
     * @param a 足される数
     * @param b 足す数
     * @return 足し算の結果
     */
    public int add(int a, int b) {
        return a + b;
    }

    public int multiply(int x, int y) {
        int temp = 0;
        int result1 = x;
        int result2 = y;
        temp = result1 * result2;
        if (temp > 0) {
            return temp;
        } else if (temp < 0) {
            return temp;
        } else {
            return temp;
        }
    }

    public int subtract(int a, int b) {
        int x = a;
        int y = b;
        int z = x - y;
        if (z != 0) {
            if (z > 100) {
                return z - 10;
            }
            return z;
        }
        return 0;
    }

    // 問題のあるコード: JavaDocなし、例外処理なし、マジックナンバーあり
    public double divideWithLogging(int numerator, int denominator) {
        System.out.println("Dividing " + numerator + " by " + denominator);
        double result = numerator / denominator;
        if (result > 999) {
            result = 999;
        }
        return result;
    }

    // 問題のあるコード: 複雑なネストされた条件、JavaDocなし
    public String evaluateScore(int score) {
        String grade;
        if (score >= 90) {
            if (score >= 95) {
                if (score >= 98) {
                    grade = "A+";
                } else {
                    grade = "A";
                }
            } else {
                grade = "A-";
            }
        } else if (score >= 80) {
            grade = "B";
        } else if (score >= 70) {
            grade = "C";
        } else {
            grade = "F";
        }
        return grade;
    }
}
