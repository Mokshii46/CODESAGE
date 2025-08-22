from typing import List
from scanner import Token
from scanner import TokenType

class ParseError(Exception):
    pass

class StmtVisitor:
    def visitPrintStmt(self, stmt): pass
    def visitExpressionStmt(self, stmt): pass
    def visitVarStmt(self, stmt): pass
    def visitBlockStmt(self, stmt): pass

class Stmt:
    class Var:
        def __init__(self, name, initializer):
            self.name = name
            self.initializer = initializer
        def accept(self, visitor: StmtVisitor):
            return visitor.visitVarStmt(self)
    class Block:
        def __init__(self, statements):
            self.statements = statements
        def accept(self, visitor: StmtVisitor):
            return visitor.visitBlockStmt(self)
    class Print:
        def __init__(self, expression):
            self.expression = expression
        def accept(self, visitor: StmtVisitor):
            return visitor.visitPrintStmt(self)
    class Expression:
        def __init__(self, expression):
            self.expression = expression
        def accept(self, visitor: StmtVisitor):
            return visitor.visitExpressionStmt(self)

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

    def visitPrintStmt(self, stmt):
        s = self._pad("PrintStmt(")
        self.indent += 1
        s += stmt.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitExpressionStmt(self, stmt):
        s = self._pad("ExpressionStmt(")
        self.indent += 1
        s += stmt.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitBlockStmt(self, stmt):
        s = self._pad("BlockStmt(")
        self.indent += 1
        for st in stmt.statements:
            s += st.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
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
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        return statements
    
    def declaration(self):
        try:
            return self.statement()
        except ParseError:
            self.synchronize()
            return None

    def statement(self):
        print("Current token:", self.peek())   # debug
        if self.check(TokenType.PRINT):
            print("Parsing print statement")  # debug
            return self.print_statement()
        if self.match(TokenType.INDENT):
            return Stmt.Block(self.block())
        return self.expression_statement()


    def print_statement(self):
        self.consume(TokenType.PRINT, "Expect 'print'.")
        print("Inside print_statement")  # DEBUG
        if self.consume(TokenType.LPAREN,"Expect '(' after value in print statement."):
            value = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after value in print statement.")
        else:
            value = self.expression()
        self.consume_end_of_statement("Expect newline or EOF after print statement.")
        print("Returning Stmt.Print with value:", value)  # DEBUG
        return Stmt.Print(value)
        
        # Ensure end of statement
       
    def expression_statement(self):
        expr = self.expression()
        if self.match(TokenType.NEWLINE) or self.check(TokenType.EOF):
            return Stmt.Expression(expr)
        else:
            self.error(self.peek(), "Expect end of statement (newline or EOF).")

    
        
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.ASSIGN):
            initializer = self.expression()
        self.consume_end_of_statement("Expect newline after variable declaration.")
        return Stmt.Var(name, initializer)


    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.ASSIGN):
            operator = self.previous()
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                return Expr.Assign(expr.name, value)
            else:
                raise ParseError(f"[line {operator.line}] Invalid assignment target.")
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
        while self.match(TokenType.GT, TokenType.GTEQ, TokenType.LT, TokenType.LTEQ):
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
        if self.match(TokenType.FALSE): return Expr.Literal(False)
        if self.match(TokenType.TRUE): return Expr.Literal(True)
        if self.match(TokenType.NONE): return Expr.Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            literal_value = self.previous().literal
            print("Matched NUMBER/STRING:", literal_value)
            return Expr.Literal(literal_value)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())
        raise Exception(f"[line {self.peek().line}] Error at '{self.peek().lexeme}': Expect expression.")

    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type): return self.advance()
        raise self.error(self.peek(), message)

    def check(self, token_type):
        if self.is_at_end(): return False
        return self.peek().type == token_type

    def advance(self):
        if not self.is_at_end(): self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def error(self, token, message):
        raise ParseError(f"[line {token.line}] Error at '{token.lexeme}': {message}")

    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.NEWLINE: return
            if self.peek().type in (TokenType.DEF, TokenType.CLASS, TokenType.FOR,
                                    TokenType.IF, TokenType.WHILE, TokenType.RETURN):
                return
            self.advance()

    def block(self):
        statements = []
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            stmt = self.declaration()
            if stmt is not None:
                statements.append(stmt)
        self.consume(TokenType.DEDENT, "Expect block to end (dedent).")
        return statements

    def consume_end_of_statement(self, message):
        if self.match(TokenType.NEWLINE):
            return
        if self.check(TokenType.EOF):
            self.advance()   # <-- Advance EOF token
            return
        raise self.error(self.peek(), message)

