from enum import Enum, auto

class VarType(Enum):
    INT = auto()
    STRING = auto()


class SymbolTable():
    '''
    Serve como memória do compilador, associando idenitfier à
    variáveis

    Pode existir mais de uma symbol_table (uma para a main e 
    outras para o escopo de funções)

    self.symbol_table = 
    {
        identifier1 = (value, type), 
        identifier2 = (value, type),
        ...
    }
    '''

    def __init__(self):
        self.symbol_table = {}

    def get(self, identifier):

        if identifier not in self.symbol_table:
            raise ValueError(
                f'ERRO EM SymbolTable: Variável {identifier} sem atribuição')

        return self.symbol_table[identifier]

    def set(self, identifier, value, var_type: VarType) -> None:
        if identifier not in list(self.symbol_table.keys()):
            raise ValueError("Tenta mudar variável antes de declará-la")
        last_value, last_type = self.symbol_table[identifier]
        if last_type != var_type:
            raise ValueError("Tenta mudar tipo de variável")
        self.symbol_table[identifier] = (value, var_type)

    def create_empty(self, identifier: str, declared_var_type: VarType) -> None:
        if identifier in self.symbol_table:
            raise ValueError("Não se pode criar um mesmo identifier 2 vezes")

        self.symbol_table[identifier] = (None, declared_var_type)

    def create(self, identifier: str, variable: tuple, declared_var_type: VarType) -> None:
        variable_value, variable_type = variable
        if variable_type != declared_var_type:
            raise ValueError(
                "Tipo declarado da variável é diferente do tipo da variável")
        self.symbol_table[identifier] = variable

    def get_table(self):
        return self.symbol_table


class FuncTable():
    '''
    Classe estática que serve como memória do compilador, 
    associando nome da função com o seu nó e tipo
    
    Só existe uma func_table por programa

    self.func_table = 
    {
        func1 = (func_dec_node1, type1),
        func2 = (func_dec_node2, type2),
        ...
    }
    '''

    func_table = dict()
    
    @staticmethod
    def get(function_name:str) -> tuple:
        if function_name not in FuncTable.func_table:
            raise ValueError(f'Tenta pegar função que não foi previamente declarada')
        
        return FuncTable.func_table[function_name]
    
    @staticmethod
    def set(function_name:str, func_dec_node, function_type:VarType) -> None:
        if function_name in FuncTable.func_table:
            raise ValueError(f'Tenta criar mesma função duas vezes')
                
        FuncTable.func_table[function_name] = (func_dec_node, function_type)