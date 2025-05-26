class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position] if self.source_code else None
        self.keywords = {
            'if': 'IF', 
            'else': 'ELSE', 
            'while': 'WHILE', 
            'def': 'DEF', 
            'return': 'RETURN',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
            'spit': 'SPIT'  # Adding the spit keyword for our print function
        }

    def advance(self):
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek(self):
        if self.position + 1 < len(self.source_code):
            return self.source_code[self.position + 1]
        return None

    def skip_comment(self):
        """Skip comments (from # to end of line)"""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()  # Skip the newline as well

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char == '#':
                self.skip_comment()
                continue
            elif self.current_char.isalpha():
                tokens.append(self._identifier())
            elif self.current_char.isdigit():
                tokens.append(self._number())
            elif self.current_char == '=' and self.peek() == '=':
                tokens.append(('EQUALS', '=='))
                self.advance()
                self.advance()
            elif self.current_char == '!' and self.peek() == '=':
                tokens.append(('NOT_EQUALS', '!='))
                self.advance()
                self.advance()
            elif self.current_char == '!' and self.peek() != '=':
                # This is our factorial operator
                tokens.append(('FACTORIAL', '!'))
                self.advance()
            elif self.current_char == '<':
                if self.peek() == '=':
                    tokens.append(('LESS_EQUALS', '<='))
                    self.advance()
                else:
                    tokens.append(('LESS', '<'))
                self.advance()
            elif self.current_char == '>':
                if self.peek() == '=':
                    tokens.append(('GREATER_EQUALS', '>='))
                    self.advance()
                else:
                    tokens.append(('GREATER', '>'))
                self.advance()
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
            elif self.current_char == ':':
                tokens.append(('COLON', ':'))
                self.advance()
            elif self.current_char == ',':
                tokens.append(('COMMA', ','))
                self.advance()
            elif self.current_char == ';':
                tokens.append(('SEMICOLON', ';'))
                self.advance()
            elif self.current_char == '%':
                tokens.append(('MODULO', '%'))
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
        if result in self.keywords:
            return (self.keywords[result], result)
        return ('IDENTIFIER', result)

    def _number(self):
        result = ''
        # Check if this is a negative number prefixed with minus
        if self.current_char == '-':
            result += self.current_char
            self.advance()
            
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return ('NUMBER', result)