flex tokenizer.l
bison -d -t parser.y
gcc -o analyzer parser.tab.c lex.yy.c -lfl