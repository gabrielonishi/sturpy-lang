with open("program.txt", 'r') as f:
    lines = f.readlines()

for line in lines:
    print(repr(line))