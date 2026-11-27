import re

# Function to recognize strings
def recognize_string(s):

    patterns = {
        "a*": r"a*",
        "a*b+": r"a*b+",
        "abb": r"abb"
    }

    found = False

    for pattern, regex in patterns.items():

        if re.fullmatch(regex, s):
            print("String is recognized under:", pattern)
            found = True

    if not found:
        print("String is not recognized under any pattern.")


# Main program
string = input("Enter a string: ")

recognize_string(string)
