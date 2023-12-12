import sys

import prepro, tokens, parse, nodes

if __name__ == '__main__':
    if(len(sys.argv)!=2):
        raise SystemError("Pass a .spy file as argument")
    
    filename = sys.argv[1]

    with open(file=filename, mode='r') as f:
        code_str = f.read()
    
    clean_code = prepro.PrePro.filter(code_str)    
    print(clean_code)    
    root = parse.Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)

    