with open ('program.txt', 'r') as f:
    code_str = f.read()

lines = code_str.split('\n')

IDENTATION = '    '
identation_level = 0
line_identation = 0
clean_code = list()

for line in lines:
    line_identation = line.count(IDENTATION)
    line = line.strip(IDENTATION)

    if line.endswith(":"):
        identation_level += 1
        clean_code.append(line + '{')
        continue

    while line_identation < identation_level:
        identation_level -= 1
        clean_code.append('}')
    
    if line_identation == identation_level:
        clean_code.append(line)

print(clean_code)