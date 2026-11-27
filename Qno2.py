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