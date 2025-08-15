INTEGER, REAL_CONST, STRING, IDENTIFIER, MUL, DIV, EOF, ADD, SUB, RPAREN, LPAREN, ASSIGN = (
    'INTEGER', 'REAL_CONST', 'STRING', 'IDENTIFIER', 'MUL', 'DIV', 'EOF', 'ADD', 'SUB', 'RPAREN', 'LPAREN', 'ASSIGN'
)

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'

    def __repr__(self):
        return self.__str__()
    

class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def error(self):
        raise Exception(f'Invalid character: {self.current_char}')

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        if '.' in result:
            return Token(REAL_CONST, float(result))
        else:
            return Token(INTEGER, int(result))

    def string(self):
        self.advance()  
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char != '"':
            self.error()
        self.advance()  
        return Token(STRING, result)

    def identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return Token(IDENTIFIER, result)

    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return self.number()

            if self.current_char == '"':
                return self.string()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '+':
                self.advance()
                return Token(ADD, '+')

            if self.current_char == '-':
                self.advance()
                return Token(SUB, '-')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)

class RuntimeError_(Exception):
    pass

class Interpreter(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.variables = {}

    def error(self, message='Invalid syntax'):
        raise Exception(message)

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f'Expected token {token_type}, got {self.current_token.type}')

    def ensure_number(self, value):
        if not isinstance(value, (int, float)):
            raise RuntimeError_(f"Operand must be a number, got {type(value).__name__}")
        return value

    def factor(self):
        token = self.current_token

        if token.type == ADD:
            self.eat(ADD)
            return +self.ensure_number(self.factor())

        if token.type == SUB:
            self.eat(SUB)
            return -self.ensure_number(self.factor())

        if token.type == INTEGER:
            value = token.value
            self.eat(INTEGER)
            return value

        if token.type == REAL_CONST:
            value = token.value
            self.eat(REAL_CONST)
            return value

        if token.type == STRING:
            value = token.value
            self.eat(STRING)
            return value

        if token.type == IDENTIFIER:
            var_name = token.value
            self.eat(IDENTIFIER)
            if var_name in self.variables:
                return self.variables[var_name]
            else:
                raise RuntimeError_(f"Variable '{var_name}' not defined")

        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result

        self.error()

    def term(self):
        result = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
                result = self.ensure_number(result) * self.ensure_number(self.factor())
            elif token.type == DIV:
                self.eat(DIV)
                divisor = self.ensure_number(self.factor())
                if divisor == 0:
                    raise RuntimeError_("Division by zero")
                result = self.ensure_number(result) / divisor
        return result

    def expr(self):
        result = self.term()

        while self.current_token.type in (ADD, SUB):
            token = self.current_token
            if token.type == ADD:
                self.eat(ADD)
                result = self.ensure_number(result) + self.ensure_number(self.term())
            elif token.type == SUB:
                self.eat(SUB)
                result = self.ensure_number(result) - self.ensure_number(self.term())
        return result

    def assignment(self):
        var_name = self.current_token.value
        self.eat(IDENTIFIER)
        self.eat(ASSIGN)
        value = self.expr()
        self.variables[var_name] = value
        return value

    def parse(self):
        if self.current_token.type == IDENTIFIER:
            lookahead = self.current_token
            pos_save = self.lexer.pos
            char_save = self.lexer.current_char
            next_token = self.lexer.get_next_token()
            self.lexer.pos = pos_save
            self.lexer.current_char = char_save

            if next_token.type == ASSIGN:
                return self.assignment()

        return self.expr()

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        try:
            lexer = Lexer(text)
            interpreter = Interpreter(lexer)
            result = interpreter.parse()
            print(result)
        except RuntimeError_ as e:
            print(f"Runtime error: {e}")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
