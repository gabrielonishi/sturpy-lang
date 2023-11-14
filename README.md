# SturPy - A versão resiliente do Python

## Visão Geral
Apesar de ser uma das linguagens mais utilizadas no mundo, o Python possui um problema. Ela é uma linguagem leniente - não há muita coisa que o compilador não aceite. O que parece uma benção para programadores iniciantes se transforma em um pesadelo à medida que um projeto escala. Com cada um escrevendo da sua própria maneira, o risco é acabar com um código remendado, pouco legível e, portanto, de difícil manutenção. Devido a isso, normas e boas práticas se tornaram de extremo valor para projetos complexos. Mas nunca houve uma forma de tornar isso obrigatório - até agora.

**SturPy** é uma linguagem de programação baseada em Python que introduz duas mudanças significativas:

 - **Tipagem Forte Exclusiva**: Em SturPy, todas as variáveis são exclusivamente fortemente tipadas. Isso significa que você deve declarar explicitamente o tipo de uma variável e, uma vez definido, esse tipo não pode ser alterado.

 - **Formatação Obrigatória**: A formatação do documento é parte da própria linguagem SturPy. Baseado nas normas PEP8 (Python Enhancement Proposal 8), todo o código compilável é um código bem escrito.

## Exemplo - Soma de Pares

```python

def sum_of_evens(n: int) -> int:
    total : int = 0
    i : int = 2
    while i <= n:
        total = total + i
        i = i + 2
    return total

n : int = input()

result = sum_of_evens(n)
print(f"The sum of even numbers from 1 to {n} is {result}")
```

## EBNF

```
EXPLANATION = "'''", "\n", {LETTER | "\n" | DIGIT}, "\n", "'''"
PROGRAM = EXPLANATION, {STATEMENT} ;
BLOCK = "\n", {"\t", STATEMENT}, "\n" ;

STATEMENT = ( λ | PRINT | ASSIGNMENT | PRINT | IF | WHILE | FUNCTION), "\n" ;

IF = "if", " ", BOOL_EXPRESSION, ":", BLOCK ;
WHILE = "while", " ", BOOL_EXPRESSION, ":", BLOCK ;
FUNCTION = "def", " ", FUNCTION_NAME, "(", IDENTIFIER, ":", VARTYPE {",", IDENTIFIER, ":", VARTYPE}, ")", " ", "->", " ", VARTYPE, ":", BLOCK ;

ASSIGNMENT = IDENTIFIER, " ", ":", " ", VARTYPE, " ", "=", " ", BOOL_EXPRESSSION ;

BOOL_EXPRESSION = BOOL_TERM , { "or", BOOL_TERM } ;
BOOL_TERM = RELATION_EXPRESSION , { "and", RELATION_EXPRESSION } ;
RELATION_EXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION } ;

EXPRESSION = TERM, { ("+" | "-" ), TERM } ;
TERM = FACTOR , { ("*" | "/"), FACTOR } ;
FACTOR = NUMBER | IDENTIFIER | (("+" | "-" | "!"), FACTOR) | "(", BOOL_EXPRESSION, ")" | INPUT;

VARTYPE = "int" | "str" | "bool"
INPUT = "input", "(", ")"
PRINT = "print", "(", BOOL_EXPRESSION, ")" ;

IDENTIFIER = LETTER, {LETTER, "_"}
FUNCTION_NAME = LOWERCASE_LETTER, { LOWERCASE_LETTER | UNDERSCORE } ;
NUMBER = DIGIT, { DIGIT } ;
LETTER = ( a | ... | z | A | ... | Z ) ;
LOWERCASE_LETTERS = (a | ... | z) ;
DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
```

## Rodando Flex (Análise Sintática)

```bash
    flex tokenizer.l
    gcc lex.yy.c -o lexer -lfl
    ./lexer input_file.txt
```
