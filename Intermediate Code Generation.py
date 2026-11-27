
import re

# Tokenizer
pattern = r'\s+|\d+(?:\.\d*)?|[a-zA-Z_]\w*|<=|>=|==|!=|&&|\|\||[+\-*/%<>=!(){};]'

def tokenize(code):
    tokens = []
    pos = 0

    while pos < len(code):
        match = re.match(pattern, code[pos:])

        if not match:
            raise SyntaxError(f"Invalid character: {code[pos]}")

        token = match.group()
        pos += len(token)

        if not token.isspace():
            tokens.append(token)

    tokens.append("$")
    return tokens


# Parser
class Parser:
    precedence = {
        "||": 1, "&&": 2,
        "==": 3, "!=": 3,
        "<": 4, ">": 4, "<=": 4, ">=": 4,
        "+": 5, "-": 5,
        "*": 6, "/": 6, "%": 6
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos]

    def eat(self, expected=None):
        token = self.peek()

        if expected and token != expected:
            raise SyntaxError(f"Expected {expected}, got {token}")

        self.pos += 1
        return token

    def expression(self, min_prec=1):
        token = self.eat()

        if token in ("!", "-", "+"):
            left = ("unary", token, self.expression(7))
        elif token == "(":
            left = self.expression()
            self.eat(")")
        elif re.fullmatch(r'\d+(?:\.\d*)?', token):
            left = ("value", token)
        elif re.fullmatch(r'[a-zA-Z_]\w*', token):
            left = ("value", token)
        else:
            raise SyntaxError(f"Unexpected token: {token}")

        while self.peek() in self.precedence:
            op = self.peek()
            prec = self.precedence[op]

            if prec < min_prec:
                break

            self.eat()
            right = self.expression(prec + 1)
            left = ("binary", op, left, right)

        return left

    def statement(self):
        if self.peek() == "if":
            self.eat("if")
            self.eat("(")
            condition = self.expression()
            self.eat(")")
            body = self.statement()

            if self.peek() == "else":
                self.eat("else")
                return ("ifelse", condition, body,
                        self.statement())

            return ("if", condition, body)

        if self.peek() == "{":
            self.eat("{")
            statements = []

            while self.peek() != "}":
                if self.peek() == "$":
                    raise SyntaxError("Missing closing brace")
                statements.append(self.statement())

            self.eat("}")
            return ("block", statements)

        variable = self.eat()

        if not re.fullmatch(r'[a-zA-Z_]\w*', variable):
            raise SyntaxError("Expected an assignment variable")

        self.eat("=")
        value = self.expression()
        self.eat(";")

        return ("assign", variable, value)


# Three Address Code Generator
class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_count = 0
        self.label_count = 0

    def temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def emit(self, instruction):
        self.code.append(instruction)

    def emit_value(self, node):
        kind = node[0]

        if kind == "value":
            return node[1]

        if kind == "unary":
            op, operand = node[1], self.emit_value(node[2])
            result = self.temp()
            self.emit(f"{result} = {op}{operand}")
            return result

        op, left, right = node[1], node[2], node[3]

        if op in ("&&", "||", "<", ">", "<=", ">=", "==", "!="):
            return self.boolean_value(node)

        a = self.emit_value(left)
        b = self.emit_value(right)

        result = self.temp()
        self.emit(f"{result} = {a} {op} {b}")
        return result

    def condition(self, node, true_label, false_label):
        if node[0] == "unary" and node[1] == "!":
            self.condition(node[2], false_label, true_label)
            return

        if node[0] == "binary":
            op, left, right = node[1], node[2], node[3]

            if op == "&&":
                middle = self.label()
                self.condition(left, middle, false_label)
                self.emit(middle + ":")
                self.condition(right, true_label, false_label)
                return

            if op == "||":
                middle = self.label()
                self.condition(left, true_label, middle)
                self.emit(middle + ":")
                self.condition(right, true_label, false_label)
                return

            if op in ("<", ">", "<=", ">=", "==", "!="):
                a = self.emit_value(left)
                b = self.emit_value(right)
                self.emit(f"if {a} {op} {b} goto {true_label}")
                self.emit(f"goto {false_label}")
                return

        value = self.emit_value(node)
        self.emit(f"if {value} != 0 goto {true_label}")
        self.emit(f"goto {false_label}")

    def boolean_value(self, node):
        result = self.temp()
        true_label = self.label()
        false_label = self.label()
        end_label = self.label()

        self.condition(node, true_label, false_label)

        self.emit(true_label + ":")
        self.emit(f"{result} = 1")
        self.emit(f"goto {end_label}")

        self.emit(false_label + ":")
        self.emit(f"{result} = 0")

        self.emit(end_label + ":")
        return result

    def statement(self, node):
        kind = node[0]

        if kind == "assign":
            value = self.emit_value(node[2])
            self.emit(f"{node[1]} = {value}")

        elif kind == "block":
            for statement in node[1]:
                self.statement(statement)

        elif kind == "if":
            true_label = self.label()
            end_label = self.label()

            self.condition(node[1], true_label, end_label)

            self.emit(true_label + ":")
            self.statement(node[2])
            self.emit(end_label + ":")

        elif kind == "ifelse":
            true_label = self.label()
            false_label = self.label()
            end_label = self.label()

            self.condition(node[1], true_label, false_label)

            self.emit(true_label + ":")
            self.emit(f"goto {end_label}")

            self.emit(false_label + ":")
            self.statement(node[3])

            self.emit(end_label + ":")


# Main program
try:
    source = input("Enter an expression or statement: ")

    tokens = tokenize(source)
    parser = Parser(tokens)

    syntax_tree = parser.statement()

    if parser.peek() != "$":
        raise SyntaxError(f"Unexpected token: {parser.peek()}")

    generator = CodeGenerator()
    generator.statement(syntax_tree)

    print("\nIntermediate Code (Three Address Code):\n")

    for instruction in generator.code:
        print(instruction)

except (SyntaxError, IndexError) as error:
    print("Invalid expression:", error)


# Theory:
# Intermediate Code Generation is a phase of a compiler that converts source code into an intermediate representation (IR) before generating the target machine code.
# One common form of intermediate code is Three Address Code (TAC). In TAC, each instruction contains at most three addresses (two operands and one result).
# For example, the expression:
# a = b + c * d
# is converted into:
# t1 = c * d
# t2 = b + t1
# a = t2
# Here, t1 and t2 are temporary variables used to store intermediate results.
# Algorithm:
# 1.	Start the program.
# 2.	Read an arithmetic expression from the user.
# 3.	Tokenize the expression into operands and operators.
# 4.	Convert the expression into postfix notation while considering operator precedence.
# 5.	Generate temporary variables for intermediate calculations.
# 6.	Generate Three Address Code instructions.
# 7.	Display the generated intermediate code.
# 8.	Stop the program.
