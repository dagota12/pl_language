class ReturnValue:
    def __init__(self, value):
        self.value = value

class Function:
    def __init__(self, name, parameters, body, env):
        self.name = name
        self.parameters = parameters
        self.body = body
        self.env = env  # Capturing the environment (closure)

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}

    def evaluate(self, node):
        if node['type'] == 'Assignment':
            value = self.evaluate(node['value'])
            self.variables[node['identifier']] = value
            return value
        elif node['type'] == 'BinaryOperation':
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])
            if node['operator'] == '+':
                return left + right
            elif node['operator'] == '-':
                return left - right
            elif node['operator'] == '*':
                return left * right
            elif node['operator'] == '/':
                return left / right
        elif node['type'] == 'Comparison':
            left = self.evaluate(node['left'])
            right = self.evaluate(node['right'])
            if node['operator'] == '==':
                return left == right
            elif node['operator'] == '!=':
                return left != right
            elif node['operator'] == '<':
                return left < right
            elif node['operator'] == '<=':
                return left <= right
            elif node['operator'] == '>':
                return left > right
            elif node['operator'] == '>=':
                return left >= right
        elif node['type'] == 'IfStatement':
            condition_result = self.evaluate(node['condition'])
            if condition_result:
                return self.evaluate(node['true_branch'])
            elif node['false_branch']:
                return self.evaluate(node['false_branch'])
            return None
        elif node['type'] == 'Block':
            result = None
            for statement in node['statements']:
                result = self.evaluate(statement)
            return result
        elif node['type'] == 'WhileStatement':
            result = None
            # Safety counter to prevent infinite loops during testing
            max_iterations = 1000
            iteration_count = 0
            
            while self.evaluate(node['condition']):
                result = self.evaluate(node['body'])
                iteration_count += 1
                if iteration_count >= max_iterations:
                    raise Exception(f"Maximum iteration limit reached ({max_iterations}). Possible infinite loop detected.")
            return result
        elif node['type'] == 'FunctionDefinition':
            function = Function(
                node['name'],
                node['parameters'],
                node['body'],
                dict(self.variables)  # Capture current environment
            )
            self.functions[node['name']] = function
            return function
        elif node['type'] == 'ReturnStatement':
            value = self.evaluate(node['value'])
            return ReturnValue(value)
        elif node['type'] == 'FunctionCall':
            function_name = node['name']
            if function_name not in self.functions:
                raise Exception(f"Undefined function: {function_name}")
                
            function = self.functions[function_name]
            
            # Evaluate arguments
            arguments = [self.evaluate(arg) for arg in node['arguments']]
            
            if len(arguments) != len(function.parameters):
                raise Exception(f"Expected {len(function.parameters)} arguments but got {len(arguments)}")
            
            # Save current environment
            saved_variables = dict(self.variables)
            
            # Set up function environment
            self.variables = dict(function.env)
            
            # Bind parameters to arguments
            for param, arg in zip(function.parameters, arguments):
                self.variables[param] = arg
                
            # Execute function body
            result = self.evaluate(function.body)
            
            # Check if the result is a return value
            if isinstance(result, ReturnValue):
                result = result.value
                
            # Restore environment
            self.variables = saved_variables
            
            return result
        elif node['type'] == 'Number':
            return int(node['value'])
        elif node['type'] == 'Identifier':
            if node['value'] in self.variables:
                return self.variables[node['value']]
            else:
                raise Exception(f"Undefined variable: {node['value']}")
        else:
            raise Exception(f"Unknown node type: {node['type']}")