from typing import List
from scanner import Token
from scanner import TokenType, Scanner


class Expr:
    class Binary:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

    class Unary:
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right

    class Literal:
        def __init__(self, value):
            self.value = value

    class Grouping:
        def __init__(self, expression):
            self.expression = expression


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    class ParseError(Exception):
        pass

    def parse(self):
        try:
            return self.expression()
        except self.ParseError:
            return None

    def report(self, line, where, message):
        print(f"[line {line}] Error{where}: {message}")

    def error(self, token, message):
        if token.type == TokenType.EOF:
            self.report(token.line, " at end", message)
        else:
            self.report(token.line, f" at '{token.lexeme}'", message)
        return self.ParseError()

    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.NEWLINE:
                return
            if self.peek().type in (
                TokenType.DEF, TokenType.CLASS, TokenType.FOR, TokenType.IF,
                TokenType.WHILE, TokenType.RETURN,
            ):
                return
            self.advance()

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.NOTEQ, TokenType.EQEQ):
            operator = self.previous()
            right = self.comparison()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GT, TokenType.GTEQ,
                         TokenType.LT, TokenType.LTEQ):
            operator = self.previous()
            right = self.term()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        while self.match(TokenType.DIV, TokenType.MUL):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return Expr.Literal(False)
        if self.match(TokenType.TRUE):
            return Expr.Literal(True)
        if self.match(TokenType.NONE):
            return Expr.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Expr.Literal(self.previous().literal)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        raise self.error(self.peek(), "Expect expression.")


class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token


class Interpreter:
    def evaluate(self, expr):
        if isinstance(expr, Expr.Literal):
            return expr.value
        elif isinstance(expr, Expr.Grouping):
            return self.evaluate(expr.expression)
        elif isinstance(expr, Expr.Unary):
            right = self.evaluate(expr.right)
            if expr.operator.type == TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -right
            if expr.operator.type == TokenType.NOT:
                return not self.is_truthy(right)
        elif isinstance(expr, Expr.Binary):
            left = self.evaluate(expr.left)
            right = self.evaluate(expr.right)

            if expr.operator.type == TokenType.PLUS:
                if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                    return left + right
                if isinstance(left, str) and isinstance(right, str):
                    return left + right
                if isinstance(left, str) and isinstance(right, (int, float)):
                    return left+str(right)
                if isinstance(left, (int, float)) and isinstance(right, str):
                    return str(left)+right
                raise RuntimeError(
                    expr.operator, "Operands must be two numbers or two strings.")

            if expr.operator.type == TokenType.MINUS:
                self.check_number_operands(expr.operator, left, right)
                return left - right

            if expr.operator.type == TokenType.MUL:
                self.check_number_operands(expr.operator, left, right)
                return left * right

            if expr.operator.type == TokenType.DIV:
                self.check_number_operands(expr.operator, left, right)
                if right == 0:
                    raise RuntimeError(expr.operator, "Division by zero.")
                return left / right

            if expr.operator.type == TokenType.EQEQ:
                return left == right
            if expr.operator.type == TokenType.NOTEQ:
                return left != right
            if expr.operator.type == TokenType.GT:
                self.check_number_operands(expr.operator, left, right)
                return left > right
            if expr.operator.type == TokenType.GTEQ:
                self.check_number_operands(expr.operator, left, right)
                return left >= right
            if expr.operator.type == TokenType.LT:
                self.check_number_operands(expr.operator, left, right)
                return left < right
            if expr.operator.type == TokenType.LTEQ:
                self.check_number_operands(expr.operator, left, right)
                return left <= right

        return None

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    def check_number_operand(self, operator, operand):
        if not isinstance(operand, (int, float)):
            raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise RuntimeError(operator, "Operands must be numbers.")


def print_ast(expr, indent=0):
    pad = "  " * indent
    if isinstance(expr, Expr.Binary):
        print(f"{pad}Binary({expr.operator.lexeme})")
        print_ast(expr.left, indent + 1)
        print_ast(expr.right, indent + 1)
    elif isinstance(expr, Expr.Unary):
        print(f"{pad}Unary({expr.operator.lexeme})")
        print_ast(expr.right, indent + 1)
    elif isinstance(expr, Expr.Literal):
        print(f"{pad}Literal({expr.value})")
    elif isinstance(expr, Expr.Grouping):
        print(f"{pad}Grouping")
        print_ast(expr.expression, indent + 1)
    else:
        print(f"{pad}{expr}")


def main():
    print("Enter Python-like expression below. Press Enter twice to finish:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    source_code = "\n".join(lines)
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    ast = parser.parse()

    print("\n[AST Output]:")
    if ast is None:
        print("Parsing failed due to syntax errors.")
    else:
        print_ast(ast)

        interpreter = Interpreter()
        try:
            result = interpreter.evaluate(ast)
            print("\n[Interpreter Result]:", result)
        except RuntimeError as e:
            print(f"\nRuntime Error at '{e.token.lexeme}': {e}")


if __name__ == "__main__":
    main()
