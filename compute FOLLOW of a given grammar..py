# Program to compute FOLLOW sets

productions = {}

n = int(input("Enter number of productions: "))

for i in range(n):
    production = input("Enter production: ").replace(" ", "")
    lhs, rhs = production.split("->")

    if lhs not in productions:
        productions[lhs] = []

    productions[lhs].extend(rhs.split("|"))


# Find FIRST of a sequence
def first_sequence(sequence):

    result = set()

    if not sequence:
        return {"ε"}

    for symbol in sequence:

        if symbol == "ε":
            temp = {"ε"}
        elif symbol in productions:
            temp = first[symbol]
        else:
            temp = {symbol}

        result.update(temp - {"ε"})

        if "ε" not in temp:
            break

    else:
        result.add("ε")

    return result


# Compute FIRST sets
first = {nt: set() for nt in productions}

changed = True

while changed:
    changed = False

    for nt in productions:
        for rhs in productions[nt]:
            temp = first_sequence(rhs)
            old_size = len(first[nt])
            first[nt].update(temp)

            if len(first[nt]) != old_size:
                changed = True


# Initialize FOLLOW sets
follow = {nt: set() for nt in productions}

start_symbol = list(productions.keys())[0]
follow[start_symbol].add("$")


# Compute FOLLOW sets
changed = True

while changed:
    changed = False

    for nt in productions:
        for rhs in productions[nt]:

            for i, symbol in enumerate(rhs):

                if symbol in productions:

                    beta = rhs[i + 1:]
                    temp = first_sequence(beta)

                    old_size = len(follow[symbol])

                    follow[symbol].update(temp - {"ε"})

                    if "ε" in temp:
                        follow[symbol].update(follow[nt])

                    if len(follow[symbol]) != old_size:
                        changed = True


# Display FOLLOW sets
print("\nFOLLOW SETS")

for nt in productions:
    print(f"FOLLOW({nt}) = {{ {', '.join(sorted(follow[nt]))} }}")

# Theory:
# In compiler design, FOLLOW is a function used in syntax analysis to determine the set of terminals that can appear immediately after a non-terminal in a sentential form.
# The FOLLOW set is important in constructing predictive parsing tables and designing LL(1) parsers.
# Rules for computing FOLLOW:
# 1.	Add $ (end-of-input marker) to the FOLLOW set of the start symbol.
# 2.	If a production contains A → αBβ, add FIRST(β), excluding ε, to FOLLOW(B).
# 3.	If a production contains A → αB, add FOLLOW(A) to FOLLOW(B).
# 4.	If A → αBβ and FIRST(β) contains ε, add FOLLOW(A) to FOLLOW(B).
# 5.	Repeat the process until no more elements can be added.
# Example:
# Consider the following grammar:
# E  → T E'
# E' → + T E' | ε
# T  → F T'
# T' → * F T' | ε
# F  → ( E ) | id
# The FOLLOW sets are:
# Non-terminal	FOLLOW
# E	)$
# E'	)$
# T	+)$
# T'	+)$
# F	*+)$
# Algorithm:
# 1.	Start the program.
# 2.	Read the grammar productions from the user.
# 3.	Identify all non-terminals and initialize their FOLLOW sets as empty.
# 4.	Add $ to the FOLLOW set of the start symbol.
# 5.	Examine each production and locate its non-terminals.
# 6.	For each non-terminal, find the symbols appearing after it.
# 7.	Add FIRST of the following symbols, excluding ε, to its FOLLOW set.
# 8.	If the following symbols can derive ε or no symbols follow the non-terminal, add FOLLOW of the left-hand side non-terminal.
# 9.	Repeat the process until no more elements can be added.
# 10.	Display the FOLLOW set of each non-terminal.
# 11.	Stop the program.


