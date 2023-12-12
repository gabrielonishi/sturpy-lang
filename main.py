import sys

import prepro, tokens, parse, nodes

if __name__ == '__main__':
    if(len(sys.argv)!=2):
        raise SystemError("Pass a .spy or a .🧱 file as argument")
    
    filename = sys.argv[1]

    extension = filename.split('.')[-1]

    if extension != '🧱' and extension != 'spy':
        print(extension)
        raise SystemError("Pass a .spy or a .🧱 file as argument")

    with open(file=filename, mode='r') as f:
        code_str = f.read()
    
    clean_code = prepro.PrePro.filter(code_str)    
    print(clean_code)    
    root = parse.Parser.run(clean_code)
    symbol_table = nodes.SymbolTable()
    root.evaluate(symbol_table=symbol_table)

    