from typing import List
from scanner import Token
from scanner import TokenType,Scanner

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
    print("Enter Python-like code below. Press Enter twice to finish:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    
    source_code = "\n".join(lines)
    scanner = Scanner(source_code)
    tokens = scanner.scan_tokens()
    
    print("\nScanned Tokens:")
    for token in tokens:
        print(token)


    parser = Parser(tokens)
    ast = parser.parse()

    print("\n[Parser Output]:")
    if ast is None:
        print("Parsing failed due to syntax errors.")
    else:
        print_ast(ast)



if __name__ == "__main__":
    main()
