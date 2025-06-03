"""
Transpiler module for converting our custom language AST to Python code.
This allows our custom language to be executed as Python.
"""

class Transpiler:
    def __init__(self):
        self.indent_level = 0
        
    def _indent(self):
        """Return the current indentation string"""
        return "    " * self.indent_level
    
    def transpile(self, ast):
        """Convert an AST to Python code"""
        if isinstance(ast, list):
            return '\n'.join(self._transpile_node(node) for node in ast)
        else:
            return self._transpile_node(ast)
    
    def _transpile_node(self, node):
        """Transpile a single AST node"""
        if node['type'] == 'Number':
            return node['value']
        
        elif node['type'] == 'String':
            return f'"{node["value"]}"'
        
        elif node['type'] == 'Identifier':
            return node['value']
        
        elif node['type'] == 'Assignment':
            value = self._transpile_node(node['value'])
            return f"{node['identifier']} = {value}"
        
        elif node['type'] == 'BinaryOperation':
            left = self._transpile_node(node['left'])
            right = self._transpile_node(node['right'])
            return f"({left} {node['operator']} {right})"
        
        elif node['type'] == 'Comparison':
            left = self._transpile_node(node['left'])
            right = self._transpile_node(node['right'])
            return f"({left} {node['operator']} {right})"
        
        elif node['type'] == 'LogicalOperation':
            left = self._transpile_node(node['left'])
            right = self._transpile_node(node['right'])
            # Convert Amharic operators to Python
            operator = node['operator']
            if operator == 'እና':
                operator = 'and'
            elif operator == 'ወይም':
                operator = 'or'
            return f"({left} {operator} {right})"
        
        elif node['type'] == 'IfStatement':
            condition = self._transpile_node(node['condition'])
            result = f"if {condition}:\n"
            
            self.indent_level += 1
            true_branch = self._transpile_node(node['true_branch'])
            result += self._add_indentation(true_branch)
            self.indent_level -= 1
            
            if node['false_branch']:
                result += "\nelse:\n"
                self.indent_level += 1
                false_branch = self._transpile_node(node['false_branch'])
                result += self._add_indentation(false_branch)
                self.indent_level -= 1
            
            return result
        
        elif node['type'] == 'WhileStatement':
            condition = self._transpile_node(node['condition'])
            result = f"while {condition}:\n"
            
            self.indent_level += 1
            body = self._transpile_node(node['body'])
            result += self._add_indentation(body)
            self.indent_level -= 1
            
            return result
        
        elif node['type'] == 'Block':
            statements = []
            for statement in node['statements']:
                statements.append(self._transpile_node(statement))
            return '\n'.join(statements)
        
        elif node['type'] == 'FunctionDefinition':
            params = ', '.join(node['parameters'])
            result = f"def {node['name']}({params}):\n"
            
            self.indent_level += 1
            body = self._transpile_node(node['body'])
            result += self._add_indentation(body)
            self.indent_level -= 1
            
            return result
        
        elif node['type'] == 'FunctionCall':
            args = ', '.join(self._transpile_node(arg) for arg in node['arguments'])
            return f"{node['name']}({args})"
        
        elif node['type'] == 'ReturnStatement':
            value = self._transpile_node(node['value'])
            return f"return {value}"
        
        elif node['type'] == 'SpitFunction':
            # Convert spit() and አውጣ() to print()
            args = ', '.join(self._transpile_node(arg) for arg in node['arguments'])
            return f"print({args})"
        
        elif node['type'] == 'Factorial':
            value = self._transpile_node(node['value'])
            return f"math.factorial({value})"
        
        else:
            raise Exception(f"Unknown node type for transpilation: {node['type']}")
    
    def _add_indentation(self, code):
        """Add proper indentation to code"""
        lines = code.split('\n')
        indented_lines = []
        for line in lines:
            if line.strip():  # Don't indent empty lines
                indented_lines.append(self._indent() + line)
            else:
                indented_lines.append(line)
        return '\n'.join(indented_lines)