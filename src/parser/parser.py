class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None
        # Add tokens_iter for compatibility with tests
        self.tokens_iter = iter(tokens)

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
            
    def _eat(self, token_type):
        """
        Checks if the current token matches the expected type and advances if it does,
        otherwise raises an exception.
        """
        if self.current_token and self.current_token[0] == token_type:
            value = self.current_token
            self.advance()
            return value
        else:
            raise Exception(f"Expected token type {token_type}, got {self.current_token}")

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
            # Check if there's another statement to parse
            if self.current_token and self.current_token[0] not in ('EOF', None):
                # Don't parse ELSE as a new statement - it should be handled by the if_statement
                if self.current_token[0] == 'ELSE':
                    break
                # For control flow keywords within blocks, we need to be more careful
                # Only break if this looks like a new top-level function definition
                elif self.current_token[0] == 'DEF':
                    # This is definitely a new top-level function, stop here
                    break
                # For RETURN statements, they should end the current block context
                elif self.current_token[0] == 'RETURN':
                    # Add the return statement and stop
                    statements.append(self._statement())
                    break
                # For IF and WHILE, they can be nested within blocks, so continue parsing
                else:
                    statements.append(self._statement())
            else:
                break
            
        return {
            'type': 'Block',
            'statements': statements
        }

    def _if_statement(self):
        self.advance()  # Skip 'if'
        condition = self._expression()
        
        if self.current_token and self.current_token[0] == 'COLON':
            self.advance()  # Skip ':'
            
            # Parse true branch - collect statements until we see ELSE or end
            true_statements = []
            
            # Parse first statement of true branch
            true_statements.append(self._statement())
            
            # Continue parsing statements in true branch until we hit ELSE
            while (self.current_token and 
                   self.current_token[0] == 'SEMICOLON'):
                self.advance()  # Skip semicolon
                
                # Check if next token is ELSE - if so, break to handle else clause
                if self.current_token and self.current_token[0] == 'ELSE':
                    break
                    
                # Otherwise, parse another statement for the true branch
                if self.current_token:
                    true_statements.append(self._statement())
            
            true_branch = {
                'type': 'Block',
                'statements': true_statements
            }
            
            false_branch = None
            
            # Check for else part
            if self.current_token and self.current_token[0] == 'ELSE':
                self.advance()  # Skip 'else'
                if self.current_token and self.current_token[0] == 'COLON':
                    self.advance()  # Skip ':'
                    
                    # Parse false branch statements
                    false_statements = []
                    false_statements.append(self._statement())
                    
                    # Continue parsing semicolon-separated statements in false branch
                    # But be more careful about when to stop
                    while (self.current_token and 
                           self.current_token[0] == 'SEMICOLON'):
                        self.advance()  # Skip semicolon
                        
                        # Stop if we reach end of input
                        if not self.current_token:
                            break
                            
                        # Stop if we see control flow keywords that indicate new top-level statements
                        if self.current_token[0] in ('IF', 'WHILE', 'DEF'):
                            break
                            
                        # Stop if we see what looks like a new variable assignment that's not part of this block
                        # This is a heuristic - if we have multiple statements already and see an identifier
                        # followed by assignment, it might be a new top-level statement
                        if (len(false_statements) >= 1 and 
                            self.current_token and self.current_token[0] == 'IDENTIFIER'):
                            # Look ahead to see if this is an assignment
                            next_pos = self.position + 1
                            if (next_pos < len(self.tokens) and 
                                self.tokens[next_pos][0] == 'ASSIGN'):
                                # This looks like a new top-level assignment, stop here
                                break
                            
                        if self.current_token:
                            false_statements.append(self._statement())
                    
                    false_branch = {
                        'type': 'Block',
                        'statements': false_statements
                    }
                else:
                    raise Exception("Expected ':' after 'else'")
                    
            return {'type': 'IfStatement', 'condition': condition, 'true_branch': true_branch, 'false_branch': false_branch}
        else:
            raise Exception(f"Expected ':' after 'if' condition")

    def _while_statement(self):
        self.advance()  # Skip 'while'
        condition = self._expression()
        
        if self.current_token and self.current_token[0] == 'COLON':
            self.advance()  # Skip ':'
            
            # Parse body - always wrap in a block
            if self.current_token and self.current_token[0] == 'NEWLINE':
                self.advance()  # Skip newline
                body = self._block()
            else:
                # Parse all statements that are part of this while loop body
                # This includes semicolon-separated statements on the same line
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
                        body = self._function_body()  # Use specialized function body parser
                        return {'type': 'FunctionDefinition', 'name': function_name, 'parameters': parameters, 'body': body}
                    else:
                        raise Exception("Expected ':' after function parameters")
                else:
                    raise Exception("Expected ')' after function parameters")
            else:
                raise Exception("Expected '(' after function name")
        else:
            raise Exception("Expected function name after 'def'")

    def _function_body(self):
        """Parse a function body, collecting statements until we hit a new function definition."""
        statements = []
        
        # Parse statements until we hit a new top-level construct
        while self.current_token:
            # Stop if we see a new function definition
            if self.current_token[0] == 'DEF':
                break
                
            # Stop if we see what looks like a top-level assignment to a built-in operation
            if (self.current_token[0] == 'IDENTIFIER' and 
                len(statements) > 0):  # Only apply this heuristic if we already have statements
                # Look ahead to see if this is an assignment
                next_pos = self.position + 1
                if (next_pos < len(self.tokens) and 
                    self.tokens[next_pos][0] == 'ASSIGN'):
                    # Check for factorial operator assignment (likely top-level)
                    if (next_pos + 1 < len(self.tokens) and
                        self.tokens[next_pos + 1][0] == 'NUMBER' and
                        next_pos + 2 < len(self.tokens) and
                        self.tokens[next_pos + 2][0] == 'FACTORIAL'):
                        # This looks like: variable = number!
                        # Definitely a top-level statement
                        break
                    # Check if this looks like a function call assignment (common pattern)
                    if (next_pos + 1 < len(self.tokens) and
                        self.tokens[next_pos + 1][0] == 'IDENTIFIER' and
                        next_pos + 2 < len(self.tokens) and
                        self.tokens[next_pos + 2][0] == 'LPAREN'):
                        # This looks like: variable = function_call(args)
                        # Likely a new top-level statement
                        break
                        
            # Stop if we see a top-level function call (not an assignment)
            if (self.current_token[0] == 'IDENTIFIER' and 
                len(statements) > 0):
                next_pos = self.position + 1
                if (next_pos < len(self.tokens) and
                    self.tokens[next_pos][0] == 'LPAREN'):
                    # This is a standalone function call, likely top-level
                    break
                    
            # Stop if we see a standalone SPIT call (top-level output)
            if self.current_token[0] == 'SPIT':
                # Spit calls at the top level are common
                if len(statements) > 0:  # Only if we already have function body content
                    break
            
            # Parse the statement
            statement = self._statement()
            statements.append(statement)
            
            # Skip semicolons between statements
            while self.current_token and self.current_token[0] == 'SEMICOLON':
                self.advance()
                
        return {
            'type': 'Block',
            'statements': statements
        }

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
            elif self.current_token and self.current_token[0] == 'ASSIGN_KW':
                self.advance()  # Skip Amharic assignment keyword 'ይሁን'
                value = self._expression()
                return {'type': 'Assignment', 'identifier': identifier, 'value': value}
            
            # If no assignment, treat as an expression
            self.position -= 1  # Go back to identifier
            self.current_token = self.tokens[self.position]
            
        return self._expression()

    def _expression(self):
        # Logical operators have the lowest precedence
        return self._logical()

    def _logical(self):
        left = self._comparison()
        
        while self.current_token and self.current_token[0] in ('AND', 'OR'):
            operator = self.current_token[1]
            self.advance()
            right = self._comparison()
            left = {'type': 'LogicalOperation', 'operator': operator, 'left': left, 'right': right}
            
        return left

    def _comparison(self):
        left = self._arithmetic()
        
        while self.current_token and self.current_token[0] in ('EQUALS', 'NOT_EQUALS', 'LESS', 'LESS_EQUALS', 'GREATER', 'GREATER_EQUALS'):
            operator = self.current_token[1]
            self.advance()
            right = self._arithmetic()
            left = {'type': 'Comparison', 'operator': operator, 'left': left, 'right': right}
            
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
        
        while self.current_token and self.current_token[0] in ('MULTIPLY', 'DIVIDE', 'MODULO'):
            operator = self.current_token[1]
            self.advance()
            right = self._factor()
            left = {'type': 'BinaryOperation', 'operator': operator, 'left': left, 'right': right}
            
        return left

    def _factor(self):
        """Parse factors (numbers, identifiers, function calls, parentheses, unary operations)"""
        token_type, token_value = self.current_token
        
        # Handle unary operators (negative numbers)
        if token_type == 'MINUS' or token_type == 'NOT' or token_type == 'ተቃራኒ':
            operator = token_value
            self.advance()
            operand = self._factor()  # Recursively parse the operand
            return {
                'type': 'UnaryOperation',
                'operator': operator,
                'operand': operand
            }
        
        # Handle parentheses
        elif self.current_token and self.current_token[0] == 'LPAREN':
            self._eat('LPAREN')
            expr = self._expression()
            self._eat('RPAREN')
            return expr

        # Handle numbers
        elif self.current_token and self.current_token[0] == 'NUMBER':
            value = self.current_token[1]
            self._eat('NUMBER')
            
            # Check for factorial operator
            if self.current_token and self.current_token[0] == 'FACTORIAL':
                self._eat('FACTORIAL')
                return {'type': 'Factorial', 'value': {'type': 'Number', 'value': value}}
                
            return {'type': 'Number', 'value': value}
            
        # Handle string literals
        elif self.current_token and self.current_token[0] == 'STRING':
            value = self.current_token[1]
            self._eat('STRING')
            return {'type': 'String', 'value': value}

        # Handle identifiers (variables, function calls)
        elif self.current_token and self.current_token[0] == 'IDENTIFIER' or self.current_token and self.current_token[0] == 'SPIT' or self.current_token and self.current_token[0] == 'PRINT':
            identifier = self.current_token[1]
            token_type = self.current_token[0]
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
                    
                    # Special handling for spit function and Amharic print function
                    if token_type == 'SPIT' or token_type == 'PRINT':
                        return {'type': 'SpitFunction', 'arguments': arguments}
                    else:
                        return {'type': 'FunctionCall', 'name': identifier, 'arguments': arguments}
                else:
                    raise Exception("Expected ')' after function arguments")
                    
            # Check for factorial operator after identifier
            if self.current_token and self.current_token[0] == 'FACTORIAL':
                self.advance()  # Skip '!'
                return {'type': 'Factorial', 'value': {'type': 'Identifier', 'value': identifier}}
            
            return {'type': 'Identifier', 'value': identifier}
        else:
            raise Exception(f"Unexpected token: {self.current_token}")