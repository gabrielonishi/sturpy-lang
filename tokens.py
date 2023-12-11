from enum import Enum, auto

class TokenType(Enum):
    '''
    Classe para armazenar o tipo de token como uma variável
    '''
    EOF = auto()
    INT = auto()
    FIRST_ORDER_OPERATIONS = auto()
    SECOND_ORDER_OPERATIONS = auto()
    PARENTHESIS = auto()
    BRACKETS = auto()
    BREAKLINE = auto()
    ATTRIBUTE = auto()
    PRINT = auto()
    IDENTIFIER = auto()
    NUMERIC_COMPARISON = auto()
    NOT = auto()
    BOOL_OPERATION = auto()
    SCANLN = auto()
    IF = auto()
    FOR = auto()
    ELSE = auto()
    SEMICOLON = auto()
    COLON = auto()
    STRING = auto()
    VAR_DECLARATION = auto()
    VAR_TYPE = auto()
    RETURN = auto()
    FUNC = auto()

class Token:
    '''
    Encapsula informações definidoras de um token
    '''

    def __init__(self, value: [int, str], type: TokenType) -> None:
        self.value = value
        self.type = type

class Tokenizer:
    '''
    Transforma uma sequência de caracteres em tokens
    Análise léxica do programa
    Println(x) da expressão, alterando a posição de análise
    '''

    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.next = None
    
    def handle_operators(self, next_character: str) -> None:
        if next_character == '-':
            self.next = Token(value='-', type=TokenType.FIRST_ORDER_OPERATIONS)
        elif next_character == '+':
            self.next = Token(value='+', type=TokenType.FIRST_ORDER_OPERATIONS)
        elif next_character == '*':
            self.next = Token(
                value='*', type=TokenType.SECOND_ORDER_OPERATIONS)
        elif next_character == '/':
            self.next = Token(
                value='/', type=TokenType.SECOND_ORDER_OPERATIONS)
        elif next_character == '(':
            self.next = Token(value='(', type=TokenType.PARENTHESIS)
        elif next_character == ')':
            self.next = Token(value=')', type=TokenType.PARENTHESIS)
        elif next_character == '\n':
            self.next = Token(value='\n', type=TokenType.LINEFEED)
        elif next_character == '>':
            self.next = Token(value='>', type=TokenType.NUMERIC_COMPARISON)
        elif next_character == '<':
            self.next = Token(value='<', type=TokenType.NUMERIC_COMPARISON)
        elif next_character == '!':
            self.next = Token(value='!', type=TokenType.NOT)
        elif next_character == '{':
            self.next = Token(value='{', type=TokenType.BRACKETS)
        elif next_character == '}':
            self.next = Token(value='}', type=TokenType.BRACKETS)
        elif next_character == ';':
            self.next = Token(value=';', type=TokenType.SEMICOLON)
        elif next_character == ',':
            self.next = Token(value=',', type=TokenType.COLON)
        elif next_character == '.':
            self.next = Token(value='.', type=TokenType.FIRST_ORDER_OPERATIONS)
        elif next_character == '=':
            if self.source[self.position + 1] == '=':
                self.next = Token(
                    value='==', type=TokenType.NUMERIC_COMPARISON)
                self.position += 1
            else:
                self.next = Token(value='=', type=TokenType.ATTRIBUTE)
        elif next_character == '&':
            if self.source[self.position + 1] == '&':
                self.next = Token(value='&&', type=TokenType.BOOL_OPERATION)
                self.position += 1
            else:
                raise ValueError(
                    "ERRO EM Tokenizer.select_next(): '&' não é um operador válido. Você quis dizer '&&'?")
        elif next_character == '|':
            if self.source[self.position + 1] == '|':
                self.next = Token(value='||', type=TokenType.BOOL_OPERATION)
                self.position += 1
            else:
                raise ValueError(
                    "ERRO EM Tokenizer.select_next(): '|' não é um operador válido. Você quis dizer '||'?")
        self.position += 1

    def handle_reserved_keywords(self, key_word) -> None:
        if key_word == 'Println':
            self.next = Token(value='Println', type=TokenType.PRINT)
        elif key_word == 'Scanln':
            self.next = Token(value='Scanln', type=TokenType.SCANLN)
        elif key_word == 'if':
            self.next = Token(value='if', type=TokenType.IF)
        elif key_word == 'for':
            self.next = Token(value='for', type=TokenType.FOR)
        elif key_word == 'else':
            self.next = Token(value='else', type=TokenType.ELSE)
        elif key_word == 'var':
            self.next = Token(value='var', type=TokenType.VAR_DECLARATION)
        elif key_word == 'string':
            self.next = Token(value=VarType.STRING, type=TokenType.VAR_TYPE)
        elif key_word == 'int':
            self.next = Token(value=VarType.INT, type=TokenType.VAR_TYPE)
        elif key_word == 'return':
            self.next = Token(value='return', type=TokenType.RETURN)
        elif key_word == 'func':
            self.next = Token(value='func', type=TokenType.FUNC)

    def select_next(self) -> None:
        '''Lê o próximo token e atualiza o atributo next'''
        if len(self.source) == self.position:
            self.next = Token(value='EOF', type=TokenType.EOF)
            return
        next_character = self.source[self.position]
        if next_character in Tokenizer.OPERATORS:
            self.handle_operators(next_character=next_character)
        elif next_character.isdigit():
            this_value = ''
            while self.position != len(self.source) and self.source[self.position].isdigit():
                this_value += self.source[self.position]
                self.position += 1
            self.next = Token(value=int(this_value), type=TokenType.INT)
        elif next_character == '"':
            this_string = ''
            self.position += 1
            while self.position != len(self.source) and self.source[self.position] != '"':
                this_string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token(value=this_string, type=TokenType.STRING)
        elif next_character.isalpha():
            this_identifier = ''
            while self.position != len(self.source) and (self.source[self.position].isalnum() or
                                                         self.source[self.position] == '_'):
                this_identifier += self.source[self.position]
                self.position += 1
            if (this_identifier in Tokenizer.RESERVED_KEYWORDS):
                self.handle_reserved_keywords(key_word=this_identifier)
            else:
                self.next = Token(value=this_identifier,
                                  type=TokenType.IDENTIFIER)
        elif next_character.isspace():
            self.position += 1
            self.select_next()
        else:
            raise ValueError(
                f"TOKENIZER ERRO: Caractere {next_character} não esperado na posição {self.position}")
