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
# In compiler design, a comment is a part of source code that provides explanations or notes for programmers. Comments are ignored by the compiler during the compilation process.
# Comments are generally classified into two types:
# 1.	Single-line comment: Begins with # in Python and continues until the end of the line.
# o	Syntax: # comment
# o	Example: # This is a comment
# 2.	Multi-line comment: Begins with /* and ends with */ in languages like C, C++, and Java.
# o	Syntax: /* comment */
# o	Example: /* This is a multi-line comment */
# A string is considered a valid comment if it follows the proper opening and closing symbols.
# Algorithm:
# 1.	Start the program.
# 2.	Read a string from the user.
# 3.	Remove leading and trailing whitespace.
# 4.	Check whether the string starts with #.
# 5.	If not, check whether it starts with /* and ends with */.
# 6.	If either condition is true, display "Valid Comment".
# 7.	Otherwise, display "Invalid Comment".
# 8.	Stop the program.
