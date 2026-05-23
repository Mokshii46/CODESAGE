from codesage.parser import ExprVisitor, StmtVisitor


class Resolver(ExprVisitor, StmtVisitor):
    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.scopes = []  # stack of scopes

    def visit_block_stmt(self, stmt):
        self.begin_scope()
        self.resolve(stmt.statements)
        self.end_scope()
        return None

    def resolve(self, statements):
        if isinstance(statements, list):
            for statement in statements:
                self.resolve(statement)
        else:
            statements.accept(self)

    def resolve_expr(self, expr):
        expr.accept(self)

    def begin_scope(self):
        self.scopes.append({})

    def end_scope(self):
        self.scopes.pop()

    def visit_var_stmt(self, stmt):
        self.declare(stmt.name)
        if stmt.initializer is not None:
            self.resolve_expr(stmt.initializer)
        self.define(stmt.name)
        return None

    def declare(self, name):
        if not self.scopes:
            return  

        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.error(name, "Already a variable with this name in this scope.")
        else:  
            scope[name.lexeme] = False  

    def define(self, name):
        if not self.scopes:
            return  
        self.scopes[-1][name.lexeme] = True  

    def error(self, token, message):
        print(f"[line {token.line}] Error at '{token.lexeme}': {message}")

    def visit_variable_expr(self, expr):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            self.error(expr.name, "Can't read local variable in its own initializer.")

        self.resolve_local(expr, expr.name)
        return None

    def resolve_local(self, expr, name):
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
            
    def visit_assign_expr(self, expr):
        self.resolve(expr.value)
        self.resolve_local(expr, expr.name)
        return None

    def visit_function_stmt(self, stmt):
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolve_function(stmt)
        return None

    def resolve_function(self, function):
        self.begin_scope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.end_scope()

    def visit_expression_stmt(self, stmt):
        self.resolve(stmt.expression)
        return None

    def visit_if_stmt(self, stmt):
        # resolve the main condition + body
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)

        
        for cond, branch in stmt.elif_branches:
            self.resolve(cond)
            self.resolve(branch)

        
        if stmt.else_branch is not None:
            self.resolve(stmt.else_branch)

        return None

    def visit_print_stmt(self, stmt):
        self.resolve_expr(stmt.expression)
        return None

    def visit_return_stmt(self, stmt):
        if stmt.value is not None:
            self.resolve_expr(stmt.value)
        return None

    def visit_while_stmt(self, stmt):
        self.resolve_expr(stmt.condition)
        self.resolve(stmt.body)
        return None

    def visit_binary_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None

    def visit_call_expr(self, expr):
        self.resolve_expr(expr.callee)
        for argument in expr.arguments:
            self.resolve_expr(argument)
        return None

    def visit_grouping_expr(self, expr):
        self.resolve_expr(expr.expression)
        return None

    def visit_literal_expr(self, expr):
        return None

    def visit_logical_expr(self, expr):
        self.resolve_expr(expr.left)
        self.resolve_expr(expr.right)
        return None

    def visit_unary_expr(self, expr):
        self.resolve_expr(expr.right)
        return None
