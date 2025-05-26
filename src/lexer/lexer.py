class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position] if self.source_code else None

    def advance(self):
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char.isalpha():
                tokens.append(self._identifier())
            elif self.current_char.isdigit():
                tokens.append(self._number())
            elif self.current_char == '+':
                tokens.append(('PLUS', '+'))
                self.advance()
            elif self.current_char == '-':
                tokens.append(('MINUS', '-'))
                self.advance()
            elif self.current_char == '*':
                tokens.append(('MULTIPLY', '*'))
                self.advance()
            elif self.current_char == '/':
                tokens.append(('DIVIDE', '/'))
                self.advance()
            elif self.current_char == '=':
                tokens.append(('ASSIGN', '='))
                self.advance()
            elif self.current_char == '(':
                tokens.append(('LPAREN', '('))
                self.advance()
            elif self.current_char == ')':
                tokens.append(('RPAREN', ')'))
                self.advance()
            else:
                tokens.append(('UNKNOWN', self.current_char))
                self.advance()
        return tokens

    def _identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        return ('IDENTIFIER', result)

    def _number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ('NUMBER', result)