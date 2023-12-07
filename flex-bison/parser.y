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
%token QUOTE ATTRIBUTE ARROW IF WHILE DEF_FUNC PRINT INPUT TYPE LOWERCASE_IDENTIFIER UPPERCASE_IDENTIFIER NUMBER EQ GT LT OR AND PLUS MINUS MULT DIV NOT COLON COMMA BREAKLINE IDENTATION SPACEBAR OPEN_PARENTHESIS CLOSE_PARENTHESIS

%start program

%%

program : 
    statements
    ;

block :
    BREAKLINE
    | BREAKLINE idented_statements
    ;

statements : 
    statement BREAKLINE
    | statements statement BREAKLINE
    ;

idented_statements :
    identations statement BREAKLINE
    | idented_statements identations statement BREAKLINE
    ;

identations :
    IDENTATION
    | identations IDENTATION
    ;

statement :
    /* vazio (λ) */ 
    | PRINT OPEN_PARENTHESIS bool_expression CLOSE_PARENTHESIS
    | assignment
    | IF bool_expression COLON block 
    | WHILE bool_expression COLON block
    | DEF_FUNC LOWERCASE_IDENTIFIER OPEN_PARENTHESIS arguments CLOSE_PARENTHESIS ARROW TYPE COLON block
    ;

assignment :
    LOWERCASE_IDENTIFIER COLON TYPE ATTRIBUTE bool_expression
    | LOWERCASE_IDENTIFIER ATTRIBUTE bool_expression

arguments :
    /* vazio λ */
    | LOWERCASE_IDENTIFIER COLON TYPE
    | arguments COMMA LOWERCASE_IDENTIFIER COLON TYPE
    ;

bool_expression :
    bool_term
    | bool_expression OR bool_term
    ;

bool_term :
    relation_expression
    | bool_term AND relation_expression
    ;

relation_expression :
    expression 
    | relation_expression EQ expression
    | relation_expression GT expression 
    | relation_expression LT expression
    ;

expression :
    term
    | expression PLUS term
    | expression MINUS term
    ;

term :
    factor
    | term MULT factor
    | term DIV factor
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
