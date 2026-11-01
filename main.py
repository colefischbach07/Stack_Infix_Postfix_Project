
"""Main program for the Stack Infix and Postfix Project."""
from postfix_evaluator import PostfixEvaluator
from infix_converter import InfixToPostfixConverter


def main():
    """Test both postfix evaluation and infix conversion."""

    evaluator = PostfixEvaluator()
    converter = InfixToPostfixConverter()

    print("----- Postfix Evaluator -----")

    postfix_tests = [
        "5 3 +",
        "8 2 - 3 +",
        "35 27 + 3 *",
        "8 0 /",
        "5 +",
        "2 3 4 +"
    ]

    for expression in postfix_tests:
        try:
            result = evaluator.evaluate(expression)
            print(f"[{expression}] = {result}")
        except (ValueError, ZeroDivisionError) as error:
            print(f"[{expression}] -> ERROR: {error}")

    print("\n----- Infix to Postfix Converter -----")

    infix_tests = [
        "A + B",
        "A + B * C",
        "(A + B) * C",
        "A - B + C",
        "A + * B",
        "(A + B",
        "A + B @ C"
    ]


    for expression in infix_tests:
        try:
            result = converter.convert(expression)
            print(f"[{expression}] -> [{result}]")
        except ValueError as error:
            print(f"[{expression}] -> ERROR: {error}")


if __name__ == "__main__":
    main()
