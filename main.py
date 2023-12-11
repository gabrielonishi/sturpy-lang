import sys

import prepro

if __name__ == '__main__':
    if(len(sys.argv)!=2):
        raise SystemError("Pass a .spy file as argument")
    
    filename = sys.argv[1]

    with open(file=filename, mode='r') as f:
        code_str = f.read()
    
    print(code_str)
    print('*'*20)
    clean_code = prepro.PrePro.filter(code_str)
    print(clean_code)
