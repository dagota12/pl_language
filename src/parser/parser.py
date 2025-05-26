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
        token_type, token_value = self.current_token
        if token_type == 'IDENTIFIER':
            self.advance()
            return {'type': 'Identifier', 'value': token_value}
        elif token_type == 'NUMBER':
            self.advance()
            return {'type': 'Number', 'value': token_value}
        else:
            self.advance()
            return {'type': 'Unknown', 'value': token_value}