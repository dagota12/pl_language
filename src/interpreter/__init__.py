class Interpreter:
    def __init__(self):
        self.variables = {}

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
        elif node['type'] == 'Number':
            return int(node['value'])
        elif node['type'] == 'Identifier':
            if node['value'] in self.variables:
                return self.variables[node['value']]
            else:
                raise Exception(f"Undefined variable: {node['value']}")
        else:
            raise Exception(f"Unknown node type: {node['type']}")