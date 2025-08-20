import sys
from parser import Expr,ExprVisitor
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
    def interpret(expression):
        if CODESAGE.had_error:
            return  
        try:
            value = CODESAGE.interpreter.evaluate(expression)
            print(CODESAGE.interpreter.stringify(value))
        except RuntimeError as error:
            CODESAGE.runtime_error(error)     

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value):
        self.values[name] = value

    def get(self, name_token):
        name = name_token.lexeme
        if name in self.values:
            return self.values[name]
        raise RuntimeError(name_token, f"Undefined variable '{name}'.")

    def assign(self, name_token, value):
        name = name_token.lexeme
        if name in self.values:
            self.values[name] = value
            return
        raise RuntimeError(name_token, f"Undefined variable '{name}'.")

class Interpreter(ExprVisitor):
    def __init__(self):
        self.environment = Environment()

    def interpret(self, expr: Expr):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RuntimeError as error:
            CODESAGE.runtime_error(error)
        
    def evaluate(self, expr: Expr):
        return expr.accept(self)

    def visitLiteralExpr(self, expr: Expr.Literal):
        return expr.value

    def visitGroupingExpr(self, expr: Expr.Grouping):
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: Expr.Unary):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        if expr.operator.type == TokenType.NOT:
            return not self.is_truthy(right)
        return None

    def visitBinaryExpr(self, expr: Expr.Binary):
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
            return float(left) > float(right)
        if op == TokenType.GTEQ:
            self.check_number_operands(expr.operator, left, right) 
            return float(left) >= float(right)
        if op == TokenType.LT:          
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if op == TokenType.LTEQ:  
            self.check_number_operands(expr.operator, left, right)  
            return float(left) <= float(right)
        if op == TokenType.EQEQ: return self.is_equal(left, right)
        if op == TokenType.NOTEQ: return not self.is_equal(left, right)
        return None

    def visitVariableExpr(self, expr: Expr.Variable):
        return self.environment.get(expr.name)

    def visitAssignExpr(self, expr: Expr.Assign):
        value = self.evaluate(expr.value)
        self.environment.define(expr.name.lexeme, value)
        return value

    def is_truthy(self, obj):
        if obj is None: return False
        if isinstance(obj, bool): return obj
        return True

    def is_equal(self, a, b):
        return a == b

    def stringify(self, obj):
        if obj is None:
            return "nil"
        if isinstance(obj, float) and obj.is_integer():
            return str(int(obj))
        return str(obj)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, (int, float)): 
            return
        raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, (int, float)) and isinstance(right, (int, float)):
            return
        raise RuntimeError(operator, "Operands must be numbers.")
