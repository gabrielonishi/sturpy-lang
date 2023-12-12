import tokens
import nodes


class Parser:
    '''
    Classe estática que analisa a estrutura da expressão e realiza operações.
    Análise sintática do programa
    '''
    tokenizer = None

    NO_CHILDREN = list()

    @staticmethod
    def run(code: str) -> nodes.Node:
        '''
        Creates Abstract Syntax Tree
        '''
        Parser.tokenizer = tokens.Tokenizer(source=code)
        Parser.tokenizer.select_next()
        ast = Parser.parse_program()
        if Parser.tokenizer.next.type != tokens.TokenType.EOF:
            raise SyntaxError("Did not consume whole code")
        return ast

    @staticmethod
    def parse_program() -> nodes.Node:
        statements = list()
        while (Parser.tokenizer.next.type != tokens.TokenType.EOF):
            if Parser.tokenizer.next.type == tokens.TokenType.DEF_FUNC:
                statements.append(Parser.parse_declaration())
            else:
                statements.append(Parser.parse_statement())

        return nodes.Program(value=None, children=statements)

    @staticmethod
    def parse_declaration() -> nodes.Node:
        if Parser.tokenizer.next.type != tokens.TokenType.DEF_FUNC:
            raise SyntaxError("Function declaration must begin with 'def'")
        Parser.tokenizer.select_next()

        if Parser.tokenizer.next.type != tokens.TokenType.IDENTIFIER:
            raise SyntaxError(
                f"Expected function identifier, instead got {Parser.tokenizer.next.type}")
        
        func_identifier = Parser.tokenizer.next.value
        func_identifier_node = nodes.Identifier(value=func_identifier, children=Parser.NO_CHILDREN)
        Parser.tokenizer.select_next()

        if Parser.tokenizer.next.value != "(":
            raise SyntaxError(
                f"Didn't open parenthesis after {func_identifier}")
        
        Parser.tokenizer.select_next()
        arg_nodes = list()
        while Parser.tokenizer.next.value != ')':
            if Parser.tokenizer.next.type != tokens.TokenType.IDENTIFIER:
                raise SyntaxError(
                    f"Problem in argument declaration in {func_identifier}")
            
            arg_identifier = Parser.tokenizer.next.value
            arg_identifier_node = nodes.Identifier(value=arg_identifier, children=list())
        
            Parser.tokenizer.select_next()

            if Parser.tokenizer.next.type != tokens.TokenType.COLON:
                raise SyntaxError("Argument in function must be followed by colon (':')")
            Parser.tokenizer.select_next()

            if Parser.tokenizer.next.type != tokens.TokenType.VAR_TYPE:
                raise SyntaxError(
                    f"Doesn't specify type for {arg_identifier} em {func_identifier}")
            
            arg_tipo = Parser.tokenizer.next.value
            arg_var_dec = nodes.VarDec(
                arg_tipo, children=[arg_identifier_node])
            arg_nodes.append(arg_var_dec)
            Parser.tokenizer.select_next()

            if (Parser.tokenizer.next.type == tokens.TokenType.COLON):
                Parser.tokenizer.select_next()
            elif (Parser.tokenizer.next.value == ")"):
                break
            else:
                raise SyntaxError(
                    f"Declaração errada de func {func_identifier}")
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != tokens.TokenType.ARROW:
            raise SyntaxError("Did not use arrow (->) to specify function return type")
        Parser.tokenizer.select_next()
        if (Parser.tokenizer.next.type != tokens.TokenType.VAR_TYPE):
            raise SyntaxError(
                f'Não manda tipo da variável ao declarar {arg_identifier}')
        
        func_return_type = Parser.tokenizer.next.value
        func_name_var_dec = nodes.VarDec(value=func_return_type, children=[func_identifier_node])
        Parser.tokenizer.select_next()

        if Parser.tokenizer.next.type != tokens.TokenType.COLON:
            raise ValueError("Function declaration must end with colon (':')")
        Parser.tokenizer.select_next()
        func_block = Parser.parse_block()

        if Parser.tokenizer.next.type != tokens.TokenType.BREAKLINE:
            raise SyntaxError("Não pula linha após block")
        
        Parser.tokenizer.select_next()
        func_node = nodes.FuncDec(value=None, children=[func_name_var_dec, func_block])

        for node in arg_nodes:
            func_node.children.append(node)
            
        return func_node

    @staticmethod
    def parse_statement() -> nodes.Node:
        if Parser.tokenizer.next.type == tokens.TokenType.PRINT:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.value != "(":
                raise SyntaxError(
                    "Doesn't open parentheses for print")
            Parser.tokenizer.select_next()
            expression = Parser.parse_bool_expression()
            if Parser.tokenizer.next.value != ")":
                raise SyntaxError(
                    "Doens't close parentheses for print")
            Parser.tokenizer.select_next()
            statement = nodes.Print(value=None, children=[expression])

        elif (Parser.tokenizer.next.type == tokens.TokenType.IF):
            Parser.tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type != tokens.TokenType.COLON:
                raise SyntaxError("End of if statement must have colon (:)")
            Parser.tokenizer.select_next()
            if_block = Parser.parse_block()
            if Parser.tokenizer.next.type == tokens.TokenType.ELSE:
                Parser.tokenizer.select_next()
                else_block = Parser.parse_block()
                statement = nodes.If(value=None, children=[
                                     condition, if_block, else_block])
            else:
                statement = nodes.If(value=None, children=[
                                     condition, if_block])

        elif (Parser.tokenizer.next.type == tokens.TokenType.WHILE):
            Parser.tokenizer.select_next()
            condition = Parser.parse_bool_expression()
            if Parser.tokenizer.next.type != tokens.TokenType.COLON:
                SyntaxError('While statements must end with colon')
            Parser.tokenizer.select_next()
            block = Parser.parse_block()
            statement = nodes.While(value=None, children=[condition, block])

        elif (Parser.tokenizer.next.type == tokens.TokenType.RETURN):
            Parser.tokenizer.select_next()
            bool_expression = Parser.parse_bool_expression()
            statement = nodes.Return(value=None, children=[bool_expression])
        elif (Parser.tokenizer.next.type == tokens.TokenType.IDENTIFIER):
            statement = Parser.parse_assign()
        else:
            SyntaxError(
                f'Value {repr(Parser.tokenizer.next.value)} not expected')
        if Parser.tokenizer.next.type == tokens.TokenType.BREAKLINE:
            Parser.tokenizer.select_next()
        else:
            raise SyntaxError(
                f'ERRO EM parse_statement(): Valor {repr(Parser.tokenizer.next.value)} não esperado na posição {Parser.tokenizer.position}'
            )
        return statement
    
    @staticmethod
    def parse_block() -> nodes.Node:
        if Parser.tokenizer.next.value != "{":
            raise SyntaxError(
                "ERRO EM Parser.parse_block(): É necessário começar um novo bloco com '{'")
        Parser.tokenizer.select_next()
        if Parser.tokenizer.next.type != tokens.TokenType.BREAKLINE:
            raise SyntaxError(
                "ERRO EM Parser.parse_block(): É necessário um linebreak depois de '{'")
        Parser.tokenizer.select_next()
        block = nodes.Block(value=None, children=Parser.NO_CHILDREN)
        statements = list()
        while Parser.tokenizer.next.value != "}":
            statement = Parser.parse_statement()
            statements.append(statement)
        block = nodes.Block(value=None, children=statements)
        if Parser.tokenizer.next.value != "}":
            raise SyntaxError(
                "ERRO EM Parser.parse_block(): Não fechou bloco com '}'")
        Parser.tokenizer.select_next()
        return block

    @staticmethod
    def parse_bool_expression() -> nodes.Node:
        bool_expression = Parser.parse_bool_term()

        while Parser.tokenizer.next.value == "or":
            Parser.tokenizer.select_next()
            other_bool_term = Parser.parse_bool_term()
            if other_bool_term is None:
                raise SyntaxError(
                    'Or clause must be followed by another bool expression')
            bool_expression = nodes.BinOp(
                value='or', children=[bool_expression, other_bool_term])

        return bool_expression

    @staticmethod
    def parse_bool_term() -> nodes.Node:
        bool_term = Parser.parse_relation_expression()
        while Parser.tokenizer.next.value == "and":
            Parser.tokenizer.select_next()
            other_relation_expression = Parser.parse_relation_expression()
            if other_relation_expression is None:
                raise SyntaxError(
                    'And clause must be followed by another relation expression')
            bool_term = nodes.BinOp(value='and', children=[
                                    bool_term, other_relation_expression])

        return bool_term

    @staticmethod
    def parse_relation_expression() -> nodes.Node:
        relation_expression = Parser.parse_expression()

        while Parser.tokenizer.next.type == tokens.TokenType.NUMERIC_COMPARISON:
            if Parser.tokenizer.next.value == "==":
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                relation_expression = nodes.BinOp(
                    value='==', children=[relation_expression, other_expression])
            elif Parser.tokenizer.next.value == ">":
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                relation_expression = nodes.BinOp(
                    value='>', children=[relation_expression, other_expression])
            elif Parser.tokenizer.next.value == "<":
                Parser.tokenizer.select_next()
                other_expression = Parser.parse_expression()
                relation_expression = nodes.BinOp(
                    value='<', children=[relation_expression, other_expression])
        return relation_expression
    
    @staticmethod
    def parse_expression():
        term = Parser.parse_term()
        while Parser.tokenizer.next.type == tokens.TokenType.FIRST_ORDER_OPERATIONS:
            if Parser.tokenizer.next.value == '-':
                Parser.tokenizer.select_next()
                other_term = Parser.parse_term()
                term = nodes.BinOp(value='-', children=[term, other_term])
            elif Parser.tokenizer.next.value == '+':
                Parser.tokenizer.select_next()
                other_term = Parser.parse_term()
                term = nodes.BinOp(value='+', children=[term, other_term])
        return term
    
    @staticmethod
    def parse_term() -> nodes.Node:
        factor = Parser.parse_factor()
        while Parser.tokenizer.next.type == tokens.TokenType.SECOND_ORDER_OPERATIONS:
            if Parser.tokenizer.next.value == '*':
                Parser.tokenizer.select_next()
                other_factor = Parser.parse_factor()
                factor = nodes.BinOp(
                    value='*', children=[factor, other_factor])
            elif Parser.tokenizer.next.value == '/':
                Parser.tokenizer.select_next()
                other_factor = Parser.parse_factor()
                factor = nodes.BinOp(
                    value='/', children=[factor, other_factor])
        return factor
    
    @staticmethod
    def parse_factor() -> nodes.Node:
        if Parser.tokenizer.next.type == tokens.TokenType.INT:
            factor = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            node = nodes.IntVal(factor, Parser.NO_CHILDREN)
            return node
        elif Parser.tokenizer.next.type == tokens.TokenType.STRING:
            string = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            node = nodes.StringVal(string, Parser.NO_CHILDREN)
            return node
        elif Parser.tokenizer.next.value == "-":
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('-', [factor])
            return node
        elif Parser.tokenizer.next.value == "+":
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('+', [factor])
            return node
        elif Parser.tokenizer.next.type == tokens.TokenType.NOT:
            Parser.tokenizer.select_next()
            factor = Parser.parse_factor()
            node = nodes.UnOp('!', children=[factor])
            return node
        elif Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()
            expression = Parser.parse_bool_expression()
            if Parser.tokenizer.next.value == ")":
                Parser.tokenizer.select_next()
                return expression
            else:
                raise SyntaxError(
                    f'Doesn\'t close parentheses for expression {expression}')
        elif Parser.tokenizer.next.type == tokens.TokenType.IDENTIFIER:
            identifier = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.value == '(':
                Parser.tokenizer.select_next()
                args_list = list()
                while Parser.tokenizer.next.value != ')':
                    arg = Parser.parse_bool_expression()
                    args_list.append(arg)
                    if Parser.tokenizer.next.value == ',':
                        Parser.tokenizer.select_next()
                        continue
                    elif Parser.tokenizer.next.value == ')':
                        break
                    else:
                        raise SyntaxError(f'Problema ao chamar {identifier}')
                Parser.tokenizer.select_next()
                return nodes.FuncCall(value=identifier, children=args_list)
            
            factor = nodes.Identifier(value=identifier, children=Parser.NO_CHILDREN)
            return factor
        
        elif Parser.tokenizer.next.type == tokens.TokenType.INPUT:
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.value != "(":
                raise SyntaxError(
                    'Doesn\'t open parentheses for input')
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.value != ")":
                raise SyntaxError(
                    'Doesn\'t close parentheses for input')
            Parser.tokenizer.select_next()
            node = nodes.Input(value=None, children=Parser.NO_CHILDREN)
            return node

    @staticmethod
    def parse_assign() -> nodes.Node:
        identifier = Parser.tokenizer.next.value
        identifier_node = nodes.Identifier(value=identifier, children=Parser.NO_CHILDREN)
        Parser.tokenizer.select_next()
        
        if Parser.tokenizer.next.type == tokens.TokenType.COLON:  
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type != tokens.TokenType.VAR_TYPE:
                raise SyntaxError(
                    "Identifier declaration must have a type")
            var_type = Parser.tokenizer.next.value
            Parser.tokenizer.select_next()
            if Parser.tokenizer.next.type == tokens.TokenType.ATTRIBUTE: 
                Parser.tokenizer.select_next()
                bool_expression = Parser.parse_bool_expression()
                return nodes.VarDec(value=var_type, children=[identifier_node, bool_expression])
            else:
                return nodes.VarDec(value=var_type, children=[identifier_node])
        elif Parser.tokenizer.next.value == "=":
            Parser.tokenizer.select_next()
            bool_expression = Parser.parse_bool_expression()
            return nodes.Assignment(value=None, children=[identifier_node, bool_expression])

        elif Parser.tokenizer.next.value == "(":
            Parser.tokenizer.select_next()
            args_list = list()
            while Parser.tokenizer.next.value != ')':
                arg = Parser.parse_bool_expression()
                args_list.append(arg)
                if Parser.tokenizer.next.value == ',':
                    Parser.tokenizer.select_next()
                    continue
                elif Parser.tokenizer.next.value == ')':
                    Parser.tokenizer.select_next()
                    break
                else:
                    raise SyntaxError(f'Problem on {identifier_node} function call')
            return nodes.FuncCall(identifier, args_list)
        else:
            raise SyntaxError(f"Next value should be '=' or '(', instead is {Parser.tokenizer.next.type})")