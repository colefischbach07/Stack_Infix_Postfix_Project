
"""This module evaluates postfix math expressions."""

from stack import Stack


class PostfixEvaluator:
    """Evaluate postfix expressions using a stack."""

    def evaluate(self, expression):
        """Evaluate an expression and return its result."""
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Empty expression")

        stack = Stack()

        # Expressions without spaces use single-digit numbers.
        if " " in expression.strip():
            tokens = expression.split()
        else:
            tokens = list(expression.strip())

        for token in tokens:
            if token in ("+", "-", "*", "/"):
                if stack.size() < 2:
                    raise ValueError("Not enough operands")

                right = stack.pop()
                left = stack.pop()

                if token == "+":
                    result = left + right
                elif token == "-":
                    result = left - right
                elif token == "*":
                    result = left * right
                else:
                    if right == 0:
                        raise ZeroDivisionError("Cannot divide by zero")
                    result = left / right

                stack.push(result)

            else:
                try:
                    number = float(token)
                    stack.push(number)
                except ValueError:
                    raise ValueError(f"Invalid token: {token}")

        if stack.size() != 1:
            raise ValueError("Incorrect number of operands")

        result = stack.pop()
        return int(result) if result.is_integer() else result



if __name__ == "__main__":
    evaluator = PostfixEvaluator()

    valid_tests = {
        "53+": 8,
        "82-3+": 9,
        "538*+": 29,
        "62/3+": 6,
        "58+3-": 10,
        "53+8*": 64,
        "823*+6-": 8,
        "538*+2/": 14.5,
        "82+36*-": -8,
        "53+82/-": 4,
        "35 27 + 3 *": 186,
        "23 30 15 * /": 23 / 450,
    }

    for expression, expected in valid_tests.items():
        result = evaluator.evaluate(expression)
        assert abs(result - expected) < 0.000001
        print(f"[{expression}] = {result}")

    invalid_tests = [
        "26 28 + 32 2 ; - 5 /",
        "234+",
        "20 29 9 * ;",
        "25 23 - +",
        "80/",
        "5+",
        "3+4",
        "8 0 /",
        "2 3 4 +",
    ]

    for expression in invalid_tests:
        try:
            evaluator.evaluate(expression)
        except (ValueError, ZeroDivisionError) as error:
            print(f"[{expression}] -> ERROR: {error}")
        else:
            raise AssertionError(
                f"Expected an error for {expression}"
            )

    print("All PostfixEvaluator tests passed!")

