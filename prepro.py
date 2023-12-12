class PrePro():
    '''
    Data pre-process
    '''

    @staticmethod
    def clean_comments(code_str: str) -> str:
        '''
        Removes comments
        '''
        clean_raw = ''
        i = 0
        while i < len(code_str):
            if code_str[i] == '#':
                while code_str[i] != '\n':
                    i += 1
                    if i == len(code_str):
                        break
                    
            else:
                clean_raw += code_str[i]
                i += 1

        return clean_raw

    @staticmethod
    def replace_indent_with_braces(code_str: str) -> str:
        IDENTATION = '    '
        identation_level = 0
        line_identation = 0
        clean_code = list()
        lines = code_str.split('\n')

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

        while identation_level > 0:
            identation_level -= 1
            clean_code.append('}')

    
        return '\n'.join(clean_code)
    
    @staticmethod
    def clear_lines(code_str:str) -> str:
        lines = code_str.split('\n')
        clean_code = list()
        for line in lines:
            if line != '':
                clean_code.append(line)
        
        return '\n'.join(clean_code) + '\n'

    @staticmethod
    def filter(source: str) -> str:
        '''
        Removes comments and adds "{" and "}"
        in place of identation
        '''

        no_comments_code = PrePro.clean_comments(source)
        braced_code = PrePro.replace_indent_with_braces(no_comments_code)
        clean_code = PrePro.clear_lines(braced_code)

        return clean_code
        