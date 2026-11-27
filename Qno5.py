import re
import keyword

# Function to perform lexical analysis
def lexical_analyzer(code):

    pattern = r'//.*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|\d+\.\d+|\d+|[a-zA-Z_]\w*|==|!=|<=|>=|\+\+|--|[+\-*/%=<>!]=?|[(){};,]'

    tokens = re.findall(pattern, code)

    print("\nTOKEN\t\tCATEGORY")
    print("-" * 35)

    for token in tokens:

        if token.startswith("//") or token.startswith("/*"):
            continue

        elif token in keyword.kwlist or token in [
            "int", "float", "char", "double", "void",
            "if", "else", "while", "for", "return"
        ]:
            category = "Keyword"

        elif token.startswith(('"', "'")):
            category = "String Literal"

        elif re.fullmatch(r'\d+(\.\d+)?', token):
            category = "Constant"

        elif re.fullmatch(r'[a-zA-Z_]\w*', token):
            category = "Identifier"

        elif token in [
            "+", "-", "*", "/", "%", "=", "==",
            "!=", "<", ">", "<=", ">=", "++", "--",
            "+=", "-=", "*=", "/="
        ]:
            category = "Operator"

        elif token in "(){};,":
            category = "Separator"

        else:
            category = "Unknown"

        print(f"{token:<15} {category}")


# Main program
code = input("Enter source code: ")

lexical_analyzer(code)
