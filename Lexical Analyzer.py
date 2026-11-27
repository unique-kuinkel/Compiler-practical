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

# Theory:
# A Lexical Analyzer is the first phase of a compiler. It reads the source code character by character and converts it into a sequence of tokens.
# It is also known as a scanner. Its main function is to identify and classify tokens such as keywords, identifiers, operators, constants, and separators.
# Main functions of a Lexical Analyzer:
# 1.	Reads source code as input.
# 2.	Removes unnecessary whitespace and comments.
# 3.	Identifies different types of tokens.
# 4.	Classifies tokens into their respective categories.
# 5.	Detects invalid or unrecognized symbols.
# 6.	Passes the identified tokens to the syntax analyzer (parser).
# Types of Tokens:
# Token	Example
# Keyword	int, if, while
# Identifier	sum, number
# Operator	+, -, =, *
# Constant	10, 20, 3.14
# Separator	;, ,, (, )
# Example:
# For the source code:
# int sum = 10 + 20;
# The lexical analyzer generates:
# int      → Keyword
# sum      → Identifier
# =        → Operator
# 10       → Constant
# +        → Operator
# 20       → Constant
# ;        → Separator
# Algorithm:
# 1.	Start the program.
# 2.	Read the source code from the user.
# 3.	Define regular expressions for different token types.
# 4.	Scan the source code from left to right.
# 5.	Ignore whitespace and comments.
# 6.	Identify keywords and identifiers.
# 7.	Identify constants, operators, and separators.
# 8.	Classify each recognized token.
# 9.	Display the tokens along with their categories.
# 10.	Stop the program.

