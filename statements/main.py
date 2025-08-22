import sys
from scanner import Scanner
from parser import Parser, ASTTreePrinter
from interpreter import CODESAGE, Interpreter

def main():
    print("Enter Python-like code below. Press Enter twice to finish:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)

    source_code = "\n".join(lines)

    # -----------------------------
    # 1. Scan tokens
    # -----------------------------
    scanner = Scanner(source_code)
    try:
        tokens = scanner.scan_tokens()
    except Exception as e:
        print(f"[Scanner Error] {e}", file=sys.stderr)
        sys.exit(65)

    print("\n[Scanner Output]:")
    for token in tokens:
        print(token)

    # -----------------------------
    # 2. Parse tokens to AST
    # -----------------------------
    parser = Parser(tokens)
    try:
        statements = parser.parse()  # returns a list of statements
    except Exception as e:
        print(f"[Parser Error] {e}", file=sys.stderr)
        sys.exit(65)

    print("\n[Parser Output]:")
    printer = ASTTreePrinter()
    for stmt in statements:
        if stmt:
            print(printer.print(stmt))  # Print AST for each statement

    # -----------------------------
    # 3. Interpret AST
    # -----------------------------
    interpreter = Interpreter()
    CODESAGE.interpreter = interpreter
    try:
        # Filter out None statements (from errors) and run interpreter
        statements = [stmt for stmt in statements if stmt is not None]
        CODESAGE.interpret(statements)
    except Exception as e:
        print(f"[Runtime Error] {e}", file=sys.stderr)
        sys.exit(70)

if __name__ == "__main__":
    main()
