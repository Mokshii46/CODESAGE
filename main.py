import sys
from scanner import Scanner
from parser import Parser, ASTTreePrinter
from interpreter import CODESAGE

def main():
    print("Enter Python-like code below. Press Enter twice to finish:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    source_code = "\n".join(lines)

   
    scanner = Scanner(source_code)
    try:
        tokens = scanner.scan_tokens()
    except Exception as e:
        print(f"[Scanner Error] {e}", file=sys.stderr)
        sys.exit(65)

    print("\n[Scanner Output]:")
    for token in tokens:
        print(token)

  
    parser = Parser(tokens)
    try:
        ast_list = parser.parse()  # returns a list of Expr objects
    except Exception as e:
        print(f"[Parser Error] {e}", file=sys.stderr)
        sys.exit(65)

    print("\n[Parser Output]:")
    printer = ASTTreePrinter()
    for expr in ast_list:
        print(printer.print(expr))


    if CODESAGE.interpreter is None:
        from interpreter import Interpreter
        CODESAGE.interpreter = Interpreter()

    for expr in ast_list:
        CODESAGE.interpret(expr)

    # Exit codes based on errors
    if CODESAGE.had_error:
        sys.exit(65)
    if CODESAGE.had_runtime_error:
        sys.exit(70)


if __name__ == "__main__":
    main()

