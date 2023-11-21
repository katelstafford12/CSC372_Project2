import re

# Regex expressions for our language
int_declaration = re.compile("^([A-Z]) is (\d+)!$")
str_declaration = re.compile("^([A-Z]) is \"(.*)\"!$")
bool_declaration = re.compile("^([A-Z]) is (yes|no)!")
arithmetic_expression = re.compile("^([A-Z]) is ([A-Z]|\d+) (plus|minus|times|divided by|modulus) ([A-Z]|\d+)!$")
boolean_expression = re.compile("^[A-Z]\s+is\s+[A-Z]\s+[\/\\][\/\\]\s+[A-Z]\!") # This ones not working
not_expression = re.compile("^([A-Z]) is opposite ([A-Z])!")
comparison_expression = re.compile("^([A-Z]) is ([A-Z]|\d+) (greater than|less than|equals) ([A-Z]|\d+)!")
conditional_statement = re.compile("^([A-Z]) is (\d+)! when (\(.*\)) do (\(.*\)) or when(\(.*\)) do (\(.*\))$")
while_loop = re.compile("^([A-Z]) is (\d+)! ([A-Z]) is (\d+)! as long as (\(.*\)) do (\(.*\))$") # This ones not working
print_statement = re.compile("^(?:([A-Z]) is ([A-Z]|\d+|\".*\")! )?say ([A-Z]|\d+|\".*\")!")
grouping_expression = re.compile("^([A-Z]) is ([A-Z]|\d+)! \[([A-Z]|\d+) (plus) ([A-Z]|\d+)\] plus \[([A-Z]|\d+) (plus) ([A-Z]|\d+)\]!") # This ones not working

variables = {}

# Determines if the line in the language matches any regex expressions above
def execute_line(line):
    match = int_declaration.match(line)
    if match:
        var = match.group(1)
        value = int(match.group(2))
        variables[var] = value
        return

    match = str_declaration.match(line)
    if match:
        var = match.group(1)
        value = match.group(2)
        variables[var] = value
        return

    match = bool_declaration.match(line)
    if match:
        var = match.group(1)
        value = match.group(2)
        variables[var] = True if value == 'yes' else False
        return

    match = arithmetic_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operator = match.group(3)
        operand2 = match.group(4)
        perform_arithmetic(var, operand1, operator, operand2)
        return

    match = boolean_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operator = match.group(3)
        operand2 = match.group(4)
        perform_boolean(var, operand1, operator, operand2)
        return

    match = not_expression.match(line)
    if match:
        var = match.group(1)
        operand = match.group(2)
        perform_not(var, operand)
        return

    match = comparison_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operator = match.group(3)
        operand2 = match.group(4)
        perform_comparison(var, operand1, operator, operand2)
        return

    match = conditional_statement.match(line)
    if match:
        var = match.group(1)
        value = int(match.group(2))
        condition1 = match.group(3)
        do1 = match.group(4)
        condition2 = match.group(5)
        do2 = match.group(6)
        perform_conditional(var, value, condition1, do1, condition2, do2)
        return

    match = while_loop.match(line)
    if match:
        var1 = match.group(1)
        value1 = int(match.group(2))
        var2 = match.group(3)
        value2 = int(match.group(4))
        condition = match.group(5)
        do_block = match.group(6)
        perform_while_loop(var1, value1, var2, value2, condition, do_block)
        return

    match = print_statement.match(line)
    if match:
        var1 = match.group(1)
        var2 = match.group(2)
        print_value(var2)
        return

    match = grouping_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operand2 = match.group(3)
        operator1 = match.group(4)
        operand3 = match.group(5)
        operator2 = match.group(6)
        operand4 = match.group(7)
        perform_grouping(var, operand1, operand2, operator1, operand3, operator2, operand4)
        return

    # If the line doesnt match anything
    print(f"Error: This line isn't matching the language: {line}")

# Handles arithmetic in our language
def perform_arithmetic(var, operand1, operator, operand2):
    if operand1.isdigit():
        val1 = int(operand1)
    else:
        if operand1 in variables.keys():
            val1 = variables[operand1]
        else:
            print(f'Unknown Variable - {operand1}')
            return
    if operand2.isdigit():
        val2 = int(operand2)
    else:
        if operand2 in variables.keys():
            val2 = variables[operand2]
        else:
            print(f'Unknown Variable - {operand2}')
            return
    if not isinstance(val2, int) or not isinstance(val1, int):
        print(f'Unsupported types for the arithmetic operator {operator}!')
        return
    if operator == "plus":
        val = val1 + val2
    elif operator == "divided by":
        val = val1 / val2
    elif operator == "times":
        val = val1 * val2
    elif operator == "minus":
        val = val1 - val2
    elif operator == "modulus":
        val = val1 % val2
    variables[var] = val
    print(f'{var} has been assigned to {val}')
    

# Handles booleans in our language    
def perform_boolean(var, operand1, operator, operand2):
   print("Boolean: Not yet implemented")

# Handles NOT in our language
def perform_not(var, operand):
    if operand in variables.keys():
        val = variables[operand]
    elif operand == 'no':
        val = False
    elif operand == "yes":
        val = True
    if val != True or val != False:
        print("Unsupport operand type!")
        return
    variables[var] = not val
    print(f'{var} has been assigned to {not val}')

# Handles comparisons in our language
def perform_comparison(var, operand1, operator, operand2):
    if operand1.isdigit():
        val1 = int(operand1)
    else:
        if operand1 in variables.keys():
            val1 = variables[operand1]
        else:
            print(f'Unknown Variable - {operand1}')
            return
    if operand2.isdigit():
        val2 = int(operand2)
    else:
        if operand2 in variables.keys():
            val2 = variables[operand2]
        else:
            print(f'Unknown Variable - {operand2}')
            return
    if not isinstance(val2, int) or not isinstance(val1, int):
        print("Unsupported types for comparison operators!")
        return
    if operator == 'greater than':
        val = val1 > val2
    elif operator == 'less than':
        val = val1 < val2
    elif operator == 'equals':
        val = val1 == val2
    variables[var] = val
    print(f'{var} assigned to {val}')

# Handles conditionals in our language
def perform_conditional(var, value, condition1, do1, condition2, do2):
    print("Conditional: Not yet implemented")

# Handles while loops in our language
def perform_while_loop(var1, value1, var2, value2, condition, do_block):
    print("While loop: Not yet implemented")

# Handles print statements in our language
def print_value(var):
    print("Print: Not yet implemented")

# Handles grouping in our language
def perform_grouping(var, operand1, operand2, operator1, operand3, operator2, operand4):
    print("Grouping: Not yet implemented")

# Handles executions in our language
def execute_block(block):
    print("Execute: Not yet implemented")

# Example usage:
program = """A is 25!
B is "i am a string"!
C is yes!
D is no!
C is A plus B!
C is 2 plus 3!
C is 3 minus 2!
C is 3 times 2!
C is 4 divided by 2!
C is 4 modulus 2!
C is A /\ B!
C is A \/ B!
C is opposite A!
C is 1 greater than 2!
C is 1 less than 2!
C is 1 equals 2!
X is 0! when (X equals 0!) do (X is X plus 1!) or when(X equals 1!) do (X is X plus 1!)
X is 2!
Y is 0!
as long as (X greater than Y) do (Y is Y plus 1!)
X is 2!
say X!
A is 1!
B is 2!
C is [A plus 1] plus [B plus 2]!
"""

# Testing with the example programs:
#file_path = 'Program1.py'
#with open(file_path, 'r') as file:
#    program = file.read()
    
lines = program.split("\n")
for line in lines:
    execute_line(line.strip())
