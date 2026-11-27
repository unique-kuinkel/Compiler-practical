def is_comment(string):
    string = string.strip()

    # Check for single-line comment
    if string.startswith("#"):
        return True

    # Check for multi-line comment
    elif string.startswith("/*") and string.endswith("*/"):
        return True

    else:
        return False

# Take input from user
s = input("Enter a string: ")

if is_comment(s):
    print("Valid Comment")
else:
    print("Invalid Comment")
