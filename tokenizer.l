/* tokenizer.l */

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"
%}

%option noyywrap

%%

"\t"                         { printf("Token Identified: TAB\n"); return TAB; }
"\n"                         { printf("Token Identified: BREAKLINE\n"); return BREAKLINE; }
" "                          { printf("Token Identified: SPACEBAR\n"); return SPACEBAR; }
"("                          { printf("Token Identified: (\n"); return OPEN_PARENTHESIS; }
")"                          { printf("Token Identified: )\n"); return CLOSE_PARENTHESIS; }
"=="                         { printf("Token Identified: EQ\n"); return EQ; }
">"                          { printf("Token Identified: GT\n"); return GT; }
"<"                          { printf("Token Identified: LT\n"); return LT; }
"or"                         { printf("Token Identified: OR\n"); return OR; }
"and"                        { printf("Token Identified: AND\n"); return AND; }
"+"                          { printf("Token Identified: PLUS\n"); return PLUS; }
"-"                          { printf("Token Identified: MINUS\n"); return MINUS; }
"*"                          { printf("Token Identified: MULT\n"); return MULT; }
"/"                          { printf("Token Identified: DIV\n"); return DIV; }
"!"                          { printf("Token Identified: NOT\n"); return NOT; }
":"                          { printf("Token Identified: COLON\n"); return COLON; }
","                          { printf("Token Identified: COMMA\n"); return COMMA; }
"print"                      { printf("Token Identified: PRINT\n"); return PRINT; }
"if"                         { printf("Token Identified: IF\n"); return IF; }
"while"                      { printf("Token Identified: WHILE\n"); return WHILE; }
"def"                        { printf("Token Identified: FUNCTION\n"); return FUNCTION; }
"input"                      { printf("Token Identified: INPUT\n"); return INPUT; }
"int"|"string"|"bool"        { printf("Token Identified: TYPE: %s\n", yytext); return TYPE; }
[a-zA-Z][a-zA-Z0-9_]*        { printf("Token Identified: IDENTIFIER: %s\n", yytext); return IDENTIFIER; }
[0-9]+                       { printf("Token Identified: NUMBER: %s\n", yytext); return NUMBER; }
.                            { printf("Token Identified: TOKEN NÃO RECONHECIDO\n"); yyterminate(); }

%%

