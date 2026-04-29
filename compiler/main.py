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
