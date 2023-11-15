/* tokenizer.l */

%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "parser.tab.h"
%}

%option noyywrap

%%

"\t"                         { printf("Token Identified: IDENTATION\n"); return IDENTATION; }
"\n"                         { printf("Token Identified: BREAKLINE\n"); return BREAKLINE; }
"->"                         { printf("Token Identified: ARROW\n"); return ARROW; }
"("                          { printf("Token Identified: (\n"); return OPEN_PARENTHESIS; }
")"                          { printf("Token Identified: )\n"); return CLOSE_PARENTHESIS; }
"=="                         { printf("Token Identified: EQ\n"); return EQ; }
"="                          { printf("Token Identified: ATTRIBUTE\n"); return ATTRIBUTE;}
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
"'"                          { printf("Token Identified: QUOTE\n"); return QUOTE; }
"print"                      { printf("Token Identified: PRINT\n"); return PRINT; }
"if"                         { printf("Token Identified: IF\n"); return IF; }
"while"                      { printf("Token Identified: WHILE\n"); return WHILE; }
"def"                        { printf("Token Identified: DEF_FUNC\n"); return DEF_FUNC; }
"input"                      { printf("Token Identified: INPUT\n"); return INPUT; }
"int"|"string"|"bool"        { printf("Token Identified: TYPE: %s\n", yytext); return TYPE; }
[a-z_][a-z0-9_]*             { printf("Token Identified: LOWERCASE_IDENTIFIER %s\n", yytext); return LOWERCASE_IDENTIFIER; }
[a-zA-Z][a-zA-Z0-9_]*        { printf("Token Identified: UPPERCASE_IDENTIFIER %s\n", yytext); return UPPERCASE_IDENTIFIER; }
[0-9]+                       { printf("Token Identified: NUMBER %s\n", yytext); return NUMBER; }
" "                          {}
.                            { printf("Token Identified: TOKEN NÃO RECONHECIDO\n"); yyterminate(); }

%%

