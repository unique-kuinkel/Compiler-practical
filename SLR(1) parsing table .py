
# Program to construct SLR(1) parsing table
# and check string acceptance or rejection

import re
from collections import deque

# Input grammar
productions = []
n = int(input("Enter number of productions: "))

grammar = {}

for _ in range(n):
    lhs, rhs = input("Enter production: ").split("->", 1)
    lhs = lhs.strip()
    grammar.setdefault(lhs, [])
    for alt in rhs.split("|"):
        grammar[lhs].append(alt.strip())

NT = list(grammar)
nt_set = set(NT)
start = NT[0]

# Tokenize productions
pattern = re.compile(
    r"ε|" + "|".join(re.escape(x) for x in sorted(NT, key=len, reverse=True))
    + r"|[A-Za-z_][A-Za-z0-9_]*|[^\s]"
)

P = [("S'", [start])]

for lhs in NT:
    for rhs in grammar[lhs]:
        P.append((lhs, [] if rhs == "ε" else pattern.findall(rhs)))

# Augmented grammar
nts = nt_set | {"S'"}
terms = sorted({
    s for lhs, rhs in P for s in rhs if s not in nts
})

# FIRST sets
first = {x: set() for x in nts}

def first_seq(seq):
    result = set()
    for s in seq:
        f = first[s] if s in nts else {s}
        result.update(f - {"ε"})
        if "ε" not in f:
            break
    else:
        result.add("ε")
    return result

changed = True
while changed:
    changed = False
    for lhs, rhs in P[1:]:
        old = len(first[lhs])
        first[lhs].update(first_seq(rhs))
        changed |= len(first[lhs]) != old

# FOLLOW sets
follow = {x: set() for x in NT}
follow[start].add("$")

changed = True
while changed:
    changed = False
    for lhs, rhs in P[1:]:
        for i, s in enumerate(rhs):
            if s in nt_set:
                old = len(follow[s])
                f = first_seq(rhs[i + 1:])
                follow[s].update(f - {"ε"})
                if "ε" in f:
                    follow[s].update(follow[lhs])
                changed |= len(follow[s]) != old

# Display FIRST and FOLLOW
print("\nFIRST SETS")
for x in NT:
    print(f"FIRST({x}) = {{ {', '.join(sorted(first[x]))} }}")

print("\nFOLLOW SETS")
for x in NT:
    print(f"FOLLOW({x}) = {{ {', '.join(sorted(follow[x]))} }}")

# LR(0) closure
def closure(items):
    items = set(items)
    changed = True
    while changed:
        changed = False
        for p, dot in list(items):
            lhs, rhs = P[p]
            if dot < len(rhs) and rhs[dot] in nts:
                for i, (a, b) in enumerate(P):
                    if a == rhs[dot] and (i, 0) not in items:
                        items.add((i, 0))
                        changed = True
    return frozenset(items)

# GOTO function
def goto(items, symbol):
    moved = {
        (p, dot + 1)
        for p, dot in items
        if dot < len(P[p][1]) and P[p][1][dot] == symbol
    }
    return closure(moved) if moved else frozenset()

# Construct canonical LR(0) item sets
states = [closure({(0, 0)})]
state_id = {states[0]: 0}
transitions = {}
queue = deque([0])

symbols = terms + NT

while queue:
    i = queue.popleft()
    for s in symbols:
        new_state = goto(states[i], s)
        if new_state:
            if new_state not in state_id:
                state_id[new_state] = len(states)
                states.append(new_state)
                queue.append(state_id[new_state])
            transitions[i, s] = state_id[new_state]

# Display LR(0) item sets
print("\nCANONICAL LR(0) ITEM SETS")

for i, state in enumerate(states):
    print(f"\nI{i}:")
    for p, dot in sorted(state):
        lhs, rhs = P[p]
        item = rhs[:]
        item.insert(dot, "·")
        print(f"  {lhs} -> {' '.join(item)}")

# Construct ACTION and GOTO tables
action = [{} for _ in states]
gotos = [{} for _ in states]

def add_entry(table, state, symbol, value):
    table[state].setdefault(symbol, set()).add(value)

for i, state in enumerate(states):
    for p, dot in state:
        lhs, rhs = P[p]

        if dot < len(rhs):
            s = rhs[dot]
            j = transitions[i, s]

            if s in terms:
                add_entry(action, i, s, f"s{j}")
            else:
                gotos[i][s] = j

        elif p == 0:
            add_entry(action, i, "$", "acc")

        else:
            for t in follow[lhs]:
                add_entry(action, i, t, f"r{p}")

# Display production numbering
print("\nPRODUCTIONS")
for i, (lhs, rhs) in enumerate(P):
    print(f"{i}. {lhs} -> {' '.join(rhs) if rhs else 'ε'}")

# Display SLR(1) parsing table
columns = terms + ["$"] + [x for x in NT if x != start]
headers = ["STATE"] + columns

width = max(12, max(len(x) for x in headers) + 2, 16)

def border():
    print("+" + "+".join("-" * width for _ in headers) + "+")

print("\nSLR(1) PARSING TABLE")
border()
print("|" + "|".join(x.center(width) for x in headers) + "|")
border()

for i in range(len(states)):
    row = [str(i)]

    for s in columns:
        if s in terms or s == "$":
            entries = action[i].get(s, set())
            value = "/".join(sorted(entries)) if entries else "-"
            if len(entries) > 1:
                value += " !"
        else:
            value = str(gotos[i][s]) if s in gotos[i] else "-"

        row.append(value)

    print("|" + "|".join(x.center(width) for x in row) + "|")
    border()

# Check SLR(1) conflicts
is_slr = all(
    len(entries) <= 1
    for row in action
    for entries in row.values()
)

if not is_slr:
    print("\nGrammar is NOT SLR(1).")
    print("Parsing cannot be performed using this table.")

else:
    print("\nGrammar is SLR(1).")

    # Input string tokenization
    string = input("\nEnter input string: ").strip()

    lex_pattern = re.compile(
        "|".join(re.escape(x) for x in sorted(terms, key=len, reverse=True))
        + r"|[A-Za-z_][A-Za-z0-9_]*|[^\s]"
    )

    tokens = lex_pattern.findall(string)
    if tokens and tokens[-1] == "$":
        tokens.pop()
    tokens.append("$")

    # SLR parsing
    stack = [0]
    index = 0
    accepted = False

    print("\nPARSING STEPS")
    print("-" * 65)
    print(f"{'STACK':<25}{'INPUT':<22}ACTION")
    print("-" * 65)

    while True:
        state = stack[-1]
        current = tokens[index]
        entries = action[state].get(current, set())

        stack_display = " ".join(map(str, stack))
        input_display = " ".join(tokens[index:])

        if len(entries) != 1:
            print(f"{stack_display:<25}{input_display:<22}ERROR")
            break

        act = next(iter(entries))

        if act == "acc":
            print(f"{stack_display:<25}{input_display:<22}ACCEPT")
            accepted = True
            break

        elif act.startswith("s"):
            print(f"{stack_display:<25}{input_display:<22}SHIFT {act[1:]}")
            stack.extend([current, int(act[1:])])
            index += 1

        elif act.startswith("r"):
            p = int(act[1:])
            lhs, rhs = P[p]

            print(
                f"{stack_display:<25}{input_display:<22}"
                f"REDUCE {lhs} -> {' '.join(rhs) if rhs else 'ε'}"
            )

            if rhs:
                del stack[-2 * len(rhs):]

            stack.extend([lhs, gotos[stack[-1]][lhs]])

    print("\nString Accepted!" if accepted else "\nString Rejected!")


# Theory:
# SLR(1) (Simple LR) Parser is a bottom-up parser used in compiler design to recognize the syntax of a given input string. It reads input from left to right and produces the rightmost derivation in reverse.
# SLR(1) parsing uses a collection of LR(0) items and FOLLOW sets to construct a parsing table.
# Important terms:
# 1.	LR(0) Items: Productions with a dot (·) indicating how much of a production has been recognized.
# o	Example: A → α · β
# 2.	Closure: Adds productions of a non-terminal when the dot appears before that non-terminal.
# 3.	Goto: Determines the next state after recognizing a grammar symbol.
# 4.	ACTION Table: Specifies shift, reduce, accept, or error operations.
# 5.	GOTO Table: Specifies the next state for a non-terminal.
# Rules for constructing an SLR(1) parsing table:
# 1.	Augment the grammar by adding a new start production S' → S.
# 2.	Construct the canonical collection of LR(0) items using closure and GOTO functions.
# 3.	For an item A → α · aβ, where a is a terminal, add a SHIFT action.
# 4.	For an item A → α ·, add a REDUCE action for every terminal in FOLLOW(A).
# 5.	For the item S' → S ·, add ACCEPT for the end marker $.
# 6.	If conflicting actions occur in a table entry, the grammar is not SLR(1).
# Example Grammar:
# E → E + T | T
# T → T * F | F
# F → ( E ) | id
# An SLR(1) parser uses the generated ACTION and GOTO tables to determine whether an input string belongs to the given grammar.
# Algorithm:
# A. Construction of SLR(1) Parsing Table
# 1.	Start the program.
# 2.	Read the grammar productions.
# 3.	Augment the grammar with a new start production.
# 4.	Calculate FIRST and FOLLOW sets.
# 5.	Generate LR(0) item sets using closure and GOTO functions.
# 6.	Construct the canonical collection of LR(0) states.
# 7.	Build the ACTION table using shift, reduce, and accept operations.
# 8.	Build the GOTO table for non-terminals.
# 9.	Check for conflicts to determine whether the grammar is SLR(1).
# 10.	Display the parsing table.
# B. String Acceptance and Rejection
# 1.	Read an input string.
# 2.	Initialize the parsing stack with state 0.
# 3.	Read the current input symbol.
# 4.	Check the ACTION table for the current state and input symbol.
# 5.	If the action is SHIFT, push the symbol and next state onto the stack.
# 6.	If the action is REDUCE, pop the symbols and states corresponding to the production's right-hand side, then use the GOTO table.
# 7.	If the action is ACCEPT, display "String Accepted".
# 8.	If no valid action exists, display "String Rejected".
# 9.	Stop the program.
