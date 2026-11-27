
# Program to construct LL(1) parsing table
# and check string acceptance or rejection

import re

# Input grammar
productions = {}

n = int(input("Enter number of productions: "))

raw_productions = []

for i in range(n):
    rule = input("Enter production: ").strip()
    lhs, rhs = rule.split("->", 1)

    lhs = lhs.strip()

    if lhs not in productions:
        productions[lhs] = []

    raw_productions.append((lhs, rhs))


non_terminals = list(productions.keys())
nt_set = set(non_terminals)

# Tokenize productions
nt_pattern = "|".join(
    re.escape(nt) for nt in sorted(non_terminals, key=len, reverse=True)
)

token_pattern = re.compile(
    r"ε|" + nt_pattern + r"|[a-z][a-zA-Z0-9_]*|[^\s]"
)

for lhs, rhs in raw_productions:
    for alternative in rhs.split("|"):
        tokens = token_pattern.findall(alternative.strip())
        productions[lhs].append(tokens)


# Find FIRST of a sequence
def first_sequence(sequence):
    result = set()

    if not sequence:
        return {"ε"}

    for symbol in sequence:

        if symbol == "ε":
            temp = {"ε"}

        elif symbol in nt_set:
            temp = first[symbol]

        else:
            temp = {symbol}

        result.update(temp - {"ε"})

        if "ε" not in temp:
            break

    else:
        result.add("ε")

    return result


# Calculate FIRST sets
first = {nt: set() for nt in non_terminals}

changed = True

while changed:
    changed = False

    for nt in non_terminals:
        for rhs in productions[nt]:

            old = len(first[nt])
            first[nt].update(first_sequence(rhs))

            if len(first[nt]) != old:
                changed = True


# Calculate FOLLOW sets
follow = {nt: set() for nt in non_terminals}

start_symbol = non_terminals[0]
follow[start_symbol].add("$")

changed = True

while changed:
    changed = False

    for nt in non_terminals:
        for rhs in productions[nt]:

            for i, symbol in enumerate(rhs):

                if symbol in nt_set:

                    temp = first_sequence(rhs[i + 1:])

                    old = len(follow[symbol])

                    follow[symbol].update(temp - {"ε"})

                    if "ε" in temp:
                        follow[symbol].update(follow[nt])

                    if len(follow[symbol]) != old:
                        changed = True


# Display FIRST sets
print("\nFIRST SETS")

for nt in non_terminals:
    print(f"FIRST({nt}) = {{ {', '.join(sorted(first[nt]))} }}")


# Display FOLLOW sets
print("\nFOLLOW SETS")

for nt in non_terminals:
    print(f"FOLLOW({nt}) = {{ {', '.join(sorted(follow[nt]))} }}")


# Construct LL(1) parsing table
table = {nt: {} for nt in non_terminals}

for nt in non_terminals:
    for rhs in productions[nt]:

        temp = first_sequence(rhs)

        for terminal in temp - {"ε"}:
            table[nt].setdefault(terminal, []).append(rhs)

        if "ε" in temp:
            for terminal in follow[nt]:
                table[nt].setdefault(terminal, []).append(rhs)


# Find terminals
terminals = set()

for nt in non_terminals:
    for rhs in productions[nt]:
        for symbol in rhs:
            if symbol not in nt_set and symbol != "ε":
                terminals.add(symbol)

terminals.add("$")
terminals = sorted(terminals)


# Display LL(1) parsing table with borders
print("\nLL(1) PARSING TABLE")

# Determine column width automatically
col_width = max(
    16,
    max(len(nt) for nt in non_terminals) + 2,
    max(
        (
            len(nt + " -> " + " ".join(rhs))
            for nt in non_terminals
            for entries in table[nt].values()
            for rhs in entries
        ),
        default=0
    ) + 2
)

# Print table border
def print_border():
    print(
        "+"
        + "+".join("-" * col_width for _ in range(len(terminals) + 1))
        + "+"
    )


# Print header
print_border()

header = ["NT"] + terminals

print(
    "|"
    + "|".join(item.center(col_width) for item in header)
    + "|"
)

print_border()


# Print table contents
for nt in non_terminals:

    row = [nt]

    for terminal in terminals:

        entries = table[nt].get(terminal, [])

        if entries:
            value = nt + " -> " + " ".join(entries[0])

            if len(entries) > 1:
                value += " (CONFLICT)"

        else:
            value = "-"

        row.append(value)

    print(
        "|"
        + "|".join(item.center(col_width) for item in row)
        + "|"
    )

    print_border()


# Check whether grammar is LL(1)
is_ll1 = all(
    len(entries) <= 1
    for row in table.values()
    for entries in row.values()
)

if not is_ll1:

    print("\nGrammar is NOT LL(1).")
    print("Parsing cannot be performed using LL(1) table.")

else:

    print("\nGrammar is LL(1).")

    # Parse input string
    string = input(
        "\nEnter input string (space-separated tokens): "
    )

    tokens = string.split() + ["$"]

    stack = ["$", start_symbol]
    index = 0

    # Parsing step column widths
    stack_width = 25
    input_width = 25
    action_width = 25

    print("\nPARSING STEPS")

    print(
        "+" + "-" * stack_width
        + "+" + "-" * input_width
        + "+" + "-" * action_width + "+"
    )

    print(
        "|"
        + "STACK".center(stack_width)
        + "|"
        + "INPUT".center(input_width)
        + "|"
        + "ACTION".center(action_width)
        + "|"
    )

    print(
        "+" + "-" * stack_width
        + "+" + "-" * input_width
        + "+" + "-" * action_width + "+"
    )

    accepted = False

    while stack:

        top = stack[-1]
        current = tokens[index] if index < len(tokens) else None

        stack_display = " ".join(stack)
        input_display = " ".join(tokens[index:])

        action = ""

        if top == "$" and current == "$":

            action = "ACCEPT"

            accepted = True

        elif top == current:

            action = "Match " + current

            stack.pop()
            index += 1

        elif top in nt_set:

            entries = table[top].get(current, [])

            if entries:

                rhs = entries[0]

                action = top + " -> " + " ".join(rhs)

                stack.pop()

                if rhs != ["ε"]:
                    stack.extend(reversed(rhs))

            else:

                action = "ERROR"

        else:

            action = "ERROR"

        # Print parsing step
        print(
            "|"
            + stack_display.ljust(stack_width)
            + "|"
            + input_display.ljust(input_width)
            + "|"
            + action.ljust(action_width)
            + "|"
        )

        print(
            "+" + "-" * stack_width
            + "+" + "-" * input_width
            + "+" + "-" * action_width + "+"
        )

        if accepted or action == "ERROR":
            break

    if accepted:
        print("\nString Accepted!")
    else:
        print("\nString Rejected!")
