import sys
from parser import Expr, ExprVisitor, StmtVisitor
from scanner import TokenType

class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)   
        self.token = token    

class CODESAGE:
    had_error = False
    had_runtime_error = False
    interpreter = None  

    @staticmethod
    def runtime_error(error):
        print(f"{error}\n[line {getattr(error.token, 'line', '?')}]", file=sys.stderr)
        CODESAGE.had_runtime_error = True

    @staticmethod
    def interpret(statements):
        if CODESAGE.had_error:
            return
        try:
            for stmt in statements:
                CODESAGE.interpreter.execute(stmt)
        except RuntimeError as error:
            CODESAGE.runtime_error(error)     

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name: str, value):
        self.values[name] = value

    def get(self, name_token):
        name = name_token.lexeme
        if name in self.values:
            return self.values[name]
        if self.enclosing:
            return self.enclosing.get(name_token)
        raise RuntimeError(name_token, f"Undefined variable '{name}'.")

    def assign(self, name_token, value):
        name = name_token.lexeme
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing:
            self.enclosing.assign(name_token, value)
            return
        # If variable doesn't exist, define it in current scope
        self.define(name, value)

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.environment = Environment()

    # --- Statement Execution ---
    def execute(self, stmt):
        return stmt.accept(self)

    def interpret(self, statements):
        try:
            for stmt in statements:
                self.execute(stmt)
        except RuntimeError as error:
            CODESAGE.runtime_error(error)

    def visitExpressionStmt(self, stmt):
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None

    def visitVarStmt(self, stmt):
        value = None
        if stmt.initializer:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visitBlockStmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    
    def visitIfStmt(self, stmt):
        # Check main IF condition
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
            return None

        # Check ELIF branches (if any)
        for elif_cond, elif_body in stmt.elif_branches:
            if self.is_truthy(self.evaluate(elif_cond)):
                self.execute(elif_body)
                return None

        # Else branch (if no IF or ELIF matched)
        if stmt.else_branch is not None:
            self.execute(stmt.else_branch)

        return None



    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for stmt in statements:
                self.execute(stmt)
        finally:
            self.environment = previous

    # --- Expression Evaluation ---
    def evaluate(self, expr):
        return expr.accept(self)

    def visitLiteralExpr(self, expr):
        return expr.value

    def visitGroupingExpr(self, expr):
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        if expr.operator.type == TokenType.NOT:
            return not self.is_truthy(right)
        return None

    def visitBinaryExpr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        op = expr.operator.type

        if op == TokenType.PLUS:
            if isinstance(left, (int, float)) and isinstance(right, (int, float)):
                return left + right
            if isinstance(left, str) and isinstance(right, str):
                return left + right
            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")

        if op == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        if op == TokenType.MUL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
        if op == TokenType.DIV:
            self.check_number_operands(expr.operator, left, right)
            if right == 0:
                raise RuntimeError(expr.operator, "Division by zero.")
            return float(left) / float(right)

        if op == TokenType.GT:
            self.check_number_operands(expr.operator, left, right)
            return left > right
        if op == TokenType.GTEQ:
            self.check_number_operands(expr.operator, left, right)
            return left >= right
        if op == TokenType.LT:
            self.check_number_operands(expr.operator, left, right)
            return left < right
        if op == TokenType.LTEQ:
            self.check_number_operands(expr.operator, left, right)
            return left <= right

        if op == TokenType.EQEQ:
            return self.is_equal(left, right)
        if op == TokenType.NOTEQ:
            return not self.is_equal(left, right)

        return None

    def visitVariableExpr(self, expr):
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)
        return value

    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else: 
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)

    # --- Helpers ---
    def is_truthy(self, obj):
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True

    def is_equal(self, a, b):
        return a == b

    def stringify(self, obj):
        if obj is None: return "nil"
        if isinstance(obj, float) and obj.is_integer():
            return str(int(obj))
        return str(obj)

    def check_number_operand(self, operator, operand):
        if not isinstance(operand, (int, float)):
            raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            raise RuntimeError(operator, "Operands must be numbers.")
