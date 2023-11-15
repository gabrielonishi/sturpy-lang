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
%token IF WHILE FUNCTION PRINT INPUT TYPE IDENTIFIER NUMBER EQ GT LT OR AND PLUS MINUS MULT DIV NOT COLON COMMA BREAKLINE TAB SPACEBAR OPEN_PARENTHESIS CLOSE_PARENTHESIS

%start program

%%

program : statements
    ;

statements : 
    statement BREAKLINE
    | statements statement BREAKLINE
    ;

statement :
    PRINT OPEN_PARENTHESIS bool_expression CLOSE_PARENTHESIS
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
    | PLUS factor
    | MINUS factor
    | NOT factor
    | OPEN_PARENTHESIS bool_expression CLOSE_PARENTHESIS
%%

/* Implement any necessary additional functions or actions */

int main() {
    yyparse();
    return 0;
}
