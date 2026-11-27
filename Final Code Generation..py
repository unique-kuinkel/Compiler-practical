
import re

def generate_code(instructions):
    target = []

    operations = {
        "+": "ADD",
        "-": "SUB",
        "*": "MUL",
        "/": "DIV",
        "%": "MOD"
    }

    jumps = {
        "==": "JE",
        "!=": "JNE",
        "<": "JL",
        ">": "JG",
        "<=": "JLE",
        ">=": "JGE"
    }

    for line in instructions:
        line = line.strip()

        if not line:
            continue

        # Handle labels
        if re.fullmatch(r'L\d+:', line):
            target.append(line)
            continue

        # Handle unconditional goto
        match = re.fullmatch(r'goto\s+(L\d+)', line)

        if match:
            target.append(f"JMP {match.group(1)}")
            continue

        # Handle conditional goto
        match = re.fullmatch(
            r'if\s+(\S+)\s*(==|!=|<=|>=|<|>)\s*(\S+)\s+goto\s+(L\d+)',
            line
        )

        if match:
            a, op, b, label = match.groups()
            target.append(f"CMP {a}, {b}")
            target.append(f"{jumps[op]} {label}")
            continue

        # Handle assignment
        match = re.fullmatch(
            r'(\w+)\s*=\s*(.+)',
            line
        )

        if match:
            result, expression = match.groups()
            expression = expression.strip()

            # Arithmetic operation
            parts = expression.split()

            if len(parts) == 3 and parts[1] in operations:
                a, op, b = parts

                target.append(f"MOV R0, {a}")
                target.append(f"{operations[op]} R0, {b}")
                target.append(f"MOV {result}, R0")

            # Simple assignment
            elif re.fullmatch(r'[\w.]+', expression):
                target.append(f"MOV {result}, {expression}")

            else:
                raise ValueError(f"Invalid instruction: {line}")

            continue

        raise ValueError(f"Invalid instruction: {line}")

    return target


# Main program
try:
    n = int(input("Enter number of instructions: "))

    instructions = []

    print("Enter Three Address Code instructions:")

    for i in range(n):
        instructions.append(input())

    print("\nGenerated Target Code:\n")

    for instruction in generate_code(instructions):
        print(instruction)

except (ValueError, IndexError) as error:
    print("Error:", error)

# Theory:
# Final Code Generation is the last phase of a compiler. It converts intermediate code into target machine code or assembly language instructions.
# In this program, Three Address Code (TAC) is converted into simple assembly-like instructions.
# For example, the intermediate code:
# t1 = a + b
# t2 = t1 * c
# is converted into:
# MOV R0, a
# ADD R0, b
# MOV t1, R0
# MOV R0, t1
# MUL R0, c
# MOV t2, R0
# Here:
# •	MOV transfers data between memory locations and registers.
# •	ADD performs addition.
# •	SUB performs subtraction.
# •	MUL performs multiplication.
# •	DIV performs division.
# Algorithm:
# 1.	Start the program.
# 2.	Read the number of intermediate code instructions.
# 3.	Read each Three Address Code instruction.
# 4.	Split each instruction into its result, operands, and operator.
# 5.	Load the first operand into a register.
# 6.	Generate the appropriate assembly instruction based on the operator.
# 7.	Store the result in the destination variable.
# 8.	Display the generated target code.

