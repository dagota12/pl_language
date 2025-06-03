class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code
        self.position = 0
        self.current_char = self.source_code[self.position] if self.source_code else None
        
        # Define the Amharic token map (keyword string to token type)
        # Using uppercase for token types is a common convention.
        self.amharic_keywords = {
            # Control Flow
            'ከሆነ': 'IF',
            'ካልሆነ': 'ELSE',
            'እስከሆነ_ድረስ': 'WHILE',
            'ለእያንዳንዱ': 'FOR',  # "For each"
            'አቋርጥ': 'BREAK',
            'ቀጥል': 'CONTINUE',

            # Function Definition
            'ግለጽ': 'DEF',
            'መልስ': 'RETURN',

            # Logical Operators (as keywords)
            'እና': 'AND',
            'ወይም': 'OR',
            'ተቃራኒ': 'NOT',  # "Opposite/negation" for boolean NOT

            # Assignment (if using Amharic word)
            'ይሁን': 'ASSIGN_KW',  # "Let it be / Becomes" for '=' written as a word

            # Input/Output
            'አውጣ': 'PRINT',  # Your 'SPIT' -> 'PRINT' token type
            'አስገባ': 'INPUT',

            # Boolean Literals
            'እውነት': 'TRUE_LITERAL',
            'ሐሰት': 'FALSE_LITERAL',

            # Membership
            'ውስጥ': 'IN',
        }
        
        # Keep English keywords for backward compatibility
        self.english_keywords = {
            'if': 'IF', 
            'else': 'ELSE', 
            'while': 'WHILE', 
            'def': 'DEF', 
            'return': 'RETURN',
            'and': 'AND',
            'or': 'OR',
            'not': 'NOT',
            'spit': 'SPIT'  # Keep existing spit function
        }
        
        # Combine both keyword sets
        self.keywords = {**self.english_keywords, **self.amharic_keywords}

    def advance(self):
        self.position += 1
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None
    
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def peek(self, offset=1):
        """Peek ahead by offset characters"""
        peek_pos = self.position + offset
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]
        return None

    def peek_word(self, word_length):
        """Peek ahead to get a word of specified length"""
        if self.position + word_length <= len(self.source_code):
            return self.source_code[self.position:self.position + word_length]
        return None

    def skip_comment(self):
        """Skip comments (from # to end of line)"""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()

    def _check_multi_word_keywords(self):
        """Check for multi-word Amharic keywords first"""
        # Sort keywords by length (longest first) to match longer keywords first
        sorted_keywords = sorted(self.amharic_keywords.keys(), key=len, reverse=True)
        
        for keyword in sorted_keywords:
            if '_' in keyword:
                # Handle keywords with underscores (like እስከሆነ_ድረስ)
                # Replace underscore with space for matching
                keyword_to_match = keyword.replace('_', ' ')
            else:
                keyword_to_match = keyword
                
            if self.source_code[self.position:].startswith(keyword_to_match):
                # Check if this is a complete word (not part of a larger identifier)
                next_pos = self.position + len(keyword_to_match)
                if (next_pos >= len(self.source_code) or 
                    not self._is_identifier_char(self.source_code[next_pos])):
                    
                    # Advance position past the keyword
                    for _ in range(len(keyword_to_match)):
                        self.advance()
                    
                    return (self.amharic_keywords[keyword], keyword_to_match)
        
        return None

    def _is_identifier_char(self, char):
        """Check if character can be part of an identifier (supports Unicode/Amharic)"""
        # Amharic Unicode ranges:
        # U+1200–U+137F: Ethiopic (main Amharic script)
        # U+1380–U+139F: Ethiopic Supplement
        # U+2D80–U+2DDF: Ethiopic Extended
        char_code = ord(char)
        return (char.isalnum() or char == '_' or 
                (0x1200 <= char_code <= 0x137F) or  # Main Ethiopic
                (0x1380 <= char_code <= 0x139F) or  # Ethiopic Supplement
                (0x2D80 <= char_code <= 0x2DDF))     # Ethiopic Extended

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            elif self.current_char == '#':
                self.skip_comment()
                continue
            
            # Check for multi-word keywords first (highest priority)
            multi_word_result = self._check_multi_word_keywords()
            if multi_word_result:
                token_type, keyword = multi_word_result
                tokens.append((token_type, keyword))
                continue
            
            # Check for operators before identifiers
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
            elif self.current_char == '"':
                tokens.append(self._string())
            elif self.current_char == "'":
                tokens.append(self._string())
            # Check for numbers
            elif self.current_char.isdigit():
                tokens.append(self._number())
            # Check for single-word identifiers/keywords (lower priority)
            elif self._is_identifier_char(self.current_char):
                tokens.append(self._identifier())
            else:
                tokens.append(('UNKNOWN', self.current_char))
                self.advance()
        return tokens

    def _identifier(self):
        result = ''
        while self.current_char is not None and self._is_identifier_char(self.current_char):
            result += self.current_char
            self.advance()
        
        # Check if this identifier is a keyword
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

    def _string(self):
        """Handle string literals with both single and double quotes"""
        quote_char = self.current_char
        result = ''
        self.advance()  # Skip opening quote
        
        while self.current_char is not None and self.current_char != quote_char:
            result += self.current_char
            self.advance()
        
        if self.current_char == quote_char:
            self.advance()  # Skip closing quote
        else:
            raise Exception("Unterminated string literal")
            
        return ('STRING', result)