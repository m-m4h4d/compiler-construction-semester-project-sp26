from ast_nodes import *

class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.scopes = [{}] # Stack of dictionaries

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, var_type, is_array=False, size=None):
        current_scope = self.scopes[-1]
        if name in current_scope:
            raise SemanticError(f"Variable '{name}' already declared in current scope")
        current_scope[name] = {'type': var_type, 'is_array': is_array, 'size': size}

    def declare_function(self, name, return_type, params):
        global_scope = self.scopes[0]
        if name in global_scope:
            raise SemanticError(f"Function '{name}' already declared")
        global_scope[name] = {'type': 'function', 'return_type': return_type, 'params': params}

    def lookup(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symtab = SymbolTable()

    def analyze(self):
        self.visit(self.ast)

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    def visit_Program(self, node):
        for decl in node.declarations:
            self.visit(decl)

    def visit_FunctionDecl(self, node):
        self.symtab.declare_function(node.name, node.return_type, node.params)
        self.symtab.enter_scope()
        for p_type, p_name in node.params:
            self.symtab.declare(p_name, p_type)
        self.visit(node.body)
        self.symtab.exit_scope()

    def visit_VarDecl(self, node):
        self.symtab.declare(node.name, node.var_type)
        if node.init_expr:
            self.visit(node.init_expr)

    def visit_ArrayDecl(self, node):
        self.symtab.declare(node.name, node.var_type, is_array=True, size=node.size)

    def visit_Block(self, node):
        self.symtab.enter_scope()
        for stmt in node.statements:
            self.visit(stmt)
        self.symtab.exit_scope()

    def visit_IfStmt(self, node):
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_WhileStmt(self, node):
        self.visit(node.condition)
        self.visit(node.body)

    def visit_ForStmt(self, node):
        self.symtab.enter_scope()
        self.visit(node.init)
        self.visit(node.condition)
        self.visit(node.increment)
        self.visit(node.body)
        self.symtab.exit_scope()

    def visit_ReturnStmt(self, node):
        if node.expr:
            self.visit(node.expr)

    def visit_AssignStmt(self, node):
        var_info = self.symtab.lookup(node.name)
        if not var_info:
            raise SemanticError(f"Undeclared variable '{node.name}'")
        if var_info.get('is_array'):
            raise SemanticError(f"Cannot assign to array '{node.name}' directly")
        self.visit(node.expr)

    def visit_ArrayAssignStmt(self, node):
        var_info = self.symtab.lookup(node.name)
        if not var_info:
            raise SemanticError(f"Undeclared array '{node.name}'")
        if not var_info.get('is_array'):
            raise SemanticError(f"'{node.name}' is not an array")
        self.visit(node.index_expr)
        self.visit(node.expr)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Var(self, node):
        var_info = self.symtab.lookup(node.name)
        if not var_info:
            raise SemanticError(f"Undeclared variable '{node.name}'")
        if var_info.get('type') == 'function':
            raise SemanticError(f"'{node.name}' is a function, not a variable")

    def visit_ArrayAccess(self, node):
        var_info = self.symtab.lookup(node.name)
        if not var_info:
            raise SemanticError(f"Undeclared array '{node.name}'")
        if not var_info.get('is_array'):
            raise SemanticError(f"'{node.name}' is not an array")
        self.visit(node.index_expr)

    def visit_Number(self, node):
        pass

    def visit_FuncCall(self, node):
        func_info = self.symtab.lookup(node.name)
        if not func_info:
            raise SemanticError(f"Undeclared function '{node.name}'")
        if func_info.get('type') != 'function':
            raise SemanticError(f"'{node.name}' is not a function")
        if len(node.args) != len(func_info['params']):
            raise SemanticError(f"Function '{node.name}' expects {len(func_info['params'])} arguments, got {len(node.args)}")
        for arg in node.args:
            self.visit(arg)
