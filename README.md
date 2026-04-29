# Compiler Construction Project Report Spring 2026

## 1. Introduction

This document presents the design and implementation of a modular compiler for a subset of the C programming language. The compiler is implemented entirely in Python and features Lexical Analysis, Syntax Analysis (Recursive Descent Parsing), Semantic Analysis (Symbol Table for scope checking), Code Optimization (Constant Folding and Dead Code Elimination), Intermediate Representation (TAC) generation, and finally LLVM IR Backend generation.

## 2. Subset Definition & Grammar

### Features Supported

- **Data Types**: `int`, `float`, `double`
- **Expressions**: Arithmetic (`+`, `-`, `*`, `/`, `%`), Relational (`==`, `!=`, `<`, `>`, `<=`, `>=`), Logical (`&&`, `||`, `!`)
- **Control Flow**: `if-else`, `while`, `for` loops
- **Functions**: Parameter passing and return statements
- **Innovation Features**: 1D Arrays, Constant Folding, Dead Code Elimination

### Context-Free Grammar (Subset)

```cpp
Program -> Decl*
Decl -> Type ID ( '(' Params ')' Block | '[' NUMBER ']' ';' | [ '=' Expr ] ';' )
Block -> '{' Stmt* '}'
Stmt -> IfStmt | WhileStmt | ForStmt | ReturnStmt | ExprStmt | Block
IfStmt -> 'if' '(' Expr ')' Stmt [ 'else' Stmt ]
WhileStmt -> 'while' '(' Expr ')' Stmt
ForStmt -> 'for' '(' ExprStmt Expr ';' Expr ')' Stmt
ExprStmt -> [ ID '=' Expr | ID '[' Expr ']' '=' Expr ] ';' | Expr ';'
Expr -> LogicalOr
```

## 3. Design of Compiler Phases

1. **Lexical Analyzer (`lexer.py`)**: Tokenizes the input code using regular expressions to match keywords, numbers, identifiers, and symbols.
2. **Syntax Analyzer (`parser.py`)**: Uses Recursive Descent Parsing to build an Abstract Syntax Tree (AST). It incorporates assignments directly into expressions to support standard C `for` loops.
3. **Semantic Analyzer (`semantic.py`)**: Traverses the AST with a stack-based Symbol Table to enforce variable scoping, duplicate declarations, and array access checks.
4. **Optimizer (`optimizer.py`)**: Performs Constant Folding on arithmetic expressions and eliminates dead code (e.g. `if(0)` blocks or `while(0)`).
5. **TAC Generator (`tac.py`)**: A post-order AST traversal to generate flat Three-Address Code with explicit labels and temporaries.
6. **LLVM Backend (`codegen.py`)**: Traverses the AST to generate standard LLVM Intermediate Representation (`.ll`). It handles memory allocation (`alloca`), loads, and stores to properly reflect local scoping.

## 4. Limitations

- Single-dimensional arrays only.
- Pointers and structs are not supported.
- Missing short-circuiting in logical operators at the LLVM level (currently evaluates both sides).
- Only simple typing (implicit promotion between int and float is limited).

## 5. Compilation Instructions

The compiler is designed to run in a standard Python 3 environment without external dependencies.

1. Place all source files (`lexer.py`, `parser.py`, `ast_nodes.py`, `semantic.py`, `optimizer.py`, `tac.py`, `codegen.py`, `main.py`) in a directory.
2. Run the compiler on a C source file:

   ```bash
   python main.py input.c
   ```

3. The compiler will produce `output.tac` (Three-Address Code) and `output.ll` (LLVM IR).
4. To compile the LLVM IR to a native executable, use clang:

   ```bash
   clang output.ll -o output.exe
   ./output.exe
   ```

## 6. Test Cases & Output

### Test Case: Simple Arithmetic and Constant Folding (`test1_arithmetic.c`)

**Source Code:**

```c
{code}
```

**Generated TAC:**

```c
{chr(10).join(tac)}
```

**Generated LLVM IR:**

```llvm
{llvm}
```

---

### Test Case: Loops and Dead Code Elimination (`test2_loops.c`)

**Source Code:**

```c
{code}
```

**Generated TAC:**

```c
{chr(10).join(tac)}
```

**Generated LLVM IR:**

```llvm
{llvm}
```

---

### Test Case: Function Calls and Arrays (`test3_functions_arrays.c`)

**Source Code:**

```c
{code}
```

**Generated TAC:**

```c
{chr(10).join(tac)}
```

**Generated LLVM IR:**

```llvm
{llvm}
```

---

## 7. Complete Executable Code

### `ast_nodes.py`

```python
class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, declarations):
        self.declarations = declarations

class FunctionDecl(ASTNode):
    def __init__(self, return_type, name, params, body):
        self.return_type = return_type
        self.name = name
        self.params = params  # list of (type, name)
        self.body = body

class VarDecl(ASTNode):
    def __init__(self, var_type, name, init_expr=None):
        self.var_type = var_type
        self.name = name
        self.init_expr = init_expr

class ArrayDecl(ASTNode):
    def __init__(self, var_type, name, size):
        self.var_type = var_type
        self.name = name
        self.size = size

class Block(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class IfStmt(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

class WhileStmt(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForStmt(ASTNode):
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

class ReturnStmt(ASTNode):
    def __init__(self, expr=None):
        self.expr = expr

class AssignStmt(ASTNode):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class ArrayAssignStmt(ASTNode):
    def __init__(self, name, index_expr, expr):
        self.name = name
        self.index_expr = index_expr
        self.expr = expr

class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

class Var(ASTNode):
    def __init__(self, name):
        self.name = name

class ArrayAccess(ASTNode):
    def __init__(self, name, index_expr):
        self.name = name
        self.index_expr = index_expr

class Number(ASTNode):
    def __init__(self, value, val_type):
        self.value = value
        self.val_type = val_type # 'int' or 'float'

class FuncCall(ASTNode):
    def __init__(self, name, args):
        self.name = name
        self.args = args

```

### `lexer.py`

```python
import re

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line})"

class LexerError(Exception):
    pass

class Lexer:
    keywords = {
        'int': 'INT',
        'float': 'FLOAT',
        'double': 'DOUBLE',
        'if': 'IF',
        'else': 'ELSE',
        'while': 'WHILE',
        'for': 'FOR',
        'return': 'RETURN'
    }

    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),      # Integer or decimal number
        ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'), # Identifiers
        ('EQ',       r'=='),
        ('NEQ',      r'!='),
        ('LE',       r'<='),
        ('GE',       r'>='),
        ('AND',      r'&&'),
        ('OR',       r'\|\|'),
        ('ASSIGN',   r'='),
        ('LT',       r'<'),
        ('GT',       r'>'),
        ('NOT',      r'!'),
        ('PLUS',     r'\+'),
        ('MINUS',    r'-'),
        ('MUL',      r'\*'),
        ('DIV',      r'/'),
        ('MOD',      r'%'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('LBRACE',   r'\{'),
        ('RBRACE',   r'\}'),
        ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'),
        ('SEMI',     r';'),
        ('COMMA',    r','),
        ('SKIP',     r'[ \t]+'),           # Skip over spaces and tabs
        ('NEWLINE',  r'\n'),               # Line endings
        ('MISMATCH', r'.'),                # Any other character
    ]

    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.tokenize()

    def tokenize(self):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)
        line_num = 1
        line_start = 0
        
        for mo in re.finditer(tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            
            if kind == 'NUMBER':
                # Check if float or int
                if '.' in value:
                    value = float(value)
                else:
                    value = int(value)
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'ID':
                kind = self.keywords.get(value, 'ID')
                self.tokens.append(Token(kind, value, line_num, column))
            elif kind == 'NEWLINE':
                line_start = mo.end()
                line_num += 1
            elif kind == 'SKIP':
                pass
            elif kind == 'MISMATCH':
                raise LexerError(f'{value!r} unexpected on line {line_num}')
            else:
                self.tokens.append(Token(kind, value, line_num, column))
        self.tokens.append(Token('EOF', '', line_num, len(self.code) - line_start))

```

### `parser.py`

```python
from lexer import Lexer
from ast_nodes import *

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.pos = -1
        self.advance()

    def advance(self):
        self.pos += 1
        if self.pos < len(self.lexer.tokens):
            self.current_token = self.lexer.tokens[self.pos]
        return self.current_token

    def match(self, token_type):
        if self.current_token.type == token_type:
            tok = self.current_token
            self.advance()
            return tok
        else:
            raise ParseError(f"Expected {token_type}, found {self.current_token.type} at line {self.current_token.line}")

    def parse(self):
        declarations = []
        while self.current_token.type != 'EOF':
            declarations.append(self.parse_declaration())
        return Program(declarations)

    def parse_declaration(self):
        # type ID ...
        if self.current_token.type in ('INT', 'FLOAT', 'DOUBLE'):
            var_type = self.current_token.value
            self.advance()
            name = self.match('ID').value
            
            # could be function, array or var
            if self.current_token.type == 'LPAREN':
                return self.parse_function_decl(var_type, name)
            elif self.current_token.type == 'LBRACKET':
                return self.parse_array_decl(var_type, name)
            else:
                return self.parse_var_decl(var_type, name)
        else:
            raise ParseError(f"Expected type specifier at line {self.current_token.line}")

    def parse_function_decl(self, return_type, name):
        self.match('LPAREN')
        params = []
        if self.current_token.type != 'RPAREN':
            params.append(self.parse_param())
            while self.current_token.type == 'COMMA':
                self.match('COMMA')
                params.append(self.parse_param())
        self.match('RPAREN')
        body = self.parse_block()
        return FunctionDecl(return_type, name, params, body)

    def parse_param(self):
        if self.current_token.type in ('INT', 'FLOAT', 'DOUBLE'):
            p_type = self.current_token.value
            self.advance()
            name = self.match('ID').value
            return (p_type, name)
        raise ParseError("Expected type in parameter list")

    def parse_array_decl(self, var_type, name):
        self.match('LBRACKET')
        size = self.match('NUMBER').value
        self.match('RBRACKET')
        self.match('SEMI')
        return ArrayDecl(var_type, name, size)

    def parse_var_decl(self, var_type, name):
        init_expr = None
        if self.current_token.type == 'ASSIGN':
            self.match('ASSIGN')
            init_expr = self.parse_expression()
        self.match('SEMI')
        return VarDecl(var_type, name, init_expr)

    def parse_block(self):
        self.match('LBRACE')
        statements = []
        while self.current_token.type != 'RBRACE' and self.current_token.type != 'EOF':
            if self.current_token.type in ('INT', 'FLOAT', 'DOUBLE'):
                # variable declaration inside block
                var_type = self.current_token.value
                self.advance()
                name = self.match('ID').value
                if self.current_token.type == 'LBRACKET':
                    statements.append(self.parse_array_decl(var_type, name))
                else:
                    statements.append(self.parse_var_decl(var_type, name))
            else:
                statements.append(self.parse_statement())
        self.match('RBRACE')
        return Block(statements)

    def parse_statement(self):
        if self.current_token.type == 'IF':
            return self.parse_if()
        elif self.current_token.type == 'WHILE':
            return self.parse_while()
        elif self.current_token.type == 'FOR':
            return self.parse_for()
        elif self.current_token.type == 'RETURN':
            return self.parse_return()
        elif self.current_token.type == 'LBRACE':
            return self.parse_block()
        else:
            return self.parse_expr_statement()

    def parse_if(self):
        self.match('IF')
        self.match('LPAREN')
        cond = self.parse_expression()
        self.match('RPAREN')
        then_b = self.parse_statement()
        else_b = None
        if self.current_token.type == 'ELSE':
            self.match('ELSE')
            else_b = self.parse_statement()
        return IfStmt(cond, then_b, else_b)

    def parse_while(self):
        self.match('WHILE')
        self.match('LPAREN')
        cond = self.parse_expression()
        self.match('RPAREN')
        body = self.parse_statement()
        return WhileStmt(cond, body)

    def parse_for(self):
        self.match('FOR')
        self.match('LPAREN')
        init = self.parse_expr_statement() # Includes SEMI
        cond = self.parse_expression()
        self.match('SEMI')
        inc = self.parse_assignment_expr()
        self.match('RPAREN')
        body = self.parse_statement()
        return ForStmt(init, cond, inc, body)

    def parse_return(self):
        self.match('RETURN')
        expr = None
        if self.current_token.type != 'SEMI':
            expr = self.parse_expression()
        self.match('SEMI')
        return ReturnStmt(expr)

    def parse_expr_statement(self):
        expr = self.parse_assignment_expr()
        self.match('SEMI')
        return expr

    def parse_assignment_expr(self):
        if self.current_token.type == 'ID':
            # Could be assignment, array assignment, or function call
            next_tok = self.lexer.tokens[self.pos + 1]
            if next_tok.type == 'ASSIGN':
                name = self.match('ID').value
                self.match('ASSIGN')
                expr = self.parse_assignment_expr()
                return AssignStmt(name, expr)
            elif next_tok.type == 'LBRACKET':
                # Quick check if it's an assignment to array
                # Find matching bracket
                temp_pos = self.pos + 2
                brackets = 1
                while temp_pos < len(self.lexer.tokens) and brackets > 0:
                    if self.lexer.tokens[temp_pos].type == 'LBRACKET': brackets += 1
                    elif self.lexer.tokens[temp_pos].type == 'RBRACKET': brackets -= 1
                    temp_pos += 1
                if temp_pos < len(self.lexer.tokens) and self.lexer.tokens[temp_pos].type == 'ASSIGN':
                    name = self.match('ID').value
                    self.match('LBRACKET')
                    idx = self.parse_expression()
                    self.match('RBRACKET')
                    self.match('ASSIGN')
                    expr = self.parse_assignment_expr()
                    return ArrayAssignStmt(name, idx, expr)
        return self.parse_expression()

    def parse_expression(self):
        return self.parse_logical_or()

    def parse_logical_or(self):
        node = self.parse_logical_and()
        while self.current_token.type == 'OR':
            op = self.match('OR').value
            right = self.parse_logical_and()
            node = BinOp(node, op, right)
        return node

    def parse_logical_and(self):
        node = self.parse_equality()
        while self.current_token.type == 'AND':
            op = self.match('AND').value
            right = self.parse_equality()
            node = BinOp(node, op, right)
        return node

    def parse_equality(self):
        node = self.parse_relational()
        while self.current_token.type in ('EQ', 'NEQ'):
            op = self.current_token.value
            self.advance()
            right = self.parse_relational()
            node = BinOp(node, op, right)
        return node

    def parse_relational(self):
        node = self.parse_additive()
        while self.current_token.type in ('LT', 'GT', 'LE', 'GE'):
            op = self.current_token.value
            self.advance()
            right = self.parse_additive()
            node = BinOp(node, op, right)
        return node

    def parse_additive(self):
        node = self.parse_multiplicative()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative()
            node = BinOp(node, op, right)
        return node

    def parse_multiplicative(self):
        node = self.parse_unary()
        while self.current_token.type in ('MUL', 'DIV', 'MOD'):
            op = self.current_token.value
            self.advance()
            right = self.parse_unary()
            node = BinOp(node, op, right)
        return node

    def parse_unary(self):
        if self.current_token.type in ('MINUS', 'NOT'):
            op = self.current_token.value
            self.advance()
            expr = self.parse_unary()
            return UnaryOp(op, expr)
        return self.parse_primary()

    def parse_primary(self):
        tok = self.current_token
        if tok.type == 'NUMBER':
            self.advance()
            val_type = 'float' if isinstance(tok.value, float) else 'int'
            return Number(tok.value, val_type)
        elif tok.type == 'ID':
            self.advance()
            if self.current_token.type == 'LPAREN':
                # Function call
                self.match('LPAREN')
                args = []
                if self.current_token.type != 'RPAREN':
                    args.append(self.parse_expression())
                    while self.current_token.type == 'COMMA':
                        self.match('COMMA')
                        args.append(self.parse_expression())
                self.match('RPAREN')
                return FuncCall(tok.value, args)
            elif self.current_token.type == 'LBRACKET':
                # Array access
                self.match('LBRACKET')
                idx = self.parse_expression()
                self.match('RBRACKET')
                return ArrayAccess(tok.value, idx)
            else:
                return Var(tok.value)
        elif tok.type == 'LPAREN':
            self.match('LPAREN')
            expr = self.parse_expression()
            self.match('RPAREN')
            return expr
        else:
            raise ParseError(f"Unexpected token {tok.type} at line {tok.line}")

```

### `semantic.py`

```python
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

```

### `optimizer.py`

```python
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

```

### `tac.py`

```python
from ast_nodes import *

class TACGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.code.append(instruction)

    def generate(self):
        self.visit(self.ast)
        return self.code

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return None

    def visit_Program(self, node):
        for decl in node.declarations:
            self.visit(decl)

    def visit_FunctionDecl(self, node):
        self.emit(f"func {node.name}:")
        self.emit(f"begin_func")
        self.visit(node.body)
        self.emit(f"end_func")
        self.emit("") # blank line for readability

    def visit_VarDecl(self, node):
        if node.init_expr:
            val = self.visit(node.init_expr)
            self.emit(f"{node.name} = {val}")

    def visit_ArrayDecl(self, node):
        self.emit(f"alloc_array {node.name}, {node.size}")

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_IfStmt(self, node):
        cond_val = self.visit(node.condition)
        label_else = self.new_label()
        label_end = self.new_label()
        
        self.emit(f"if_false {cond_val} goto {label_else}")
        self.visit(node.then_branch)
        self.emit(f"goto {label_end}")
        self.emit(f"{label_else}:")
        if node.else_branch:
            self.visit(node.else_branch)
        self.emit(f"{label_end}:")

    def visit_WhileStmt(self, node):
        label_start = self.new_label()
        label_end = self.new_label()
        
        self.emit(f"{label_start}:")
        cond_val = self.visit(node.condition)
        self.emit(f"if_false {cond_val} goto {label_end}")
        self.visit(node.body)
        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    def visit_ForStmt(self, node):
        self.visit(node.init)
        label_start = self.new_label()
        label_end = self.new_label()
        
        self.emit(f"{label_start}:")
        cond_val = self.visit(node.condition)
        self.emit(f"if_false {cond_val} goto {label_end}")
        self.visit(node.body)
        self.visit(node.increment)
        self.emit(f"goto {label_start}")
        self.emit(f"{label_end}:")

    def visit_ReturnStmt(self, node):
        if node.expr:
            val = self.visit(node.expr)
            self.emit(f"return {val}")
        else:
            self.emit(f"return")

    def visit_AssignStmt(self, node):
        val = self.visit(node.expr)
        self.emit(f"{node.name} = {val}")
        return node.name

    def visit_ArrayAssignStmt(self, node):
        idx_val = self.visit(node.index_expr)
        val = self.visit(node.expr)
        self.emit(f"{node.name}[{idx_val}] = {val}")

    def visit_BinOp(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        temp = self.new_temp()
        self.emit(f"{temp} = {left_val} {node.op} {right_val}")
        return temp

    def visit_UnaryOp(self, node):
        val = self.visit(node.expr)
        temp = self.new_temp()
        self.emit(f"{temp} = {node.op} {val}")
        return temp

    def visit_Var(self, node):
        return node.name

    def visit_ArrayAccess(self, node):
        idx_val = self.visit(node.index_expr)
        temp = self.new_temp()
        self.emit(f"{temp} = {node.name}[{idx_val}]")
        return temp

    def visit_Number(self, node):
        return str(node.value)

    def visit_FuncCall(self, node):
        args_vals = []
        for arg in node.args:
            args_vals.append(self.visit(arg))
        for arg_val in args_vals:
            self.emit(f"param {arg_val}")
        temp = self.new_temp()
        self.emit(f"{temp} = call {node.name}, {len(args_vals)}")
        return temp

```

### `codegen.py`

```python
from ast_nodes import *

class LLVMGenerator:
    def __init__(self, ast, symtab):
        self.ast = ast
        self.symtab = symtab
        self.code = []
        self.reg_count = 0
        self.label_count = 0
        self.local_vars = {} # maps var name to LLVM register or ptr

    def new_reg(self):
        self.reg_count += 1
        return f"%{self.reg_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.code.append(instruction)

    def map_type(self, c_type):
        if c_type == 'int': return 'i32'
        elif c_type == 'float': return 'float'
        elif c_type == 'double': return 'double'
        return 'i32' # default

    def generate(self):
        self.emit("; LLVM IR Generated by Custom Compiler")
        self.emit("declare i32 @printf(i8*, ...)")
        self.visit(self.ast)
        return "\n".join(self.code)

    def visit(self, node):
        if node is None:
            return None
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return None

    def visit_Program(self, node):
        for decl in node.declarations:
            self.visit(decl)

    def visit_FunctionDecl(self, node):
        ret_type = self.map_type(node.return_type)
        params = []
        for p_type, p_name in node.params:
            params.append(f"{self.map_type(p_type)} %{p_name}_arg")
        
        param_str = ", ".join(params)
        self.emit(f"define {ret_type} @{node.name}({param_str}) {{")
        self.emit("entry:")
        self.reg_count = 0
        self.local_vars = {}
        
        # Allocate local variables for parameters
        for p_type, p_name in node.params:
            llvm_type = self.map_type(p_type)
            ptr = self.new_reg()
            self.emit(f"  {ptr} = alloca {llvm_type}")
            self.emit(f"  store {llvm_type} %{p_name}_arg, {llvm_type}* {ptr}")
            self.local_vars[p_name] = {'ptr': ptr, 'type': llvm_type}
            
        self.visit(node.body)
        
        # Add default return if void/missing
        if ret_type == 'i32':
            self.emit("  ret i32 0")
        elif ret_type == 'float':
            self.emit("  ret float 0.0")
        elif ret_type == 'double':
            self.emit("  ret double 0.0")
        self.emit("}\n")

    def visit_Block(self, node):
        for stmt in node.statements:
            self.visit(stmt)

    def visit_VarDecl(self, node):
        llvm_type = self.map_type(node.var_type)
        ptr = self.new_reg()
        self.emit(f"  {ptr} = alloca {llvm_type}")
        self.local_vars[node.name] = {'ptr': ptr, 'type': llvm_type}
        
        if node.init_expr:
            val, val_type = self.visit(node.init_expr)
            self.emit(f"  store {llvm_type} {val}, {llvm_type}* {ptr}")

    def visit_ArrayDecl(self, node):
        llvm_type = self.map_type(node.var_type)
        ptr = self.new_reg()
        self.emit(f"  {ptr} = alloca {llvm_type}, i32 {node.size}")
        self.local_vars[node.name] = {'ptr': ptr, 'type': llvm_type, 'is_array': True, 'size': node.size}

    def visit_AssignStmt(self, node):
        val, val_type = self.visit(node.expr)
        var_info = self.local_vars[node.name]
        self.emit(f"  store {var_info['type']} {val}, {var_info['type']}* {var_info['ptr']}")

    def visit_ArrayAssignStmt(self, node):
        idx_val, _ = self.visit(node.index_expr)
        val, val_type = self.visit(node.expr)
        var_info = self.local_vars[node.name]
        
        ptr = self.new_reg()
        self.emit(f"  {ptr} = getelementptr {var_info['type']}, {var_info['type']}* {var_info['ptr']}, i32 {idx_val}")
        self.emit(f"  store {var_info['type']} {val}, {var_info['type']}* {ptr}")

    def visit_ReturnStmt(self, node):
        if node.expr:
            val, val_type = self.visit(node.expr)
            self.emit(f"  ret {val_type} {val}")
        else:
            self.emit("  ret void")

    def visit_IfStmt(self, node):
        cond_val, _ = self.visit(node.condition)
        # Convert condition to i1
        cond_i1 = self.new_reg()
        self.emit(f"  {cond_i1} = icmp ne i32 {cond_val}, 0")
        
        then_label = self.new_label()
        else_label = self.new_label()
        end_label = self.new_label()
        
        if node.else_branch:
            self.emit(f"  br i1 {cond_i1}, label %{then_label}, label %{else_label}")
        else:
            self.emit(f"  br i1 {cond_i1}, label %{then_label}, label %{end_label}")
            
        self.emit(f"{then_label}:")
        self.visit(node.then_branch)
        self.emit(f"  br label %{end_label}")
        
        if node.else_branch:
            self.emit(f"{else_label}:")
            self.visit(node.else_branch)
            self.emit(f"  br label %{end_label}")
            
        self.emit(f"{end_label}:")

    def visit_WhileStmt(self, node):
        cond_label = self.new_label()
        body_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"  br label %{cond_label}")
        self.emit(f"{cond_label}:")
        
        cond_val, _ = self.visit(node.condition)
        cond_i1 = self.new_reg()
        self.emit(f"  {cond_i1} = icmp ne i32 {cond_val}, 0")
        self.emit(f"  br i1 {cond_i1}, label %{body_label}, label %{end_label}")
        
        self.emit(f"{body_label}:")
        self.visit(node.body)
        self.emit(f"  br label %{cond_label}")
        
        self.emit(f"{end_label}:")

    def visit_ForStmt(self, node):
        self.visit(node.init)
        
        cond_label = self.new_label()
        body_label = self.new_label()
        end_label = self.new_label()
        
        self.emit(f"  br label %{cond_label}")
        self.emit(f"{cond_label}:")
        
        cond_val, _ = self.visit(node.condition)
        cond_i1 = self.new_reg()
        self.emit(f"  {cond_i1} = icmp ne i32 {cond_val}, 0")
        self.emit(f"  br i1 {cond_i1}, label %{body_label}, label %{end_label}")
        
        self.emit(f"{body_label}:")
        self.visit(node.body)
        self.visit(node.increment)
        self.emit(f"  br label %{cond_label}")
        
        self.emit(f"{end_label}:")

    def visit_BinOp(self, node):
        left_val, left_type = self.visit(node.left)
        right_val, right_type = self.visit(node.right)
        res = self.new_reg()
        
        if left_type == 'i32':
            if node.op == '+': self.emit(f"  {res} = add i32 {left_val}, {right_val}")
            elif node.op == '-': self.emit(f"  {res} = sub i32 {left_val}, {right_val}")
            elif node.op == '*': self.emit(f"  {res} = mul i32 {left_val}, {right_val}")
            elif node.op == '/': self.emit(f"  {res} = sdiv i32 {left_val}, {right_val}")
            elif node.op == '%': self.emit(f"  {res} = srem i32 {left_val}, {right_val}")
            elif node.op in ['==', '!=', '<', '<=', '>', '>=']:
                icmp_op = {'==': 'eq', '!=': 'ne', '<': 'slt', '<=': 'sle', '>': 'sgt', '>=': 'sge'}[node.op]
                i1_res = self.new_reg()
                self.emit(f"  {i1_res} = icmp {icmp_op} i32 {left_val}, {right_val}")
                self.emit(f"  {res} = zext i1 {i1_res} to i32")
        return res, left_type

    def visit_UnaryOp(self, node):
        val, val_type = self.visit(node.expr)
        res = self.new_reg()
        if val_type == 'i32':
            if node.op == '-':
                self.emit(f"  {res} = sub i32 0, {val}")
            elif node.op == '!':
                i1_res = self.new_reg()
                self.emit(f"  {i1_res} = icmp eq i32 {val}, 0")
                self.emit(f"  {res} = zext i1 {i1_res} to i32")
        return res, val_type

    def visit_Var(self, node):
        var_info = self.local_vars[node.name]
        res = self.new_reg()
        self.emit(f"  {res} = load {var_info['type']}, {var_info['type']}* {var_info['ptr']}")
        return res, var_info['type']

    def visit_ArrayAccess(self, node):
        idx_val, _ = self.visit(node.index_expr)
        var_info = self.local_vars[node.name]
        ptr = self.new_reg()
        self.emit(f"  {ptr} = getelementptr {var_info['type']}, {var_info['type']}* {var_info['ptr']}, i32 {idx_val}")
        res = self.new_reg()
        self.emit(f"  {res} = load {var_info['type']}, {var_info['type']}* {ptr}")
        return res, var_info['type']

    def visit_Number(self, node):
        if node.val_type == 'float':
            return f"{node.value:.6e}", 'float'
        return str(node.value), 'i32'

    def visit_FuncCall(self, node):
        args_vals = []
        args_types = []
        for arg in node.args:
            val, v_type = self.visit(arg)
            args_vals.append(val)
            args_types.append(v_type)
            
        arg_strs = [f"{t} {v}" for t, v in zip(args_types, args_vals)]
        arg_str = ", ".join(arg_strs)
        
        res = self.new_reg()
        self.emit(f"  {res} = call i32 @{node.name}({arg_str})") # assuming i32 return for simplicity
        return res, 'i32'

```

### `main.py`

```python
import sys
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from optimizer import Optimizer
from tac import TACGenerator
from codegen import LLVMGenerator

def compile_c_code(source_code, optimize=True):
    print("--- Lexical Analysis ---")
    lexer = Lexer(source_code)
    # for t in lexer.tokens:
    #     print(t)
        
    print("\n--- Syntax Analysis ---")
    parser = Parser(lexer)
    ast = parser.parse()
    print("AST generated successfully.")
    
    print("\n--- Semantic Analysis ---")
    semantic = SemanticAnalyzer(ast)
    semantic.analyze()
    print("Semantic analysis passed.")
    
    if optimize:
        print("\n--- Optimization (Constant Folding & DCE) ---")
        opt = Optimizer(ast)
        ast = opt.optimize()
        print("Optimization complete.")
        
    print("\n--- TAC Generation ---")
    tac_gen = TACGenerator(ast)
    tac_code = tac_gen.generate()
    # for line in tac_code:
    #     print(line)
        
    print("\n--- LLVM IR Generation ---")
    llvm_gen = LLVMGenerator(ast, semantic.symtab)
    llvm_code = llvm_gen.generate()
    
    return tac_code, llvm_code

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python main.py <source_file>")
        sys.exit(1)
        
    with open(sys.argv[1], 'r') as f:
        source_code = f.read()
        
    tac, llvm = compile_c_code(source_code)
    
    with open('output.tac', 'w') as f:
        f.write("\n".join(tac))
    print("\nTAC written to output.tac")
    
    with open('output.ll', 'w') as f:
        f.write(llvm)
    print("LLVM IR written to output.ll")

```
