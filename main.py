import sys

import prepro, tokens

if __name__ == '__main__':
    if(len(sys.argv)!=2):
        raise SystemError("Pass a .spy file as argument")
    
    filename = sys.argv[1]

    with open(file=filename, mode='r') as f:
        code_str = f.read()
    
    clean_code = prepro.PrePro.filter(code_str)    
    
    print(clean_code)

    tokenizer = tokens.Tokenizer(clean_code)
    tokenizer.select_next()
    while tokenizer.next.type != tokens.TokenType.EOF:
        print(repr(tokenizer.next.value), tokenizer.next.type)
        tokenizer.select_next()