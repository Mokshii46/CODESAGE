from typing import List
from scanner import Token
from scanner import TokenType,Scanner

class ExprVisitor:
    def visitBinaryExpr(self, expr): pass
    def visitUnaryExpr(self, expr): pass
    def visitLiteralExpr(self, expr): pass
    def visitGroupingExpr(self, expr): pass
    def visitVariableExpr(self,expr): pass
    def visitAssignExpr(self, expr): pass

class ASTTreePrinter:
    def print(self, expr, indent=0):
        self.indent = indent
        return expr.accept(self)

    def _pad(self, text):
        return "  " * self.indent + text + "\n"

    def visitLiteralExpr(self, expr):
        return self._pad(f"Literal({expr.value})")

    def visitGroupingExpr(self, expr):
        s = self._pad("Grouping(")
        self.indent += 1
        s += expr.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitUnaryExpr(self, expr):
        s = self._pad(f"Unary({expr.operator.lexeme})")
        self.indent += 1
        s += expr.right.accept(self)
        self.indent -= 1
        return s

    def visitBinaryExpr(self, expr):
        s = self._pad(f"Binary({expr.operator.lexeme})")
        self.indent += 1
        s += expr.left.accept(self)
        s += expr.right.accept(self)
        self.indent -= 1
        return s

    def visitVariableExpr(self, expr):
        return self._pad(f"Variable({expr.name.lexeme})")

    def visitAssignExpr(self, expr):
        s = self._pad(f"Assign({expr.name.lexeme})")
        self.indent += 1
        s += expr.value.accept(self)
        self.indent -= 1
        return s



class Expr:
    class Binary:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right
        def accept(self, visitor):
            return visitor.visitBinaryExpr(self)

    class Unary:
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right
        def accept(self, visitor):
            return visitor.visitUnaryExpr(self)

    class Literal:
        def __init__(self, value):
            self.value = value
        def accept(self, visitor):
            return visitor.visitLiteralExpr(self)

    class Grouping:
        def __init__(self, expression):
            self.expression = expression
        def accept(self, visitor):
            return visitor.visitGroupingExpr(self)


    class Variable:
        def __init__(self, name_token: Token):
            self.name = name_token
        def accept(self, visitor):
            return visitor.visitVariableExpr(self)
    
    class Assign:
        def __init__(self, name_token: Token, value):
            self.name = name_token
            self.value = value
        def accept(self, visitor):
            return visitor.visitAssignExpr(self)
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0 

    


    def parse(self):
        statements = []
        while not self.is_at_end():
    
            while self.match(TokenType.NEWLINE):
                pass
            if self.is_at_end():
                break
            statements.append(self.assignment())
        return statements
        



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
    
    def assignment(self):
        expr=self.equality()

        if self.match(TokenType.ASSIGN):
            operator=self.previous()
            value=self.assignment()
            if isinstance(expr, Expr.Variable):
                name_token = expr.name
                return Expr.Assign(name_token, value)
            else:
                raise Exception(f"[line {operator.line}] Invalid assignment target.")
        return expr

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

        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())
        
        raise Exception(f"[line {self.peek().line}] Error at '{self.peek().lexeme}': Expect expression.")




