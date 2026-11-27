import re
import keyword

# Function to check identifier validity
def check_identifier(identifier):

    pattern = r'^[a-zA-Z_][a-zA-Z0-9_]*$'

    if re.fullmatch(pattern, identifier) and not keyword.iskeyword(identifier):
        print("Valid Identifier")
    else:
        print("Invalid Identifier")


# Take input from user
identifier = input("Enter an identifier: ")

check_identifier(identifier)

# Theory:
# An identifier is a name used to identify variables, functions, arrays, classes, and other user-defined elements in a program.
# In compiler design, the lexical analyzer recognizes identifiers based on the rules defined by the programming language.
# Rules for a valid identifier:
# 1.	An identifier must begin with an alphabet (A–Z or a–z) or an underscore (_).
# 2.	It can contain alphabets, digits (0–9), and underscores.
# 3.	It cannot begin with a digit.
# 4.	Spaces and special characters are not allowed.
# 5.	Reserved keywords such as if, while, and int cannot be used as identifiers.
# Syntax (Regular Expression):
# ^[a-zA-Z_][a-zA-Z0-9_]*$
# Examples:
# •	Valid: name, _total, num123, student_name
# •	Invalid: 123name, student name, first-name, int
# Algorithm:
# 1.	Start the program.
# 2.	Read an identifier from the user.
# 3.	Define a regular expression to check identifier syntax.
# 4.	Check whether the identifier starts with a letter or underscore.
# 5.	Check whether the remaining characters contain only letters, digits, or underscores.
# 6.	Check whether the identifier is a reserved keyword.
# 7.	If all conditions are satisfied, display "Valid Identifier".
# 8.	Otherwise, display "Invalid Identifier".
# 9.	Stop the program.
