from tables import SymbolTable, FuncTable, VarType


class Node():
    '''
    Base class for nodes representing operations

    Attributes:
     - value: varies from node to node
     - children: list of nodes

    Methods: 
     - Evaluate(): varies from node to node
    '''

    def __init__(self, value, children: list):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        pass


class IntVal(Node):
    '''
    Integer Value - Represents an integer value

    value: Int

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return (self.value, VarType.INT)


class StringVal(Node):
    '''
    String Value - Represents a string

    value: String

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return (self.value, VarType.STRING)


class BinOp(Node):
    '''
    Binary Operation - can be +, -, *, /

    value: None

    children: 2 
     - children[0]: term 1
     - children[1]: term 2
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:

        left_term_value, left_term_type = self.children[0].evaluate(
            symbol_table)
        right_term_value, right_term_type = self.children[1].evaluate(
            symbol_table)

        ARITHIMETIC_OPERATORS = ['+', '-', '*', '/']
        BOOLEAN_OPERATORS = ['or', 'and']
        RELATIONAL_OPERATORS = ['>', '<', '==']

        if self.value in ARITHIMETIC_OPERATORS:
            if (left_term_type == VarType.STRING or right_term_type == VarType.STRING):
                raise ValueError(
                    "It is not possible to perform arithmetic operations involving strings")
            return_type = VarType.INT
            if self.value == '+':
                return_value = left_term_value + right_term_value
                return (return_value, return_type)
            elif self.value == '-':
                return_value = left_term_value - right_term_value
                return (return_value, return_type)
            elif self.value == '*':
                return_value = left_term_value * right_term_value
                return (return_value, return_type)
            elif self.value == '/':
                return_value = left_term_value // right_term_value
                return (return_value, return_type)

        elif self.value in BOOLEAN_OPERATORS:
            if (left_term_type != right_term_type):
                raise ValueError(
                    "It is not possible to perform boolean operations with different types")

            return_type = VarType.INT
            if self.value == 'or':
                return_value = left_term_value or right_term_value
                return (int(return_value), return_type)
            elif self.value == 'and':
                return_value = left_term_value and right_term_value
                return (int(return_value), return_type)

        elif self.value in RELATIONAL_OPERATORS:
            if (left_term_type != right_term_type):
                raise ValueError(
                    "It is not possible to perform boolean operations with different types")
            return_type = VarType.INT
            if self.value == '==':
                return_value = left_term_value == right_term_value
                return (int(return_value), return_type)
            elif self.value == '>':
                return_value = left_term_value > right_term_value
                return (int(return_value), return_type)
            elif self.value == '<':
                return_value = left_term_value < right_term_value
                return (int(return_value), return_type)

        else:
            raise ArithmeticError(
                f"Invalid operator {self.children[0]} {self.value} {self.children[1]}")


class UnOp(Node):
    '''
    Unary Operation - can be + or -

    value: None

    children: 1 (any type)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:

        term_value, term_type = self.children[0].evaluate(symbol_table)

        if self.value == '-':
            return_value = (-term_value, term_type)
            return return_value
        elif self.value == '+':
            return_value = (term_value, term_type)
            return return_value
        elif self.value == '!':
            return_value = (not term_value, term_type)
            return return_value


class Input(Node):
    '''
    Input variable from terminal

    value: None

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return (int(input()), VarType.INT)


class Assignment(Node):
    '''
    Represents a variable

    value: None

    children: 2
     - children[0] -> identifier
     - children[1] -> ast
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        variable = self.children[0].value
        ast_result_value, ast_type_value = self.children[1].evaluate(
            symbol_table)
        symbol_table.set(identifier=variable,
                         value=ast_result_value, var_type=ast_type_value)


class VarDec(Node):
    '''
    Variable Declaration - Adds a variable to the SymbolTable

    value: Variable type

    children: May have 1 or 2
     - children[0] -> Identifier Node
     - children[1] -> boolExpression
    '''

    def evaluate(self, symbol_table: SymbolTable) -> None:
        identifier_node = self.children[0]
        identifier = identifier_node.value
        declared_var_type = self.value
        if len(self.children) == 1:
            SymbolTable.create_empty(
                symbol_table, identifier=identifier, declared_var_type=declared_var_type)
        elif len(self.children) == 2:
            variable = self.children[1].evaluate(symbol_table)
            SymbolTable.create(symbol_table, identifier=identifier, variable=variable,
                               declared_var_type=declared_var_type)


class Identifier(Node):
    '''
    Variable to which a value is atributed

    value: any type

    children: []
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        return symbol_table.get(identifier=self.value)


class If(Node):
    '''
    Conditional

    value: None

    children: 2 or 3
     - children[0] -> condition
     - children[1] -> block to be executed if true
     - children[2] -> block to be executed in else (optional)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        condition = self.children[0]
        true_block = self.children[1]
        if condition.evaluate(symbol_table):
            true_block.evaluate(symbol_table)
        elif len(self.children) == 3:
            else_block = self.children[2]
            else_block.evaluate(symbol_table)


class While(Node):
    '''
    While Loop

    value: None

    children: 2
     - children[0] -> condition
     - children[1] -> block
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        condition = self.children[0]
        block = self.children[1]
        while condition.evaluate(symbol_table) == (1, VarType.INT):
            block.evaluate(symbol_table)


class FuncDec(Node):
    '''
    Represents components of a function

    value: None
    children: number of args + 2 children
     - children[0]: VarDec of the function name
     - children[1]: Block
     - children[n]: VarDec of the argument

    evaluate: Instantiate function in func_table
    '''

    def evaluate(self, symbol_table: SymbolTable) -> None:
        function_name_var_dec_node = self.children[0]
        function_type = function_name_var_dec_node.value
        function_name_identifier_node = function_name_var_dec_node.children[0]
        function_name = function_name_identifier_node.value

        FuncTable.set(function_name=function_name,
                      func_dec_node=self, function_type=function_type)


class FuncCall(Node):
    '''
    Represents a function call

    value: function name
    children: n (number of args passed in the call)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> Node:
        function_name = self.value
        func_dec_node, func_return_type = FuncTable.get(
            function_name=function_name)
        func_symbol_table = SymbolTable()

        if len(self.children) != len(func_dec_node.children) - 2:
            raise ValueError("Chama função com número errado de argumentos")

        for i in range(len(self.children)):
            # func_dec_node.children[0] é o nome da função
            # func_dec_node.children[1] é o bloco
            dec_arg_node = func_dec_node.children[i+2]
            # criar variáveis na symbol_table da função
            dec_arg_node.evaluate(func_symbol_table)
            arg_identifier = dec_arg_node.children[0].value
            # atribuir valor do argumento passado na nova st
            call_arg_node = self.children[i]
            arg_value, arg_type = call_arg_node.evaluate(symbol_table)
            func_symbol_table.set(identifier=arg_identifier,
                                  value=arg_value, var_type=arg_type)
        func_block_node = func_dec_node.children[1]
        retval = func_block_node.evaluate(func_symbol_table)
        if retval is not None:
            retval_value, retval_type = retval
            if retval_type != func_return_type:
                raise ValueError(
                    "Tenta retornar um valor de tipo diferente do tipo de retorno da função")
            else:
                return retval


class Return(Node):
    '''
    Returns within a function

    value: None
    children: bool_expression
    '''

    def evaluate(self, symbol_table: SymbolTable) -> Node:
        result_node = self.children[0]
        return result_node.evaluate(symbol_table)


class Block(Node):
    '''
    Block of instructions (for, if)

    value: None

    children: n (one per line with program instructions)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        for child in self.children:
            if isinstance(child, Return):
                return child.evaluate(symbol_table)
            child.evaluate(symbol_table)


class Program(Node):
    '''
    Represents the program as a whole. Should only be called
    once by the parser.

    value: None

    children: n (one per line with program instructions)
    '''

    def evaluate(self, symbol_table: SymbolTable) -> tuple:
        for statement in self.children:
            statement.evaluate(symbol_table)
