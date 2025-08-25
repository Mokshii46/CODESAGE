import re
from enum import Enum, auto

class ErrorCode(Enum):
    UNEXPECTED_TOKEN = 'Unexpected token'
    ID_NOT_FOUND     = 'Identifier not found'
    DUPLICATE_ID     = 'Duplicate id found'
    INVALID_OPERATOR = 'Invalid Operator found'

class Error(Exception):
    def __init__(self, error_code=None, token=None, message=None):
        self.error_code = error_code
        self.token = token
        self.message = f'{self.__class__.__name__}: {message}'

class TokenType(Enum):
   
    DEF = auto(); IF = auto(); ELSE = auto(); ELIF = auto(); WHILE = auto()
    FOR = auto(); IN = auto(); RETURN = auto(); TRUE = auto(); FALSE = auto(); NONE = auto(); PASS = auto(); CLASS=auto();PRINT=auto()


    IDENTIFIER = auto(); NUMBER = auto(); STRING = auto()

    AND=auto()
    OR=auto()

    NOT=auto();  PLUS = auto(); MINUS = auto(); MUL = auto(); DIV = auto()

    PP = auto(); MM=auto(); EQEQ = auto(); NOTEQ = auto()
    LT = auto(); LTEQ = auto(); GT = auto(); GTEQ = auto()

    ASSIGN = auto()
    COLON = auto(); COMMA = auto(); DOT = auto()
    LPAREN = auto(); RPAREN = auto()
    LBRACE = auto(); RBRACE = auto()
    LBRACKET = auto(); RBRACKET = auto()

    NEWLINE = auto(); INDENT = auto(); DEDENT = auto()
    EOF = auto()

    TRUE=auto()
    FALSE=auto()


KEYWORDS = {
    'True':TokenType.TRUE,
    'False':TokenType.FALSE,
    'or':TokenType.OR,
    'and':TokenType.AND,
    'print':TokenType.PRINT,
    'Class':TokenType.CLASS,
    'def': TokenType.DEF,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'elif': TokenType.ELIF,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'return': TokenType.RETURN,
    'True': TokenType.TRUE,
    'False': TokenType.FALSE,
    'None': TokenType.NONE,
    'pass': TokenType.PASS,
}


class Token:
    def __init__(self, type_, lexeme, literal, line):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.lexeme)}, {repr(self.literal)}, line={self.line})"


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.indents = [0]  
        self.dedent_pending = 0 


    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current

            if self.dedent_pending > 0:
                self.tokens.append(Token(TokenType.DEDENT, '', None, self.line))
                self.dedent_pending -= 1
            else:
                self.scan_token()
           
        while len(self.indents) > 1:
            self.indents.pop()
            self.tokens.append(Token(TokenType.DEDENT, '', None, self.line))
            
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()

        if c in ' \r\t':
            pass
        elif c == '\n':
            self.tokens.append(Token(TokenType.NEWLINE, c, None, self.line))
            self.line += 1
            self.handle_indentation()

        elif c == '+':
            self.add_token(print("Unexpected '++'. Increment operator not supported." )if self.match('+')else TokenType.PLUS)
        elif c == '-':
            self.add_token(print("Unexpected '--'. Decrement operator not supported.")  if self.match('-')else TokenType.MINUS)
        elif c == '*':
            self.add_token(TokenType.MUL)
        elif c == '/':
            self.add_token(TokenType.DIV)
        elif c == '=':
            self.add_token(TokenType.EQEQ if self.match('=') else TokenType.ASSIGN)
        elif c == '!':
            self.add_token(TokenType.NOTEQ if self.match('=') else None)
        elif c == '<':
            self.add_token(TokenType.LTEQ if self.match('=') else TokenType.LT)
        elif c == '>':
            self.add_token(TokenType.GTEQ if self.match('=') else TokenType.GT)
        elif c == ':':
            self.add_token(TokenType.COLON)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '(':
            self.add_token(TokenType.LPAREN)
        elif c == ')':
            self.add_token(TokenType.RPAREN)
        elif c == '{':
            self.add_token(TokenType.LBRACE)
        elif c == '}':
            self.add_token(TokenType.RBRACE)
        elif c == '[':
            self.add_token(TokenType.LBRACKET)
        elif c == ']':
            self.add_token(TokenType.RBRACKET)
        elif c == '"':
            self.string()
        elif c.isdigit():
            self.number()
        elif c.isalpha() or c == '_':
            self.identifier()
        else:
            print(f"[Line {self.line}] Unexpected character: '{c}'")

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
        type_ = KEYWORDS.get(text, TokenType.IDENTIFIER)
        if text == "True":
            self.add_token(TokenType.TRUE, True)
        elif text == "False":
            self.add_token(TokenType.FALSE, False)
        else:
            self.add_token(type_)
    
    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        value = float(self.source[self.start:self.current])
        self.add_token(TokenType.NUMBER, value)

    def string(self):
        while not self.is_at_end() and self.peek() != '"':
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            print(f"[Line {self.line}] Unterminated string")
            return
        self.advance() 
        value = self.source[self.start + 1: self.current - 1]
        self.add_token(TokenType.STRING, value)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        return '\0' if self.is_at_end() else self.source[self.current]

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c

    def is_at_end(self):
        return self.current >= len(self.source)

    def add_token(self, type_, literal=None):
        if type_ is None:
            print(f"[Line {self.line}] Invalid token")
            return
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type_, text, literal, self.line))
    def handle_indentation(self):
            spaces = 0
            while not self.is_at_end():
                c = self.peek()
                if c == ' ':
                    spaces += 1
                    self.advance()
                elif c == '\t':
                    spaces += 4 
                    self.advance()
                elif c == '\n':
                    self.tokens.append(Token(TokenType.NEWLINE, '\n', None, self.line))
                    self.line += 1
                else:
                    break

            current_indent = self.indents[-1]
            if spaces > current_indent:
                self.indents.append(spaces)
                self.tokens.append(Token(TokenType.INDENT, '', None, self.line))
            elif spaces < current_indent:
                while self.indents and self.indents[-1] > spaces:
                    self.indents.pop()
                    self.dedent_pending += 1



