%{
#include <stdio.h>
#include <stdlib.h>
%}

%option noyywrap

%%

 "\t"                         { printf("TAB"); return TAB; }
 "\n"                         { printf("BREAKLINE"); return BREAKLINE; }
 " "                          { printf("SPACEBAR"); return SPACEBAR; }
 "("                          { printf("("); return OPEN_PARENTHESIS; }
 ")"                          { printf(")"); return CLOSE_PARENTHESIS; }
 "=="                         { printf("EQ\n"); return EQ; }
 ">"                          { printf("GT\n"); return GT; }
 "<"                          { printf("LT\n"); return LT; }
 "or"                         { printf("OR\n"); return OR; }
 "and"                        { printf("AND\n"); return AND; }
 "+"                          { printf("PLUS\n"); return PLUS; }
 "-"                          { printf("MINUS\n"); return MINUS; }
 "*"                          { printf("MULT\n"); return MULT; }
 "/"                          { printf("DIV\n"); return DIV; }
 "!"                          { printf("NOT\n"); return NOT; }
 ":"                          { printf("COLON\n"); return COLON; }
 ","                          { printf("COMMA\n"); return COMMA; }
 "print"                      { printf("PRINT"); return PRINT; }
 "if"                         { printf("IF\n"); return IF; }
 "while"                      { printf("WHILE\n"); return WHILE; }
 "def"                        { printf("FUNCTION\n"); return FUNCTION; }
 "input"                      { printf("INPUT"); return INPUT; }
 "int"|"string"|"bool"        { yylval.strval = strdup(yytext); printf("TYPE: %s\n", yytext); return TYPE; }
 [a-zA-Z][a-zA-Z0-9_]*        { yylval.strval = strdup(yytext); printf("IDENTIFIER: %s\n", yytext); return IDENTIFIER; }
 [0-9]+                       { yylval.intval = atoi(yytext); printf("NUMBER: %s\n", yytext); return NUMBER; }
 .                            { printf("TOKEN NÃO RECONHECIDO\n"); yyterminate(); }
%%