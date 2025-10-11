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
    def visitWhileStmt(self, stmt): pass
    def visitForStmt(self,stmt): pass
    def visitBreakStmt(self,stmt):pass
    def visitContinueStmt(self,stmt):pass
    def visitFunctionStmt(self,stmt):pass
    


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
        
    class While:
        def __init__(self, condition, body):
            self.condition = condition 
            self.body = body          

        def accept(self, visitor:StmtVisitor):
            return visitor.visitWhileStmt(self)
        
    class For:
        def __init__(self, name, iterable, body):
            self.name = name
            self.iterable = iterable
            self.body = body

        def accept(self, visitor:StmtVisitor):
            return visitor.visitForStmt(self)
    class Break:
        def accept(self, visitor:StmtVisitor):
            return visitor.visitBreakStmt(self)
        
    class Continue:
        def accept(self, visitor:StmtVisitor):
            return visitor.visitContinueStmt(self)
        
    class Function:
        def __init__(self, name, params, body):
            self.name = name        
            self.params = params    
            self.body = body        

        def accept(self, visitor:StmtVisitor):
            return visitor.visitFunctionStmt(self)

    class Return:
        def __init__(self, keyword, value):
            self.keyword = keyword
            self.value = value

        def accept(self, visitor):
            return visitor.visitReturnStmt(self)






class ExprVisitor:
    def visitBinaryExpr(self, expr): pass
    def visitUnaryExpr(self, expr): pass
    def visitLiteralExpr(self, expr): pass
    def visitGroupingExpr(self, expr): pass
    def visitVariableExpr(self, expr): pass
    def visitAssignExpr(self, expr): pass
    def visitLogicalExpr(self, expr): pass
    def visitListLiteral(self, expr): pass
    def visitIndexExpr(self, expr): pass
    def visitIndexAssignExpr(self, expr): pass
    def visitLenExpr(self, expr): pass
    def visitRangeExpr(self, expr): pass
    def visitCallExpr(self, expr): pass


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
        
    class ListLiteral:
        def __init__(self, elements):
            self.elements = elements
        def accept(self, visitor: ExprVisitor):
            return visitor.visitListLiteral(self)

    class Index:
        def __init__(self, collection, index_expr):
            self.collection = collection
            self.index_expr = index_expr
        def accept(self, visitor: ExprVisitor):
            return visitor.visitIndexExpr(self)

    class IndexAssign:
        def __init__(self, collection, index_expr, value_expr):
            self.collection = collection
            self.index_expr = index_expr
            self.value_expr = value_expr
        def accept(self, visitor: ExprVisitor):
            return visitor.visitIndexAssignExpr(self)
    
    class Range:
        def __init__(self, args):
            self.args = args  # list[Expr]
        def accept(self, visitor: ExprVisitor):
            return visitor.visitRangeExpr(self)

    class Len:
        def __init__(self, target):
            self.target = target  # Expr
        def accept(self, visitor: ExprVisitor):
            return visitor.visitLenExpr(self)

    class Call:
        def __init__(self, callee, paren, arguments):
            self.callee = callee
            self.paren = paren
            self.arguments = arguments

        def accept(self, visitor:ExprVisitor):
            return visitor.visitCallExpr(self)



class ASTPathExtractor:
    def __init__(self):
        self.paths = []

    def extract_paths(self, node):
        self.paths = []
        self._visit(node, [])
        return self.paths

    def _visit(self, stmt, current_path):
        if stmt is None:
            return

        new_path = current_path + [type(stmt).__name__]
        if isinstance(stmt, Stmt.Expression):
            self._visit_expr(stmt.expression, new_path)

        elif isinstance(stmt, Stmt.Print):
            self.paths.append(new_path + ["Print"])
            self._visit_expr(stmt.expression, new_path + ["Print"])

        elif isinstance(stmt, Stmt.Var):
            self.paths.append(new_path + ["Var", stmt.name.lexeme])
            if stmt.initializer:
                self._visit_expr(stmt.initializer, new_path + ["Initializer"])

        elif isinstance(stmt, Stmt.Block):
            self.paths.append(new_path + ["Block"])
            for s in stmt.statements:
                self._visit(s, new_path + ["Block"])

        elif isinstance(stmt, Stmt.If):
            self.paths.append(new_path + ["If"])
            self._visit_expr(stmt.condition, new_path + ["Condition"])
            self._visit(stmt.then_branch, new_path + ["Then"])
            if stmt.else_branch:
                self._visit(stmt.else_branch, new_path + ["Else"])

        elif isinstance(stmt, Stmt.While):
            self.paths.append(new_path + ["While"])
            self._visit_expr(stmt.condition, new_path + ["Condition"])
            self._visit(stmt.body, new_path + ["Body"])

        elif isinstance(stmt, Stmt.Function):
            self.paths.append(new_path + ["Function", stmt.name.lexeme])
            for param in stmt.params:
                self.paths.append(new_path + ["Param", param.lexeme])
            self._visit(stmt.body, new_path + ["Body"])

        elif isinstance(stmt, Stmt.Return):
            self.paths.append(new_path + ["Return"])
            if stmt.value:
                self._visit_expr(stmt.value, new_path + ["Value"])

        elif isinstance(stmt, Stmt.Break):
            self.paths.append(new_path + ["Break"])

        elif isinstance(stmt, Stmt.Continue):
            self.paths.append(new_path + ["Continue"])

        else:
            self.paths.append(new_path + ["UnknownStmt"])

    # -----------------------
    # Expressions
    # -----------------------
    def _visit_expr(self, expr, current_path):
        if expr is None:
            return

        new_path = current_path + [type(expr).__name__]
        if isinstance(expr, Expr.Literal):
            self.paths.append(new_path + [str(expr.value)])

        elif isinstance(expr, Expr.Variable):
            self.paths.append(new_path + ["Variable", expr.name.lexeme])

        elif isinstance(expr, Expr.Assign):
            self.paths.append(new_path + ["Assign", expr.name.lexeme])
            self._visit_expr(expr.value, new_path + ["Value"])

        elif isinstance(expr, Expr.Binary):
            self.paths.append(new_path + ["Binary", expr.operator.lexeme])
            self._visit_expr(expr.left, new_path + ["Left"])
            self._visit_expr(expr.right, new_path + ["Right"])

        elif isinstance(expr, Expr.Unary):
            self.paths.append(new_path + ["Unary", expr.operator.lexeme])
            self._visit_expr(expr.right, new_path + ["Right"])

        elif isinstance(expr, Expr.Call):
            self.paths.append(new_path + ["Call"])
            self._visit_expr(expr.callee, new_path + ["Callee"])
            for arg in expr.arguments:
                self._visit_expr(arg, new_path + ["Arg"])

        elif isinstance(expr, Expr.Grouping):
            self._visit_expr(expr.expression, new_path + ["Grouping"])

        else:
            self.paths.append(new_path + ["UnknownExpr"])



    




            
        

    

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
    
    def visitListLiteral(self, expr):
        s = self._pad("ListLiteral(")
        self.indent += 1
        if not expr.elements:
            s += self._pad("<empty>")
        else:
            for el in expr.elements:
                s += el.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitIndexExpr(self, expr):
        s = self._pad("IndexExpr(")
        self.indent += 1
        s += expr.collection.accept(self)   
        s += expr.index_expr.accept(self)   
        self.indent -= 1
        s += self._pad(")")
        return s
    
    def visitIndexAssignExpr(self, expr):
        s = self._pad("IndexAssign(")
        self.indent += 1
        s += expr.collection.accept(self)
        s += expr.index_expr.accept(self)
        s += expr.value_expr.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s
    
    def visitRangeExpr(self, expr):
        s = self._pad("Range(")
        self.indent += 1
        for a in expr.args:
            s += a.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitLenExpr(self, expr):
        s = self._pad("Len(")
        self.indent += 1
        s += expr.target.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s
    
    def visitCallExpr(self, expr):
        s = self._pad("Call")
        self.indent += 1
        s += expr.callee.accept(self)

        s+=self._pad("Arguments:")
        for arg in expr.arguments:
            s += arg.accept(self)

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
        s += self._pad("Condition:")
        self.indent += 1
        s += stmt.condition.accept(self)
        self.indent -= 1
        s += self._pad("Then:")
        self.indent += 1
        s += stmt.then_branch.accept(self)
        self.indent -= 1
        for idx, (elif_cond, elif_body) in enumerate(stmt.elif_branches):
            s += self._pad(f"Elif {idx + 1} Condition:")
            self.indent += 1
            s += elif_cond.accept(self)
            self.indent -= 1

            s += self._pad(f"Elif {idx + 1} Then:")
            self.indent += 1
            s += elif_body.accept(self)
            self.indent -= 1
        if stmt.else_branch is not None:
            s += self._pad("Else:")
            self.indent += 1
            s += stmt.else_branch.accept(self)
            self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s
    
    def visitWhileStmt(self, stmt):
        s = self._pad("WhileStmt(")
        self.indent += 1

        s += self._pad("Condition:")
        self.indent += 1
        s += stmt.condition.accept(self)
        self.indent -= 1

        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1

        s += self._pad(")")
        return s

    def visitForStmt(self, stmt):
        s = self._pad("ForStmt(")
        self.indent += 1
        s += self._pad("Variable:")
        self.indent += 1
        s += self._pad(stmt.name.lexeme)
        self.indent -= 1
        s += self._pad("Iterable:")
        self.indent += 1
        s += stmt.iterable.accept(self)
        self.indent -= 1
        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s

    def visitBreakStmt(self, stmt):
        s=self._pad("BreakSTmt()")
        return s
    
    def visitContinueStmt(self, stmt):
        s=self._pad("ContinueStmt()")
        return s
    def visitFunctionStmt(self, stmt):
        s = self._pad("Function(")
        self.indent += 1
        s += self._pad("Name:")
        self.indent += 1
        s += self._pad(stmt.name.lexeme)
        self.indent -= 1

        
        s += self._pad("Params:")
        self.indent += 1
        for param in stmt.params:
            s += self._pad(param.lexeme)
        self.indent -= 1

    
        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self) 
        self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s


    def visitReturnStmt(self, stmt):
        s = self._pad("ReturnStmt(")
        self.indent += 1
        s += self._pad("Value:")
        self.indent += 1
        if stmt.value is not None:
            s += stmt.value.accept(self)
        else:
            s += self._pad("None") 
        self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s


class ASTSummarizer(ExprVisitor, StmtVisitor):
    def __init__(self):
        self.indent = 0
        self.summary_lines = []

    def _pad(self, text):
        return "  " * self.indent + text + "\n"

    def _add_summary(self, text):
        self.summary_lines.append(text)

    def print(self, stmt, indent=0):
        self.indent = indent
        return stmt.accept(self)

    def _describe_expr(self, expr):
        """Return a short, human-readable description of any expression."""
        if expr is None:
            return "None"
        # Literal values
        if hasattr(expr, "value"):
            return str(expr.value)
        # Variable names
        if hasattr(expr, "name"):
            return getattr(expr.name, "lexeme", str(expr.name))
        # Binary expressions
        if hasattr(expr, "left") and hasattr(expr, "right") and hasattr(expr, "operator"):
            left = self._describe_expr(expr.left)
            right = self._describe_expr(expr.right)
            return f"({left} {expr.operator.lexeme} {right})"
        # Unary expressions
        if hasattr(expr, "right") and hasattr(expr, "operator"):
            child = self._describe_expr(expr.right)
            return f"({expr.operator.lexeme}{child})"
        # Logical expressions
        if hasattr(expr, "left") and hasattr(expr, "right") and hasattr(expr, "operator"):
            left = self._describe_expr(expr.left)
            right = self._describe_expr(expr.right)
            return f"({left} {expr.operator.lexeme} {right})"
        # List literals
        if hasattr(expr, "elements"):
            return "[" + ", ".join([self._describe_expr(e) for e in expr.elements]) + "]"
        # Call expressions
        if hasattr(expr, "callee") and hasattr(expr, "arguments"):
            callee = self._describe_expr(expr.callee)
            args = ", ".join([self._describe_expr(a) for a in expr.arguments])
            return f"{callee}({args})"
        # Indexing
        if hasattr(expr, "collection") and hasattr(expr, "index_expr"):
            return f"{self._describe_expr(expr.collection)}[{self._describe_expr(expr.index_expr)}]"
        # Index assignment
        if hasattr(expr, "collection") and hasattr(expr, "index_expr") and hasattr(expr, "value_expr"):
            return f"{self._describe_expr(expr.collection)}[{self._describe_expr(expr.index_expr)}] = {self._describe_expr(expr.value_expr)}"
        # Range
        if hasattr(expr, "args"):
            return "range(" + ", ".join([self._describe_expr(a) for a in expr.args]) + ")"
        return "<expr>"

    # ----------------- Expression Visitors -----------------
    def visitLiteralExpr(self, expr):
        return self._pad(f"Literal({expr.value})")

    def visitVariableExpr(self, expr):
        return self._pad(f"Variable({expr.name.lexeme})")

    def visitAssignExpr(self, expr):
        self._add_summary(f"Assigning '{self._describe_expr(expr.value)}' to variable '{expr.name.lexeme}'.")
        s = self._pad(f"Assign({expr.name.lexeme})")
        self.indent += 1
        s += expr.value.accept(self)
        self.indent -= 1
        return s

    def visitUnaryExpr(self, expr):
        self._add_summary(f"This is a unary operation '{expr.operator.lexeme}' applied to {self._describe_expr(expr.right)}.")
        s = self._pad(f"Unary({expr.operator.lexeme})")
        self.indent += 1
        s += expr.right.accept(self)
        self.indent -= 1
        return s

    def visitBinaryExpr(self, expr):
        self._add_summary(f"This is a binary operation '{expr.operator.lexeme}' between left ({self._describe_expr(expr.left)}) and right ({self._describe_expr(expr.right)}).")
        s = self._pad(f"Binary({expr.operator.lexeme})")
        self.indent += 1
        s += expr.left.accept(self)
        s += expr.right.accept(self)
        self.indent -= 1
        return s

    def visitLogicalExpr(self, expr):
        self._add_summary(f"This is a logical operation '{expr.operator.lexeme}' between left ({self._describe_expr(expr.left)}) and right ({self._describe_expr(expr.right)}).")
        s = self._pad(f"Logical({expr.operator.lexeme})")
        self.indent += 1
        s += expr.left.accept(self)
        s += expr.right.accept(self)
        self.indent -= 1
        return s

    def visitGroupingExpr(self, expr):
        self._add_summary("This is a grouping expression (parentheses) around a sub-expression.")
        s = self._pad("Grouping(")
        self.indent += 1
        s += expr.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitListLiteral(self, expr):
        self._add_summary(f"This is a list literal with elements: {self._describe_expr(expr)}")
        s = self._pad("ListLiteral(")
        self.indent += 1
        for el in expr.elements:
            s += el.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitIndexExpr(self, expr):
        self._add_summary(f"Accessing index {self._describe_expr(expr.index_expr)} of {self._describe_expr(expr.collection)}")
        s = self._pad("IndexExpr(")
        self.indent += 1
        s += expr.collection.accept(self)
        s += expr.index_expr.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitIndexAssignExpr(self, expr):
        self._add_summary(f"Assigning {self._describe_expr(expr.value_expr)} to index {self._describe_expr(expr.index_expr)} of {self._describe_expr(expr.collection)}")
        s = self._pad("IndexAssign(")
        self.indent += 1
        s += expr.collection.accept(self)
        s += expr.index_expr.accept(self)
        s += expr.value_expr.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitRangeExpr(self, expr):
        self._add_summary(f"This is a range expression: {self._describe_expr(expr)}")
        s = self._pad("Range(")
        self.indent += 1
        for a in expr.args:
            s += a.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitLenExpr(self, expr):
        self._add_summary(f"This expression computes the length of {self._describe_expr(expr.target)}")
        s = self._pad("Len(")
        self.indent += 1
        s += expr.target.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitCallExpr(self, expr):
        callee_name = self._describe_expr(expr.callee)
        arg_vals = [self._describe_expr(a) for a in expr.arguments]
        self._add_summary(f"Calling function '{callee_name}' with arguments {arg_vals}")
        s = self._pad("Call(")
        self.indent += 1
        s += expr.callee.accept(self)
        s += self._pad("Arguments:")
        for arg in expr.arguments:
            s += arg.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    # ----------------- Statement Visitors -----------------
    def visitExpressionStmt(self, stmt):
        self._add_summary(f"Expression statement: {self._describe_expr(stmt.expression)}")
        s = self._pad("ExpressionStmt(")
        self.indent += 1
        s += stmt.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitPrintStmt(self, stmt):
        self._add_summary(f"Print statement printing: {self._describe_expr(stmt.expression)}")
        s = self._pad("PrintStmt(")
        self.indent += 1
        s += stmt.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitVarStmt(self, stmt):
        init_val = self._describe_expr(stmt.initializer) if stmt.initializer else "None"
        self._add_summary(f"Declare variable '{stmt.name.lexeme}' with initial value {init_val}")
        s = self._pad(f"VarStmt({stmt.name.lexeme})")
        if stmt.initializer:
            self.indent += 1
            s += stmt.initializer.accept(self)
            self.indent -= 1
        return s

    def visitBlockStmt(self, stmt):
        self._add_summary("Block statement executing multiple statements sequentially.")
        s = self._pad("BlockStmt(")
        self.indent += 1
        for st in stmt.statements:
            s += st.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitIfStmt(self, stmt):
        self._add_summary(f"If statement with condition {self._describe_expr(stmt.condition)}")
        s = self._pad("IfStmt(")
        self.indent += 1

        s += self._pad("Condition:")
        self.indent += 1
        s += stmt.condition.accept(self)
        self.indent -= 1

        s += self._pad("Then:")
        self.indent += 1
        s += stmt.then_branch.accept(self)
        self.indent -= 1

        for idx, (elif_cond, elif_body) in enumerate(stmt.elif_branches):
            s += self._pad(f"Elif {idx+1} Condition:")
            self.indent += 1
            s += elif_cond.accept(self)
            self.indent -= 1

            s += self._pad(f"Elif {idx+1} Then:")
            self.indent += 1
            s += elif_body.accept(self)
            self.indent -= 1

        if stmt.else_branch:
            s += self._pad("Else:")
            self.indent += 1
            s += stmt.else_branch.accept(self)
            self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s

    def visitWhileStmt(self, stmt):
        self._add_summary(f"While loop with condition {self._describe_expr(stmt.condition)}")
        s = self._pad("WhileStmt(")
        self.indent += 1

        s += self._pad("Condition:")
        self.indent += 1
        s += stmt.condition.accept(self)
        self.indent -= 1

        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s

    def visitForStmt(self, stmt):
        self._add_summary(f"For loop iterating variable '{stmt.name.lexeme}' over iterable {self._describe_expr(stmt.iterable)}")
        s = self._pad("ForStmt(")
        self.indent += 1

        s += self._pad("Variable:")
        self.indent += 1
        s += self._pad(stmt.name.lexeme)
        self.indent -= 1

        s += self._pad("Iterable:")
        self.indent += 1
        s += stmt.iterable.accept(self)
        self.indent -= 1

        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s

    def visitBreakStmt(self, stmt):
        self._add_summary("Break statement to exit the nearest loop.")
        return self._pad("BreakStmt()")

    def visitContinueStmt(self, stmt):
        self._add_summary("Continue statement to skip to the next iteration of the nearest loop.")
        return self._pad("ContinueStmt()")

    def visitFunctionStmt(self, stmt):
        params = [p.lexeme for p in stmt.params]
        self._add_summary(f"Function '{stmt.name.lexeme}' defined with parameters {params}")
        s = self._pad("Function(")
        self.indent += 1

        s += self._pad("Name:")
        self.indent += 1
        s += self._pad(stmt.name.lexeme)
        self.indent -= 1

        s += self._pad("Params:")
        self.indent += 1
        for param in stmt.params:
            s += self._pad(param.lexeme)
        self.indent -= 1

        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s

    def visitReturnStmt(self, stmt):
        val_desc = self._describe_expr(stmt.value) if stmt.value else "None"
        self._add_summary(f"Return statement returning {val_desc}")
        s = self._pad("ReturnStmt(")
        self.indent += 1

        s += self._pad("Value:")
        self.indent += 1
        if stmt.value:
            s += stmt.value.accept(self)
        else:
            s += self._pad("None")
        self.indent -= 1

        self.indent -= 1
        s += self._pad(")")
        return s




    # ----------------- Stmt Visitors -----------------
    def visitPrintStmt(self, stmt):
        expr_val = getattr(stmt.expression, "value", "<expr>")
        self._add_summary(f"Print statement printing the value of expression ({expr_val}).")
        s = self._pad("PrintStmt(")
        self.indent += 1
        s += stmt.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitExpressionStmt(self, stmt):
        # self._add_summary(f"Expression statement evaluating: {getattr(stmt.expression, 'value', '<expr>')}")
        s = self._pad("ExpressionStmt(")
        self.indent += 1
        s += stmt.expression.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitVarStmt(self, stmt):
        init_val = getattr(stmt.initializer, "value", "<expr>") if stmt.initializer else None
        self._add_summary(f"Declare variable '{stmt.name.lexeme}' with initial value {init_val}.")
        s = self._pad(f"VarStmt({stmt.name.lexeme})")
        if stmt.initializer:
            self.indent += 1
            s += stmt.initializer.accept(self)
            self.indent -= 1
        return s

    def visitBlockStmt(self, stmt):
        self._add_summary("Block statement executing multiple statements sequentially.")
        s = self._pad("BlockStmt(")
        self.indent += 1
        for st in stmt.statements:
            s += st.accept(self)
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitIfStmt(self, stmt):
        cond_val = getattr(stmt.condition, "value", "<expr>")
        self._add_summary(
            f"If statement: evaluates condition ({cond_val}). Executes 'then' branch if true; "
            "otherwise checks 'elif' branches or executes 'else' branch if present."
        )
        s = self._pad("IfStmt(")
        self.indent += 1
        s += self._pad("Condition:")
        self.indent += 1
        s += stmt.condition.accept(self)
        self.indent -= 1
        s += self._pad("Then:")
        self.indent += 1
        s += stmt.then_branch.accept(self)
        self.indent -= 1
        for idx, (elif_cond, elif_body) in enumerate(stmt.elif_branches):
            cond_val = getattr(elif_cond, "value", "<expr>")
            self._add_summary(f"Elif branch {idx+1}: condition ({cond_val}). Executes if true.")
            s += self._pad(f"Elif {idx+1} Condition:")
            self.indent += 1
            s += elif_cond.accept(self)
            self.indent -= 1
            s += self._pad(f"Elif {idx+1} Then:")
            self.indent += 1
            s += elif_body.accept(self)
            self.indent -= 1
        if stmt.else_branch:
            self._add_summary("Else branch executes if all previous conditions are false.")
            s += self._pad("Else:")
            self.indent += 1
            s += stmt.else_branch.accept(self)
            self.indent -= 1
        self.indent -= 1
        s += self._pad(")")
        return s


    def visitWhileStmt(self, stmt):
        cond_val = getattr(stmt.condition, "value", "<expr>")
        self._add_summary(
            f"While loop: repeatedly executes its body while the condition ({cond_val}) is true."
        )
        s = self._pad("WhileStmt(")
        self.indent += 1
        s += self._pad("Condition:")
        self.indent += 1
        s += stmt.condition.accept(self)
        self.indent -= 1
        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1
        self.indent -= 1
        s += self._pad(")")
        return s


    def visitForStmt(self, stmt):
        iter_val = getattr(stmt.iterable, "value", "<expr>")
        self._add_summary(
            f"For loop: iterates variable '{stmt.name.lexeme}' over iterable ({iter_val}), "
            "executing the loop body for each element."
        )
        s = self._pad("ForStmt(")
        self.indent += 1
        s += self._pad("Variable:")
        self.indent += 1
        s += self._pad(stmt.name.lexeme)
        self.indent -= 1
        s += self._pad("Iterable:")
        self.indent += 1
        s += stmt.iterable.accept(self)
        self.indent -= 1
        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1
        self.indent -= 1
        s += self._pad(")")
        return s


    def visitBreakStmt(self, stmt):
        self._add_summary("Break statement to exit the nearest loop.")
        return self._pad("BreakStmt()")

    def visitContinueStmt(self, stmt):
        self._add_summary("Continue statement to skip to the next iteration of the nearest loop.")
        return self._pad("ContinueStmt()")

    def visitFunctionStmt(self, stmt):
        params = [p.lexeme for p in stmt.params]
        self._add_summary(f"Function '{stmt.name.lexeme}' defined with parameters {params}.")
        s = self._pad("Function(")
        self.indent += 1
        s += self._pad("Name:")
        self.indent += 1
        s += self._pad(stmt.name.lexeme)
        self.indent -= 1
        s += self._pad("Params:")
        self.indent += 1
        for param in stmt.params:
            s += self._pad(param.lexeme)
        self.indent -= 1
        s += self._pad("Body:")
        self.indent += 1
        s += stmt.body.accept(self)
        self.indent -= 1
        self.indent -= 1
        s += self._pad(")")
        return s

    def visitReturnStmt(self, stmt):
        val = getattr(stmt.value, "value", "<expr>") if stmt.value else "None"
        self._add_summary(f"Return statement returning value {val}.")
        s = self._pad("ReturnStmt(")
        self.indent += 1
        s += self._pad("Value:")
        self.indent += 1
        if stmt.value:
            s += stmt.value.accept(self)
        else:
            s += self._pad("None")
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
            if self.match(TokenType.DEF):
                return self.function("function")
            return self.statement()
        except ParseError as e:
            print(f"[Parser Error] {e}")
            self.synchronize()
            return None


    # ----------------- Statements -----------------
    def statement(self):
        if self.match(TokenType.PRINT):
            stmt = self.print_statement()
        elif self.match(TokenType.IF):
            stmt = self.if_statement()
        elif self.match(TokenType.WHILE):
            stmt = self.while_statement()
        elif self.match(TokenType.FOR):
            stmt = self.for_statement()
        elif self.match(TokenType.BREAK):
            stmt =self.break_statement()
        elif self.match(TokenType.CONTINUE):
            stmt=self.continue_statement()
        elif self.match(TokenType.DEF):
            stmt = self.function("function")
        elif self.match(TokenType.RETURN):
            stmt=self.return_statement()
        elif self.match(TokenType.LBRACE):
            stmt = Stmt.Block(self.block())
        else:
            stmt = self.expression_statement()  

        return stmt


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

    def while_statement(self):
        condition = self.expression()
        self.consume(TokenType.COLON, "Expect ':' after while condition.")
        self.consume(TokenType.NEWLINE, "Expect newline after ':'.")

        body = Stmt.Block(self.block())
        return Stmt.While(condition, body)
    

    def for_statement(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect loop variable after 'for'.")
        self.consume(TokenType.IN, "Expect 'in' after loop variable.")

        if self.check(TokenType.RANGE):
            self.advance()
            iterable = self.parse_range_expr()
        elif self.check(TokenType.LEN):
            self.advance()
            iterable = self.parse_len_expr()
        else:
            iterable = self.expression()

        self.consume(TokenType.COLON, "Expect ':' after iterable in for loop.")
        body = self.suite()
        return Stmt.For(name, iterable, body)

    def break_statement(self):
        if self.match(TokenType.COLON):
            raise self.error(self.previous(), "Unexpected ':' after 'break'.")
        self.match(TokenType.NEWLINE) 
        return Stmt.Break()

    def continue_statement(self):
        if self.match(TokenType.COLON):
            raise self.error(self.previous(), "Unexpected ':' after 'continue'.")
        self.match(TokenType.NEWLINE) 
        return Stmt.Continue()


   
    def parse_range_expr(self):
        args = []
        if self.match(TokenType.LPAREN):
            if not self.check(TokenType.RPAREN):
                args.append(self.expression())
                while self.match(TokenType.COMMA):
                    args.append(self.expression())
            self.consume(TokenType.RPAREN, "Expect ')' after range arguments.")
        else:
            args.append(self.expression())
            while self.match(TokenType.COMMA):
                args.append(self.expression())
        if not (1 <= len(args) <= 3):
            raise self.error(self.previous(), "range() takes 1 to 3 arguments.")
        return Expr.Range(args)

    def parse_len_expr(self):
        if self.match(TokenType.LPAREN):
            target = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after len argument.")
        else:
            target = self.expression()
        return Expr.Len(target)



    def print_statement(self):
        
        if self.match(TokenType.LPAREN):
            value = self.expression()
            self.consume(TokenType.RPAREN, "Expect ')' after print value.")
        else:
            value = self.expression()
        self.match(TokenType.NEWLINE)
        return Stmt.Print(value)

    def expression_statement(self):
        expr = self.expression()
        stmt = Stmt.Expression(expr)
        if self.match(TokenType.NEWLINE):
            return stmt
        if self.check(TokenType.DEDENT):
            return stmt
        if self.is_at_end():
            self.advance()
            return stmt
        self.error(self.peek(), "Expect end of statement (newline or EOF).")


    def expression(self):
        return self.or_()

    def or_(self):
        expr = self.and_()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self.and_()
            expr = Expr.Logical(expr, operator, right) 

        return expr
    
    def and_(self):
        expr = self.assignment()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.assignment()
            expr = Expr.Logical(expr, operator, right)  
        return expr



    def assignment(self):
        expr = self.equality()
        if self.match(TokenType.ASSIGN):
            operator = self.previous()
            value = self.assignment()
            if isinstance(expr, Expr.Variable):
                return Expr.Assign(expr.name, value)
            elif isinstance(expr, Expr.Index):
                return Expr.IndexAssign(expr.collection, expr.index_expr, value)
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
        while self.match(TokenType.DIV, TokenType.MUL,TokenType.REM):
            operator = self.previous()
            right = self.unary()
            expr = Expr.Binary(expr, operator, right)
        return expr

    def unary(self):
        if self.match(TokenType.NOT, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Expr.Unary(operator, right)
        return self.call()
    
    def function(self, kind):
        name = self.consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
        self.consume(TokenType.LPAREN, "Expect '(' after function name.")
        parameters = []
        if not self.check(TokenType.RPAREN):
            while True:
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name."))
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RPAREN, "Expect ')' after parameters.")
        self.consume(TokenType.COLON, "Expect ':' before function body.")
        self.consume(TokenType.NEWLINE, "Expect newline after ':' in function definition.")
        body = self.block()
        return Stmt.Function(name, parameters, Stmt.Block(body)) 




    def call(self):
        expr = self.primary()

        while True:
            if self.match(TokenType.LPAREN):
                expr = self.finish_call(expr)
            else:
                break

        return expr

    def finish_call(self, callee):
        arguments = []
        if not self.check(TokenType.RPAREN):
            while True:
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break
        paren = self.consume(TokenType.RPAREN, "Expect ')' after arguments.")
        return Expr.Call(callee, paren, arguments)


    
    def return_statement(self):
        keyword = self.previous()  
        value = None

        if not self.check(TokenType.NEWLINE) and not self.check(TokenType.DEDENT) and not self.is_at_end():
            value = self.expression()

        
        self.match(TokenType.NEWLINE)

        return Stmt.Return(keyword, value)


    
    def list_literal(self):
        elements = []
        if not self.check(TokenType.RBRACKET):
            while True:
                elements.append(self.expression())
                if self.match(TokenType.COMMA):
                    if self.check(TokenType.RBRACKET):
                        break
                    continue
                else:
                    break
        self.consume(TokenType.RBRACKET, "Expect ']' after list elements.")
        return Expr.ListLiteral(elements)


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
            primary_expr = Expr.Grouping(expr)
        elif self.match(TokenType.LBRACKET):
            primary_expr = self.list_literal()
        elif self.match(TokenType.IDENTIFIER):
            primary_expr = Expr.Variable(self.previous())
        elif self.match(TokenType.RANGE):
            primary_expr=self.parse_range_expr()
            return primary_expr
        elif self.match(TokenType.LEN):
            primary_expr=self.parse_len_expr()
            return primary_expr
        
        else:
            raise ParseError(f"[line {self.peek().line}] Error at '{self.peek().lexeme}': Expect expression.")

        
        while True:
            if self.match(TokenType.LBRACKET):
                index_expr = self.expression()
                self.consume(TokenType.RBRACKET, "Expect ']' after index expression.")
                primary_expr = Expr.Index(primary_expr, index_expr)
                continue
            break

        return primary_expr

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
        self.consume(TokenType.INDENT, "Expect indent after ':'.")
        while not self.check(TokenType.DEDENT) and not self.is_at_end():
            statements.append(self.declaration())
        self.consume(TokenType.DEDENT, "Expect dedent after block.")
        return statements

