from typing import List
from scanner import Token, TokenType

class ParseError(Exception):
    pass

class StmtVisitor:
    def visitPrintStmt(self, stmt): pass
    def visitExpressionStmt(self, stmt): pass
    def visitVarStmt(self, stmt): pass
    def visitBlockStmt(self, stmt): pass
    def visitIfStmt(self, stmt): pass


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

    class If:
        def __init__(self, condition, then_branch, elif_branches=None, else_branch=None):
            self.condition = condition   
            self.then_branch = then_branch         
            self.elif_branches = elif_branches or [] 
            self.else_branch = else_branch             

        def accept(self, visitor: StmtVisitor):
            return visitor.visitIfStmt(self)


class ExprVisitor:
    def visitBinaryExpr(self, expr): pass
    def visitUnaryExpr(self, expr): pass
    def visitLiteralExpr(self, expr): pass
    def visitGroupingExpr(self, expr): pass
    def visitVariableExpr(self, expr): pass
    def visitAssignExpr(self, expr): pass
    def visitLogicalExpr(self, expr): pass

class Expr:
    class Binary:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right
        def accept(self, visitor:ExprVisitor):
            return visitor.visitBinaryExpr(self)

    class Unary:
        def __init__(self, operator, right):
            self.operator = operator
            self.right = right
        def accept(self, visitor:ExprVisitor):
            return visitor.visitUnaryExpr(self)

    class Literal:
        def __init__(self, value):
            self.value = value
        def accept(self, visitor:ExprVisitor):
            return visitor.visitLiteralExpr(self)

    class Grouping:
        def __init__(self, expression):
            self.expression = expression
        def accept(self, visitor:ExprVisitor):
            return visitor.visitGroupingExpr(self)

    class Variable:
        def __init__(self, name_token: Token):
            self.name = name_token
        def accept(self, visitor:ExprVisitor):
            return visitor.visitVariableExpr(self)

    class Assign:
        def __init__(self, name_token: Token, value):
            self.name = name_token
            self.value = value
        def accept(self, visitor:ExprVisitor):
            return visitor.visitAssignExpr(self)
        
    class Logical:
        def __init__(self, left, operator, right):
            self.left = left
            self.operator = operator
            self.right = right

        def accept(self, visitor:ExprVisitor):
            return visitor.visitLogicalExpr(self)

        
    

class ASTTreePrinter(ExprVisitor, StmtVisitor):
    def print(self, stmt, indent=0):
        self.indent = indent
        return stmt.accept(self)

    def _pad(self, text):
        return "  " * self.indent + text + "\n"

    # ----------------- Expr Visitors -----------------
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
    
    def visitLogicalExpr(self, expr):
        s = self._pad(f"Logical({expr.operator.lexeme})")
        self.indent += 1
        s += expr.left.accept(self)
        s += expr.right.accept(self)
        self.indent -= 1
        return s


    # ----------------- Stmt Visitors -----------------
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

    def visitVarStmt(self, stmt):
        s = self._pad(f"VarStmt({stmt.name.lexeme})")
        if stmt.initializer:
            self.indent += 1
            s += stmt.initializer.accept(self)
            self.indent -= 1
        return s

    def visitBlockStmt(self, stmt):
        s = self._pad("BlockStmt(")
        self.indent += 1
        for st in stmt.statements:
            s += st.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s
    
    def visitIfStmt(self, stmt):
        s = self._pad("IfStmt(")
        self.indent += 1

        # Main If Condition
        s += self._pad("Condition:")
        self.indent += 1
        s += stmt.condition.accept(self)
        self.indent -= 1

        # Then branch
        s += self._pad("Then:")
        self.indent += 1
        s += stmt.then_branch.accept(self)
        self.indent -= 1

        # Elif branches
        for idx, (elif_cond, elif_body) in enumerate(stmt.elif_branches):
            s += self._pad(f"Elif {idx + 1} Condition:")
            self.indent += 1
            s += elif_cond.accept(self)
            self.indent -= 1

            s += self._pad(f"Elif {idx + 1} Then:")
            self.indent += 1
            s += elif_body.accept(self)
            self.indent -= 1

        # Else branch
        if stmt.else_branch is not None:
            s += self._pad("Else:")
            self.indent += 1
            s += stmt.else_branch.accept(self)
            self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s




# ----------------- Main parse -----------------

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
        except ParseError as e:
            print(f"[Parser Error] {e}")
            self.synchronize()
            return None


    # ----------------- Statements -----------------
    def statement(self):
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.INDENT):
            return Stmt.Block(self.block())
        return self.expression_statement()

    def if_statement(self):
        condition = self.expression()
        self.consume(TokenType.COLON, "Expect ':' after 'if' condition.")
        then_branch = self.suite()

        elif_branches = []
        while self.match(TokenType.ELIF):
            cond = self.expression()
            self.consume(TokenType.COLON, "Expect ':' after 'elif' condition.")
            body = self.suite()
            elif_branches.append((cond, body))

        else_branch = None
        if self.match(TokenType.ELSE):
            self.consume(TokenType.COLON, "Expect ':' after 'else'.")
            else_branch = self.suite()

        return Stmt.If(condition, then_branch, elif_branches, else_branch)



    def suite(self):

        if self.match(TokenType.NEWLINE):
            self.consume(TokenType.INDENT, "Expect indentation after newline.")
            statements = []
            while not self.check(TokenType.DEDENT) and not self.is_at_end():
                statements.append(self.statement())
            self.consume(TokenType.DEDENT, "Expect DEDENT after block.")
            return Stmt.Block(statements)
        else:
            return self.statement()

        


    def print_statement(self):
        
        if self.match(TokenType.LPAREN):
            value = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after print value.")
        else:
            value = self.expression()
        # Accept newline
        self.match(TokenType.NEWLINE)
        return Stmt.Print(value)

    def expression_statement(self):
        expr = self.expression()
        if isinstance(expr, Expr.Assign):
            stmt = Stmt.Var(expr.name, expr.value)
        else:
            stmt = Stmt.Expression(expr)

        # Consume NEWLINE if present
        if self.match(TokenType.NEWLINE):
            return stmt

        # Consume EOF if it's next
        if self.is_at_end():
            self.advance()  # move past EOF so main loop finishes correctly
            return stmt

        self.error(self.peek(), "Expect end of statement (newline or EOF).")


    # ----------------- Expressions -----------------
    def expression(self):
        return self.or_()

    def or_(self):
        expr = self.and_()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Expr.Logical(expr, operator, right)  # Logical is an AST node

        return expr
    
    def and_(self):
        expr = self.assignment()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.assignment()
            expr = Expr.Logical(expr, operator, right)  # Logical AST node

        return expr



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
            return Expr.Literal(self.previous().literal)
        if self.match(TokenType.LPAREN):
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after expression.")
            return Expr.Grouping(expr)
        if self.match(TokenType.IDENTIFIER):
            return Expr.Variable(self.previous())
        raise ParseError(f"[line {self.peek().line}] Error at '{self.peek().lexeme}': Expect expression.")

    # ----------------- Helpers -----------------
    def match(self, *types):
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)

    def check(self, token_type):
        if self.is_at_end(): return False
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
            if stmt:
                statements.append(stmt)
        self.consume(TokenType.DEDENT, "Expect block to end (DEDENT).")
        return statements
