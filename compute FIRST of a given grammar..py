# Program to compute FIRST sets

productions = {}

n = int(input("Enter number of productions: "))

for i in range(n):
    production = input("Enter production: ").replace(" ", "")
    lhs, rhs = production.split("->")

    if lhs not in productions:
        productions[lhs] = []

    productions[lhs].extend(rhs.split("|"))


# Function to find FIRST
def find_first(symbol, visited=None):

    if visited is None:
        visited = set()

    first = set()

    # If symbol is a terminal
    if symbol not in productions:
        return {symbol}

    if symbol in visited:
        return first

    visited.add(symbol)

    for production in productions[symbol]:

        if production == "ε":
            first.add("ε")
            continue

        for char in production:

            temp = find_first(char, visited.copy())

            first.update(temp - {"ε"})

            if "ε" not in temp:
                break

        else:
            first.add("ε")

    return first


# Display FIRST sets
print("\nFIRST SETS")

for non_terminal in productions:
    result = find_first(non_terminal)
    print(f"FIRST({non_terminal}) = {{ {', '.join(sorted(result))} }}")
