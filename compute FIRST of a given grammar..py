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

# Theory:
# In compiler design, FIRST is a function used in syntax analysis (parsing) to determine the set of terminals that can appear at the beginning of strings derived from a particular grammar symbol.
# The FIRST set is important in constructing predictive parsing tables and designing LL(1) parsers.
# Rules for computing FIRST:
# 1.	If X is a terminal, then FIRST(X) = .
# 2.	If X → ε, then add ε to FIRST(X).
# 3.	If X → aα, where a is a terminal, add a to FIRST(X).
# 4.	If X → Y₁Y₂...Yₙ, add FIRST(Y₁) to FIRST(X), excluding ε.
# 5.	If FIRST(Y₁) contains ε, consider FIRST(Y₂), and continue similarly.
# 6.	If all symbols can derive ε, add ε to FIRST(X).
# Example:
# Consider the following grammar:
# E  → T E'
# E' → + T E' | ε
# T  → F T'
# T' → * F T' | ε
# F  → ( E ) | id
# The FIRST sets are:
# Non-terminal	FIRST
# E	(id
# E'	+ε
# T	(id
# T'	*ε
# F	(id
# Algorithm:
# 1.	Start the program.
# 2.	Read the grammar productions from the user.
# 3.	Initialize an empty FIRST set for each non-terminal.
# 4.	Examine each production one by one.
# 5.	If the first symbol is a terminal, add it to the FIRST set.
# 6.	If the first symbol is a non-terminal, add its FIRST elements, excluding ε.
# 7.	If the FIRST set contains ε, examine the next symbol.
# 8.	If all symbols can derive ε, add ε to the FIRST set.
# 9.	Repeat the process until no more elements can be added.
# 10.	Display the FIRST set of each non-terminal.
# 11.	Stop the program.

