class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None

    def parse(self):
        ast = []
        while self.current_token is not None:
            ast.append(self._expression())
        return ast

    def _expression(self):
        if self.current_token[0] == 'IDENTIFIER':
            identifier = self.current_token[1]
            self.advance()
            if self.current_token and self.current_token[0] == 'ASSIGN':
                self.advance()
                value = self._expression()
                return {'type': 'Assignment', 'identifier': identifier, 'value': value}
            return {'type': 'Identifier', 'value': identifier}
        return self._binary_operation()

    def _binary_operation(self):
        left = self._term()
        while self.current_token and self.current_token[0] in ('PLUS', 'MINUS'):
            operator = self.current_token[1]
            self.advance()
            right = self._term()
            left = {'type': 'BinaryOperation', 'operator': operator, 'left': left, 'right': right}
        return left

    def _term(self):
        left = self._factor()
        while self.current_token and self.current_token[0] in ('MULTIPLY', 'DIVIDE'):
            operator = self.current_token[1]
            self.advance()
            right = self._factor()
            left = {'type': 'BinaryOperation', 'operator': operator, 'left': left, 'right': right}
        return left

    def _factor(self):
        if self.current_token[0] == 'NUMBER':
            number = self.current_token[1]
            self.advance()
            return {'type': 'Number', 'value': number}
        elif self.current_token[0] == 'LPAREN':
            self.advance()
            expr = self._expression()
            if self.current_token and self.current_token[0] == 'RPAREN':
                self.advance()
                return expr
            else:
                raise Exception("Expected closing parenthesis")
        elif self.current_token[0] == 'IDENTIFIER':
            identifier = self.current_token[1]
            self.advance()
            return {'type': 'Identifier', 'value': identifier}
        else:
            raise Exception(f"Unexpected token: {self.current_token}")