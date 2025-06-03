"""
Interpreter module for executing our custom language AST.
The interpreter directly executes the Abstract Syntax Tree without
generating intermediate code.
"""

import math

class Function:
    def __init__(self, name, parameters, body, closure_env):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.closure_env = closure_env

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.call_stack = []
        
    def evaluate(self, node):
        """Evaluate an AST node and return its value."""
        if node['type'] == 'Number':
            return int(node['value'])
        
        elif node['type'] == 'String':
            return node['value']
        
        elif node['type'] == 'Identifier':
            name = node['value']
            if name in self.variables:
                return self.variables[name]
            else:
                raise Exception(f"Undefined variable: {name}")
        
        elif node['type'] == 'Assignment':
            value = self.evaluate(node['value'])
            self.variables[node['identifier']] = value
            return value
        
        elif node['type'] == 'BinaryOperation':
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])
            operator = node['operator']
            
            if operator == '+':
                return left + right
            elif operator == '-':
                return left - right
            elif operator == '*':
                return left * right
            elif operator == '/':
                if right == 0:
                    raise Exception("Division by zero")
                return left / right
            elif operator == '%':
                return left % right
            else:
                raise Exception(f"Unknown binary operator: {operator}")
        
        elif node['type'] == 'Comparison':
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])
            operator = node['operator']
            
            if operator == '==':
                return left == right
            elif operator == '!=':
                return left != right
            elif operator == '<':
                return left < right
            elif operator == '<=':
                return left <= right
            elif operator == '>':
                return left > right
            elif operator == '>=':
                return left >= right
            else:
                raise Exception(f"Unknown comparison operator: {operator}")
        
        elif node['type'] == 'LogicalOperation':
            left = self.evaluate(node['left'])
            operator = node['operator']
            
            # Short-circuit evaluation
            if operator == 'and' or operator == 'እና':
                if not left:
                    return left
                return self.evaluate(node['right'])
            elif operator == 'or' or operator == 'ወይም':
                if left:
                    return left
                return self.evaluate(node['right'])
            else:
                raise Exception(f"Unknown logical operator: {operator}")
        
        elif node['type'] == 'IfStatement':
            condition = self.evaluate(node['condition'])
            if condition:
                return self.evaluate(node['true_branch'])
            elif node['false_branch']:
                return self.evaluate(node['false_branch'])
            return None
        
        elif node['type'] == 'WhileStatement':
            result = None
            iteration_count = 0  # Initialize iteration counter
            while self.evaluate(node['condition']):
                iteration_count += 1
                if iteration_count > 500:  # Terminate after 500 iterations
                    print("Debug: Terminating while loop after 500 iterations")
                    break
                result = self.evaluate(node['body'])
                # If we encounter a return statement, propagate it immediately
                if isinstance(result, dict) and result.get('type') == 'return':
                    return result
            return result
        
        elif node['type'] == 'Block':
            result = None
            for statement in node['statements']:
                result = self.evaluate(statement)
                # Handle return statements in blocks
                if isinstance(result, dict) and result.get('type') == 'return':
                    return result
            return result
        
        elif node['type'] == 'FunctionDefinition':
            func = Function(
                node['name'],
                node['parameters'],
                node['body'],
                dict(self.variables)  # Capture current environment
            )
            self.functions[node['name']] = func
            return None
        
        elif node['type'] == 'FunctionCall':
            func_name = node['name']
            if func_name not in self.functions:
                raise Exception(f"Undefined function: {func_name}")
            
            func = self.functions[func_name]
            args = [self.evaluate(arg) for arg in node['arguments']]
            
            if len(args) != len(func.parameters):
                raise Exception(f"Function {func_name} expects {len(func.parameters)} arguments, got {len(args)}")
            
            # Save current state
            old_vars = dict(self.variables)
            
            # Set up function environment
            self.variables.update(func.closure_env)
            for param, arg in zip(func.parameters, args):
                self.variables[param] = arg
            
            # Execute function body
            try:
                result = self.evaluate(func.body)
                # Handle return value
                if isinstance(result, dict) and result.get('type') == 'return':
                    return_value = result['value']
                else:
                    return_value = None
            finally:
                # Restore previous environment
                self.variables = old_vars
            
            return return_value
        
        elif node['type'] == 'ReturnStatement':
            value = self.evaluate(node['value'])
            return {'type': 'return', 'value': value}
        
        elif node['type'] == 'SpitFunction':
            # Handle both spit() and አውጣ() functions
            args = [self.evaluate(arg) for arg in node['arguments']]
            output = ' '.join(str(arg) for arg in args)
            print(output)
            return None
        
        elif node['type'] == 'UnaryOperation':
            operand = self.evaluate(node['operand'])
            operator = node['operator']
            
            if operator == '-':
                return -operand
            elif operator == 'not' or operator == 'ተቃራኒ':
                return not operand
            else:
                raise Exception(f"Unknown unary operator: {operator}")
        
        elif node['type'] == 'Factorial':
            value = self.evaluate(node['value'])
            if not isinstance(value, int) or value < 0:
                raise Exception("Factorial is only defined for non-negative integers")
            return math.factorial(value)
        
        else:
            raise Exception(f"Unknown node type: {node['type']}")