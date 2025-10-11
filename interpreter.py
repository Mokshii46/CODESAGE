import sys
from parser import Expr, ExprVisitor, StmtVisitor
from scanner import TokenType
from abc import ABC, abstractmethod




class PyCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments):
        pass

    @abstractmethod
    def arity(self):
        pass

class PyFunction(PyCallable):
    def __init__(self, declaration, closure=None):
        self.declaration = declaration
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure or interpreter.globals)
        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])

        try:
            if hasattr(self.declaration.body, "statements"):
                interpreter.execute_block(self.declaration.body.statements, environment)
            else:
                interpreter.execute_block(self.declaration.body, environment)

        except ReturnException as r:
            return r.value 
        return None  

    def __str__(self):
        return f"<fn {self.declaration.name.lexeme}>"

class ClockFunction:
    def arity(self):
        return 0  

    def call(self, interpreter, arguments):
        import time
        return time.time() 

    def __str__(self):
        return "<native fn>"

class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)   
        self.token = token 

class BreakException(Exception):
    pass
class ContinueException(Exception):
    pass
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value



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
        if isinstance(name_token, str):
            name = name_token
        else:
            name = name_token.lexeme

        if name in self.values:
            return self.values[name]

        if self.enclosing:
            return self.enclosing.get(name_token)

        raise RuntimeError(name_token, f"Undefined variable '{name}'.")


    def assign(self, name_token, value):
        if isinstance(name_token, str):
            name = name_token
        else:
            name = name_token.lexeme

        if name in self.values:
            self.values[name] = value
            return

        if self.enclosing:
            self.enclosing.assign(name_token, value)
            return

        # If not found anywhere, define in current environment
        self.define(name, value)


    def get_at(self, distance, name):
        return self.ancestor(distance).values[name]

    def assign_at(self, distance, name_token, value):
        self.ancestor(distance).values[name_token.lexeme] = value

    def ancestor(self, distance):
        env = self
        for _ in range(distance):
            env = env.enclosing
        return env

class Interpreter(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.globals= Environment()
        self.environment=self.globals
        self.globals.define("clock", ClockFunction())
        self.locals = {}

    def resolve(self, expr, depth):
        # expr: an Expr object
        # depth: integer, how many scopes up the variable is
        self.locals[expr] = depth

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
        if stmt.name.lexeme not in self.environment.values:
            self.environment.define(stmt.name.lexeme, value)
        else:
            self.environment.assign(stmt.name, value)
        return None

    def visitBlockStmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))

    
    def visitIfStmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
            return None
        for elif_cond, elif_body in stmt.elif_branches:
            if self.is_truthy(self.evaluate(elif_cond)):
                self.execute(elif_body)
                return None
        if stmt.else_branch is not None:
            self.execute(stmt.else_branch)

        return None

    def visitWhileStmt(self, stmt):
        iteration = 0
        while self.is_truthy(self.evaluate(stmt.condition)):
            try:
                self.execute(stmt.body) 
            except BreakException:
                break  
            except ContinueException:
                continue  

            iteration += 1
            if iteration > 50: 
                print("[DEBUG] Breaking possible infinite loop.")
                break

        
    
    def visitListLiteral(self, expr):
        return [self.evaluate(e) for e in expr.elements]

    def visitIndexExpr(self, expr):
        collection = self.evaluate(expr.collection)
        index = self.evaluate(expr.index_expr)  
        if not isinstance(collection, list):
            raise RuntimeError(expr.collection, "Indexing only supported on lists.")
        if not isinstance(index, (int, float)):
            raise RuntimeError("List index must be a number.")
        index = int(index)
        if index < 0 or index >= len(collection):
            raise RuntimeError(expr.index_expr, "List index out of range.")
        return collection[index]

    def visitIndexAssignExpr(self, expr):
        collection = self.evaluate(expr.collection)
        index = self.evaluate(expr.index_expr)
        value = self.evaluate(expr.value_expr)  

        if not isinstance(collection, list):
            raise RuntimeError(expr.collection, "Index assignment only supported on lists.")
        if not isinstance(index, (int, float)):
            raise RuntimeError("List index must be a number.")
        index = int(index)
        if index < 0 or index >= len(collection):
            raise RuntimeError(expr.index_expr, "List index out of range.")

        collection[index] = value
        return value
    
    def visitRangeExpr(self, expr):
        args = [self.evaluate(a) for a in expr.args]
        ints = []
        for a in args:
            if isinstance(a, (int, float, bool)):
                ints.append(int(a))
            else:
                raise RuntimeError(None, "range() arguments must be numbers.")
        if len(ints) == 1:  return range(ints[0])
        if len(ints) == 2:  return range(ints[0], ints[1])
        if len(ints) == 3:  return range(ints[0], ints[1], ints[2])
        raise RuntimeError(None, "range() takes 1 to 3 arguments.")

    def visitLenExpr(self, expr):
        target = self.evaluate(expr.target)
        try:
            return len(target)
        except Exception:
            raise RuntimeError(None, "object has no len().")


    def visitForStmt(self, stmt):
        iterable_value = self.evaluate(stmt.iterable)
        if isinstance(iterable_value, (int, float, bool)):
            iterable_value = range(int(iterable_value))

        if not hasattr(iterable_value, "__iter__"):
            raise RuntimeError(stmt.name, "Object is not iterable.")
        
        for v in iterable_value:
            self.environment.assign(stmt.name, v)
            try:
                self.execute(stmt.body)
            except BreakException:
                break
            except ContinueException:
                continue
        
        return None

    def visitBreakStmt(self, stmt):
        raise BreakException()
    
    def visitContinueStmt(self, stmt):
        raise ContinueException()


    def visitFunctionStmt(self, stmt):
        function = PyFunction(stmt,self.environment)
        
        self.environment.define(stmt.name.lexeme, function)
        
        return None

    def visitReturnStmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise ReturnException(value)



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
        if op == TokenType.REM:
            self.check_number_operands(expr.operator, left, right)
            return float(left) % float(right)


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
        distance = self.locals.get(expr)
        if distance is not None:
            return self.environment.get_at(distance, expr.name.lexeme)
        else:
            # Look in current environment first, then globals
            return self.environment.get(expr.name)


    def visitAssignExpr(self, expr):
        value = self.evaluate(expr.value)
        distance = self.locals.get(expr)
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.environment.assign(expr.name, value)  # ✅ Use assign() and pass Token
        return value



    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)

        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:  # AND
            if not self.is_truthy(left):
                return left

        return self.evaluate(expr.right)
    
    def visitCallExpr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, PyCallable):
            raise RuntimeError("Can only call functions and classes.")
        
        function = callee  
        if len(arguments) != function.arity():
            raise RuntimeError(expr.paren,f"Expected {function.arity()} arguments but got {len(arguments)}."
            )

        return callee.call(self, arguments)


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
