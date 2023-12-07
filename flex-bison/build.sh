flex tokenizer.l
bison -d -Wcounterexamples parser.y
gcc -o analyzer parser.tab.c lex.yy.c -lfl