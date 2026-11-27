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

# Theory:
# In compiler design, regular expressions are used to represent patterns of strings. They are commonly used in lexical analysis to recognize tokens and validate input strings.
# The given patterns are:
# 1.	a* (Zero or more a's): Accepts any number of occurrences of a, including an empty string.
# o	Examples: ε, a, aa, aaa.
# 2.	a*b+ (Zero or more a's followed by one or more b's): Accepts strings containing zero or more a characters followed by at least one b.
# o	Examples: b, ab, aab, aaabb.
# 3.	abb (Exact string): Accepts only the string abb.
# o	Examples: abb is valid, whereas ab, aabb, and abbb are invalid.
# Regular Expression Symbols:
# •	* – Zero or more occurrences.
# •	+ – One or more occurrences.
# •	ε – Empty string.
# Algorithm:
# 1.	Start the program.
# 2.	Display the three regular expression patterns.
# 3.	Read a string from the user.
# 4.	Check whether the string matches the pattern a*.
# 5.	Check whether the string matches the pattern a*b+.
# 6.	Check whether the string exactly matches abb.
# 7.	Display which pattern or patterns recognize the given string.
# 8.	If no pattern matches, display "String not recognized".
# 9.	Stop the program.

