
"""Convert infix expressions to postfix using a stack."""


import re
from stack import Stack


class InfixToPostfixConverter:
    """Convert infix expressions using the shunting-yard algorithm."""

    def __init__(self):
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2
        }


    def convert(self, expression):
        """Convert an infix expression to postfix notation.

        Raises ValueError for invalid syntax or parentheses.
        """
        if not isinstance(expression, str) or not expression.strip():
            raise ValueError("Empty expression")

        # This project uses single-letter variables or numbers.
        tokens = re.findall(r"[A-Za-z]|\d+(?:\.\d+)?|[()+*/-]|\S", expression)

        output = []
        operators = Stack()
        expect_operand = True

        for token in tokens:
            if re.fullmatch(r"[A-Za-z]|\d+(?:\.\d+)?", token):
                if not expect_operand:
                    raise ValueError("Misplaced operand")

                output.append(token)
                expect_operand = False

            elif token == "(":
                if not expect_operand:
                    raise ValueError("Misplaced opening parenthesis")
                operators.push(token)

            elif token == ")":
                if expect_operand:
                    raise ValueError("Misplaced closing parenthesis")

                while not operators.is_empty() and operators.peek() != "(":
                    output.append(operators.pop())

                if operators.is_empty():
                    raise ValueError("Mismatched parentheses")

                operators.pop()
                expect_operand = False

            elif token in self.precedence:
                if expect_operand:
                    raise ValueError("Misplaced operator")

                while (
                    not operators.is_empty()
                    and operators.peek() in self.precedence
                    and self.precedence[operators.peek()] >= self.precedence[token]
                ):
                    output.append(operators.pop())

                operators.push(token)
                expect_operand = True

            else:
                raise ValueError(f"Invalid token: {token}")

        if expect_operand:
            raise ValueError("Incomplete expression")

        while not operators.is_empty():
            operator = operators.pop()

            if operator == "(":
                raise ValueError("Mismatched parentheses")

            output.append(operator)

        return " ".join(output)


if __name__ == "__main__":
    converter = InfixToPostfixConverter()

    valid_tests = {
        "A+B": "A B +",
        "A+B*C": "A B C * +",
        "(A+B)*C": "A B + C *",
        "A*B+C/D": "A B * C D / +",
        "(A+B)*(C-D)": "A B + C D - *",
        "A+B*C-D/E": "A B C * + D E / -",
        "A*(B+C)/D": "A B C + * D /",
        "(A+B*C)/(D-E)": "A B C * + D E - /",
        "A+(B-C)*D": "A B C - D * +",
        "(A+B*(C-D))/E": "A B C D - * + E /",
        "A-B+C": "A B - C +",
        "A/B*C": "A B / C *",
        "(((((((( A + B ))))))))": "A B +"
    }

    for expression, expected in valid_tests.items():
        result = converter.convert(expression)
        assert result == expected, f"Failed: {expression}"
        print(f"[{expression}] -> [{result}]")



    invalid_tests = [
        "A+B)C",
        "A+B;C",
        "+AB",
        "A+*B",
        "AB+C",
        "A+)B*C(",
        "(A+B",
        "A+B)",
        "A B+C",
        "A+",
        "()"
    ]


    for expression in invalid_tests:
        try:
            converter.convert(expression)
        except ValueError as error:
            print(f"[{expression}] -> ERROR: {error}")
        else:
            raise AssertionError(
                f"Expected error for {expression}"
            )


    print("All InfixToPostfixConverter tests passed!")
