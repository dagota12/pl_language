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
            statement = self._statement()
            ast.append(statement)
            # Skip any trailing semicolons between top-level statements
            while self.current_token and self.current_token[0] == 'SEMICOLON':
                self.advance()
        return ast

    def _statement(self):
        if self.current_token[0] == 'IF':
            return self._if_statement()
        elif self.current_token[0] == 'WHILE':
            return self._while_statement()
        elif self.current_token[0] == 'DEF':
            return self._function_definition()
        elif self.current_token[0] == 'RETURN':
            return self._return_statement()
        elif self.current_token[0] == 'ELSE':
            raise Exception("Unexpected 'else' without matching 'if'")
        elif self.current_token[0] == 'SEMICOLON':
            self.advance()  # Skip the semicolon and parse the next statement
            return self._statement()
        else:
            return self._assignment()

    def _block(self):
        """Parse a block of statements (for function bodies and control structures)."""
        statements = []
        
        # Add the first statement
        statements.append(self._statement())
        
        # Check for semicolons indicating multiple statements in the block
        while self.current_token and self.current_token[0] == 'SEMICOLON':
            self.advance()  # Skip the semicolon
            if self.current_token:  # Ensure there's another statement after the semicolon
                statements.append(self._statement())
            
        return {
            'type': 'Block',
            'statements': statements
        }

    def _if_statement(self):
        self.advance()  # Skip 'if'
        condition = self._expression()
        
        if self.current_token and self.current_token[0] == 'COLON':
            self.advance()  # Skip ':'
            true_branch = self._block()
            false_branch = None
            
            # Check for else part
            if self.current_token and self.current_token[0] == 'ELSE':
                self.advance()  # Skip 'else'
                if self.current_token and self.current_token[0] == 'COLON':
                    self.advance()  # Skip ':'
                    false_branch = self._block()
                else:
                    raise Exception("Expected ':' after 'else'")
                    
            return {'type': 'IfStatement', 'condition': condition, 'true_branch': true_branch, 'false_branch': false_branch}
        else:
            raise Exception("Expected ':' after 'if' condition")

    def _while_statement(self):
        self.advance()  # Skip 'while'
        condition = self._expression()
        
        if self.current_token and self.current_token[0] == 'COLON':
            self.advance()  # Skip ':'
            body = self._block()
            return {'type': 'WhileStatement', 'condition': condition, 'body': body}
        else:
            raise Exception("Expected ':' after 'while' condition")

    def _function_definition(self):
        self.advance()  # Skip 'def'
        
        if self.current_token and self.current_token[0] == 'IDENTIFIER':
            function_name = self.current_token[1]
            self.advance()  # Skip function name
            
            if self.current_token and self.current_token[0] == 'LPAREN':
                self.advance()  # Skip '('
                parameters = []
                
                # Parse parameters
                if self.current_token and self.current_token[0] == 'IDENTIFIER':
                    parameters.append(self.current_token[1])
                    self.advance()
                    
                    while self.current_token and self.current_token[0] == 'COMMA':
                        self.advance()  # Skip ','
                        if self.current_token and self.current_token[0] == 'IDENTIFIER':
                            parameters.append(self.current_token[1])
                            self.advance()
                        else:
                            raise Exception("Expected parameter name after ','")
                
                if self.current_token and self.current_token[0] == 'RPAREN':
                    self.advance()  # Skip ')'
                    
                    if self.current_token and self.current_token[0] == 'COLON':
                        self.advance()  # Skip ':'
                        body = self._block()
                        return {'type': 'FunctionDefinition', 'name': function_name, 'parameters': parameters, 'body': body}
                    else:
                        raise Exception("Expected ':' after function parameters")
                else:
                    raise Exception("Expected ')' after function parameters")
            else:
                raise Exception("Expected '(' after function name")
        else:
            raise Exception("Expected function name after 'def'")

    def _return_statement(self):
        self.advance()  # Skip 'return'
        value = self._expression()
        return {'type': 'ReturnStatement', 'value': value}

    def _assignment(self):
        if self.current_token[0] == 'IDENTIFIER':
            identifier = self.current_token[1]
            self.advance()
            
            if self.current_token and self.current_token[0] == 'ASSIGN':
                self.advance()  # Skip '='
                value = self._expression()
                return {'type': 'Assignment', 'identifier': identifier, 'value': value}
            
            # If no assignment, treat as an expression
            self.position -= 1  # Go back to identifier
            self.current_token = self.tokens[self.position]
            
        return self._expression()

    def _expression(self):
        left = self._arithmetic()
        
        if self.current_token and self.current_token[0] in ('EQUALS', 'NOT_EQUALS', 'LESS', 'LESS_EQUALS', 'GREATER', 'GREATER_EQUALS'):
            operator = self.current_token[1]
            self.advance()
            right = self._arithmetic()
            return {'type': 'Comparison', 'operator': operator, 'left': left, 'right': right}
            
        return left

    def _arithmetic(self):
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
            
            # Check if this is a function call
            if self.current_token and self.current_token[0] == 'LPAREN':
                self.advance()  # Skip '('
                arguments = []
                
                # Parse arguments
                if self.current_token and self.current_token[0] != 'RPAREN':
                    arguments.append(self._expression())
                    
                    while self.current_token and self.current_token[0] == 'COMMA':
                        self.advance()  # Skip ','
                        arguments.append(self._expression())
                
                if self.current_token and self.current_token[0] == 'RPAREN':
                    self.advance()  # Skip ')'
                    return {'type': 'FunctionCall', 'name': identifier, 'arguments': arguments}
                else:
                    raise Exception("Expected ')' after function arguments")
            
            return {'type': 'Identifier', 'value': identifier}
        else:
            raise Exception(f"Unexpected token: {self.current_token}")