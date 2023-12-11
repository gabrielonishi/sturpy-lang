from enum import Enum, auto

class TokenType(Enum):
    '''
    Classe para armazenar o tipo de token como uma variável
    '''
    EOF = auto()
    INT = auto() # 1, 431, 31...
    FIRST_ORDER_OPERATIONS = auto() # +, -
    SECOND_ORDER_OPERATIONS = auto() # *, /
    NUMERIC_COMPARISON = auto() # >, <
    NOT = auto() # !
    ATTRIBUTE = auto() # =
    BOOL_OPERATION = auto() # and, or
    PARENTHESIS = auto() # (, )
    BRACKETS = auto() # {, }
    BREAKLINE = auto() # \n
    PRINT = auto() # print
    IDENTIFIER = auto() # x, string1, this_var...
    INPUT = auto() # input
    IF = auto() # if
    ELSE = auto() # else
    WHILE = auto() # for
    SEMICOLON = auto() # ;
    COLON = auto() # :
    COMMA = auto() # ,
    STRING = auto() # "this is a string"
    VAR_TYPE = auto() # int, str
    RETURN = auto() # return
    ARROW = auto() # ->
    DEF_FUNC = auto()

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
    
    def select_next(self) -> None:
        '''
        Seleciona o próximo token
        '''

        KEYWORDS = ['print', 'input', 'if', 'else', 'while', 'int', 'str', 'return', 'def']
        
        if(len(self.source) == self.position):
            self.next = Token(None, TokenType.EOF)
            return

        next_character = self.source[self.position]
        
        if next_character == '+':
            self.next = Token(next_character, TokenType.FIRST_ORDER_OPERATIONS)
            self.position += 1
            return
        elif next_character == '-':
            if self.source[self.position + 1] == '>':
                self.next = Token('->', TokenType.ARROW)
                self.position += 2
                return
            self.next = Token(next_character, TokenType.FIRST_ORDER_OPERATIONS)
            self.position += 1
            return
        elif next_character == '*' or next_character == '/':
            self.next = Token(next_character, TokenType.SECOND_ORDER_OPERATIONS)
            self.position += 1
            return
        elif next_character == '>' or next_character == '<':
            self.next = Token(next_character, TokenType.NUMERIC_COMPARISON)
            self.position += 1
            return
        elif next_character == '!':
            self.next = Token(next_character, TokenType.NOT)
            self.position += 1
            return
        elif next_character == '(' or next_character == ')':
            self.next = Token(next_character, TokenType.PARENTHESIS)
            self.position += 1
            return
        elif next_character == '{' or next_character == '}':
            self.next = Token(next_character, TokenType.BRACKETS)
            self.position += 1
            return
        elif next_character == '\n':
            self.next = Token(next_character, TokenType.BREAKLINE)
            self.position += 1
            return       
        elif next_character == ';':
            self.next = Token(next_character, TokenType.SEMICOLON)
            self.position += 1
            return
        elif next_character == ':':
            self.next = Token(next_character, TokenType.COLON)
            self.position += 1
            return 
        elif next_character == '=':
            if self.source[self.position + 1] == '=':
                self.next = Token('==', TokenType.NUMERIC_COMPARISON)
                self.position += 2
                return
            self.next = Token(next_character, TokenType.ATTRIBUTE)
            self.position += 1
            return
        elif next_character == '"':
            self.position += 1
            string = ''
            while self.source[self.position] != '"':
                string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token(string, TokenType.STRING)
            return
        elif next_character == "'":
            self.position += 1
            string = ''
            while self.source[self.position] != "'":
                string += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token(string, TokenType.STRING)
            return
        elif next_character == ',':
            self.next = Token(next_character, TokenType.COMMA)
            self.position += 1
            return
        elif next_character.isnumeric():
            number = ''
            while self.source[self.position].isnumeric():
                number += self.source[self.position]
                self.position += 1
            self.next = Token(int(number), TokenType.INT)
            return
        elif next_character.isalpha():
            identifier = ''
            while self.source[self.position].isalpha() or self.source[self.position].isnumeric() or self.source[self.position] == '_':
                identifier += self.source[self.position]
                self.position += 1
            match identifier:
                case 'print':
                    self.next = Token(identifier, TokenType.PRINT)
                    return
                case 'input':
                    self.next = Token(identifier, TokenType.INPUT)
                    return
                case 'if':
                    self.next = Token(identifier, TokenType.IF)
                    return
                case 'else':
                    self.next = Token(identifier, TokenType.ELSE)
                    return
                case 'while':
                    self.next = Token(identifier, TokenType.WHILE)
                    return
                case 'int':
                    self.next = Token(identifier, TokenType.VAR_TYPE)
                    return
                case 'str':
                    self.next = Token(identifier, TokenType.VAR_TYPE)
                    return
                case 'return':
                    self.next = Token(identifier, TokenType.RETURN)
                    return
                case 'def':
                    self.next = Token(identifier, TokenType.DEF_FUNC)
                    return
                case _:
                    self.next = Token(identifier, TokenType.IDENTIFIER)
                    return
        elif next_character.isspace():
            self.position += 1
            self.select_next()
        else:
            raise TypeError(f'Invalid character: {next_character}')