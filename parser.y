%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yylex();

void yyerror(const char *s) {
    fprintf(stderr, "Parser error: %s\n", s);
}
%}

/* Token definitions */
%token ATTRIBUTE ARROW IF WHILE DEF_FUNC PRINT INPUT TYPE LOWERCASE_IDENTIFIER UPPERCASE_IDENTIFIER NUMBER EQ GT LT OR AND PLUS MINUS MULT DIV NOT COLON COMMA BREAKLINE IDENTATION SPACEBAR OPEN_PARENTHESIS CLOSE_PARENTHESIS

%start program

%%

program : 
    statements
    ;

block :
    BREAKLINE idented_statements BREAKLINE
    ;

statements : 
    BREAKLINE
    | statement BREAKLINE
    | statements statement BREAKLINE
    ;

idented_statements :
    IDENTATION statement BREAKLINE
    | IDENTATION idented_statements statement BREAKLINE
    ;

statement :
    /* vazio (λ) */ 
    | PRINT OPEN_PARENTHESIS bool_expression CLOSE_PARENTHESIS
    | LOWERCASE_IDENTIFIER COLON TYPE ATTRIBUTE bool_expression
    | IF bool_expression COLON block 
    | WHILE bool_expression COLON block
    | DEF_FUNC LOWERCASE_IDENTIFIER OPEN_PARENTHESIS arguments CLOSE_PARENTHESIS ARROW TYPE COLON block
    ;

arguments :
    /* vazio λ */
    | LOWERCASE_IDENTIFIER COLON TYPE
    | arguments COMMA LOWERCASE_IDENTIFIER COLON TYPE
    ;

bool_expression :
    bool_term
    | bool_term OR bool_term
    ;

bool_term :
    relation_expression
    | relation_expression AND relation_expression
    ;

relation_expression :
    expression 
    | expression EQ expression
    | expression GT expression 
    | expression LT expression
    ;

expression :
    term
    | term PLUS term
    | term MINUS term
    ;

term :
    factor
    | factor MULT factor
    | factor DIV factor
    ;

factor :
    NUMBER
    | LOWERCASE_IDENTIFIER
    | PLUS factor
    | MINUS factor
    | NOT factor
    | OPEN_PARENTHESIS bool_expression CLOSE_PARENTHESIS
    | INPUT OPEN_PARENTHESIS CLOSE_PARENTHESIS
%%

/* Implement any necessary additional functions or actions */

int main() {
    yyparse();
    return 0;
}
