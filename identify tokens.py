import re

# Read source code
with open("program.txt", "r") as file:
    code = file.read()

# Define token patterns
token_patterns = [
    ("Keyword", r"\b(int|float|char|double|void|if|else|while|for|return|do|break|continue)\b"),
    ("Identifier", r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"),
    ("Constant", r'"[^"]*"|\'[^\']*\'|\b\d+(\.\d+)?\b'),
    ("Operator", r"\+\+|--|==|!=|<=|>=|\+=|-=|\*=|/=|&&|\|\||[+\-*/%=<>!]"),
    ("Separator", r"[(){}\[\];,]"),
]

# Combine patterns into one regular expression
master_pattern = re.compile(
    "|".join(f"(?P<{name}>{pattern})" 
             for name, pattern in token_patterns)
)

# Display token table
print("{:<20} {:<20}".format("TOKEN", "CATEGORY"))
print("-" * 40)

for match in master_pattern.finditer(code):
    token = match.group()
    category = match.lastgroup

    print("{:<20} {:<20}".format(token, category))

# Theory:
# A token is the smallest meaningful unit of a program recognized by the lexical analyzer during the compilation process.
# The lexical analyzer (scanner) reads source code character by character, groups characters into meaningful sequences, and classifies them into different token categories.
# The major types of tokens are:
# 1.	Keywords: Reserved words with predefined meanings, e.g., if, else, while, int.
# 2.	Identifiers: Names used for variables, functions, and classes, e.g., sum, total.
# 3.	Operators: Symbols used to perform operations, e.g., +, -, *, /, =.
# 4.	Constants/Literals: Fixed values such as integers, floating-point numbers, and strings, e.g., 10, 3.14, "Hello".
# 5.	Separators (Punctuators): Symbols used to separate program elements, e.g., ;, ,, (, ), {, }.
# Example:
# For the statement:
# int sum = 10;
# Token	Category
# int	Keyword
# sum	Identifier
# =	Operator
# 10	Constant
# ;	Separator
# Algorithm:
# 1.	Start the program.
# 2.	Open the source code text file in read mode.
# 3.	Read the entire content of the file.
# 4.	Define regular expressions to identify different types of tokens.
# 5.	Scan the source code and identify each token.
# 6.	Classify each token as a keyword, identifier, operator, constant, or separator.
# 7.	Display all identified tokens in a tabular format.
# 8.	Close the file.
# 9.	Stop the program.

