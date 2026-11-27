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
