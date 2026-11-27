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
