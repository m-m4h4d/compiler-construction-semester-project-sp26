from ast_nodes import *

class Optimizer:
    def __init__(self, ast):
        self.ast = ast

    def optimize(self):
        return self.visit(self.ast)

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return node

    def visit_Program(self, node):
        node.declarations = [self.visit(decl) for decl in node.declarations]
        return node

    def visit_FunctionDecl(self, node):
        node.body = self.visit(node.body)
        return node

    def visit_VarDecl(self, node):
        if node.init_expr:
            node.init_expr = self.visit(node.init_expr)
        return node

    def visit_ArrayDecl(self, node):
        return node

    def visit_Block(self, node):
        optimized_statements = []
        for stmt in node.statements:
            opt_stmt = self.visit(stmt)
            if opt_stmt:
                optimized_statements.append(opt_stmt)
            # Dead code elimination: stop appending if we hit a return
            if isinstance(opt_stmt, ReturnStmt):
                break
        node.statements = optimized_statements
        return node

    def visit_IfStmt(self, node):
        node.condition = self.visit(node.condition)
        node.then_branch = self.visit(node.then_branch)
        if node.else_branch:
            node.else_branch = self.visit(node.else_branch)
            
        # Constant Folding + Dead Code Elimination
        if isinstance(node.condition, Number):
            if node.condition.value != 0:
                return node.then_branch
            else:
                return node.else_branch
        return node

    def visit_WhileStmt(self, node):
        node.condition = self.visit(node.condition)
        node.body = self.visit(node.body)
        
        # Dead code elimination if condition is const 0
        if isinstance(node.condition, Number) and node.condition.value == 0:
            return None
        return node

    def visit_ForStmt(self, node):
        node.init = self.visit(node.init)
        node.condition = self.visit(node.condition)
        node.increment = self.visit(node.increment)
        node.body = self.visit(node.body)
        
        # Dead code elimination
        if isinstance(node.condition, Number) and node.condition.value == 0:
            # Init is executed, then loop ends. In C, if init is declaration, we just keep init.
            # But to keep AST simple, we'll just return init if it's an assignment/decl
            return node.init 
        return node

    def visit_ReturnStmt(self, node):
        if node.expr:
            node.expr = self.visit(node.expr)
        return node

    def visit_AssignStmt(self, node):
        node.expr = self.visit(node.expr)
        return node

    def visit_ArrayAssignStmt(self, node):
        node.index_expr = self.visit(node.index_expr)
        node.expr = self.visit(node.expr)
        return node

    def visit_BinOp(self, node):
        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        
        # Constant Folding
        if isinstance(node.left, Number) and isinstance(node.right, Number):
            lval = node.left.value
            rval = node.right.value
            op = node.op
            val_type = 'float' if node.left.val_type == 'float' or node.right.val_type == 'float' else 'int'
            
            try:
                if op == '+': result = lval + rval
                elif op == '-': result = lval - rval
                elif op == '*': result = lval * rval
                elif op == '/': result = lval / rval if val_type == 'float' else lval // rval
                elif op == '%': result = lval % rval
                elif op == '==': result = 1 if lval == rval else 0
                elif op == '!=': result = 1 if lval != rval else 0
                elif op == '<': result = 1 if lval < rval else 0
                elif op == '<=': result = 1 if lval <= rval else 0
                elif op == '>': result = 1 if lval > rval else 0
                elif op == '>=': result = 1 if lval >= rval else 0
                elif op == '&&': result = 1 if lval and rval else 0
                elif op == '||': result = 1 if lval or rval else 0
                else: return node
                
                return Number(result, val_type)
            except ZeroDivisionError:
                pass # don't fold division by zero
        return node

    def visit_UnaryOp(self, node):
        node.expr = self.visit(node.expr)
        
        # Constant Folding
        if isinstance(node.expr, Number):
            if node.op == '-':
                return Number(-node.expr.value, node.expr.val_type)
            elif node.op == '!':
                return Number(1 if not node.expr.value else 0, 'int')
        return node

    def visit_Var(self, node):
        return node

    def visit_ArrayAccess(self, node):
        node.index_expr = self.visit(node.index_expr)
        return node

    def visit_Number(self, node):
        return node

    def visit_FuncCall(self, node):
        node.args = [self.visit(arg) for arg in node.args]
        return node
