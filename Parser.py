import re

# Regex expressions for our language
int_declaration = re.compile("^([A-Z]) is (\d+)!$")
str_declaration = re.compile("^([A-Z]) is \"(.*)\"!$")
bool_declaration = re.compile("^([A-Z]) is (yes|no)!")
arithmetic_expression = re.compile("^([A-Z]) is ([A-Z]|\d+) (plus|minus|times|divided by|modulus) ([A-Z]|\d+)!$")
boolean_expression = re.compile(r"^([A-Z]) is ([A-Z]) (\\\/|\/\\) ([A-Z])!$") # Fixed! Will continue to test
not_expression = re.compile("^([A-Z]) is opposite ([A-Z])!")
comparison_expression = re.compile("^([A-Z]) is ([A-Z]|\d+) (greater than|less than|equals) ([A-Z]|\d+)!")
conditional_statement = re.compile("^([A-Z]) is (\d+)! when (\(.*\)) do (\(.*\)) or when(\(.*\)) do (\(.*\))$")
while_loop = re.compile(r"^as long as \((.*)\) do \((.*)\)$") # Fixed! Will continue to test
print_statement = re.compile("^(?:([A-Z]) is ([A-Z]|\d+|\".*\")! )?say ([A-Z]|\d+|\".*\")!")
grouping_expression = re.compile("^([A-Z]) is \[([A-Z]|\d+) (plus) ([A-Z]|\d+)\] plus \[([A-Z]|\d+) (plus) ([A-Z]|\d+)\]!") # Fixed for now!

variables = {'yes': True, 'no': False}

def has_lowercase_letter(s):
    return bool(re.search(r'[a-z]', s))

# Determines if the line in the language matches any regex expressions above
def execute_line(line, int_mode, i=0):
    if line == "":
        return
    match = int_declaration.match(line)
    if match:
        var = match.group(1)
        value = int(match.group(2))
        variables[var] = value
        if int_mode:
            print(f"{var} has been assigned to {value}")
        return

    match = str_declaration.match(line)
    if match:
        var = match.group(1)
        value = match.group(2)
        variables[var] = value
        if int_mode:
            print(f"{var} has been assigned to {value}")
        return

    match = bool_declaration.match(line)
    if match:
        var = match.group(1)
        value = match.group(2)
        variables[var] = True if value == 'yes' else False
        if int_mode:
            print(f"{var} has been assigned to {variables[var]}")
        return

    match = arithmetic_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operator = match.group(3)
        operand2 = match.group(4)
        perform_arithmetic(var, operand1, operator, operand2, int_mode, i)
        return

    match = boolean_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operator = match.group(3)
        operand2 = match.group(4)
        perform_boolean(var, operand1, operator, operand2, int_mode, i)
        return

    match = not_expression.match(line)
    if match:
        var = match.group(1)
        operand = match.group(2)
        perform_not(var, operand, int_mode)
        return

    match = comparison_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operator = match.group(3)
        operand2 = match.group(4)
        perform_comparison(var, operand1, operator, operand2, int_mode)
        return

    match = conditional_statement.match(line)
    if match:
        var = match.group(1)
        value = int(match.group(2))
        condition1 = match.group(3)
        do1 = match.group(4)
        condition2 = match.group(5)
        do2 = match.group(6)
        perform_conditional(var, value, condition1, do1, condition2, do2, int_mode, i)
        return

    match = while_loop.match(line)
    if match:
        condition = match.group(1)
        do_block = match.group(2)
        perform_while_loop(condition, do_block, int_mode, i)
        return

    match = print_statement.match(line)
    if match:
        var1 = match.group(1)
        var2 = match.group(2)
        var3 = match.group(3)
        print_value(var3, i)
        return

    match = grouping_expression.match(line)
    if match:
        var = match.group(1)
        operand1 = match.group(2)
        operator1  = match.group(3)
        operand2 = match.group(4)
        operand3 = match.group(5)
        operator2 = match.group(6)
        operand4 = match.group(7)
        perform_grouping(var, operand1, operand2, operator1, operand3, operator2, operand4, int_mode, i)
        return

    # If the line doesnt match anything
    if line.count('!') == 0:
        print(f"Error: This line isn't matching the language: {line}")
        print('Statemets must end with a !')
        return 
    elif has_lowercase_letter(line.split()[0]):
        print(f"Error on line {i}")
        print("Variable names must be capitals letters only!")
        return
    print(f"Error: This line isn't matching the language: {line}")

# Handles arithmetic in our language
def perform_arithmetic(var, operand1, operator, operand2, int_mode, i):
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
    
    if not isinstance(val2, int) or not isinstance(val1, int) or isinstance(val2,bool) or isinstance(val1, bool):
        print(f"Error on line - {i}")
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
    if var == "temp":
        return val
    variables[var] = val
    if int_mode:
        print(f'{var} has been assigned to {val}')
    

# Handles booleans in our language    
def perform_boolean(var, operand1, operator, operand2, int_mode, i):
   #fetch values
   v1 = variables.get(operand1, False)
   v2 = variables.get(operand2, False)

   #Perform specific boolean operation
   
   #AND operation
   if operator == '/\\':
    result = v1 and v2
    if int_mode:
        print(f'AND Operation: {var} has been assigned to {result}')
   #OR operation
   elif operator == '\\/':
    result = v1 or v2
    if int_mode:
        print(f'OR Operation: {var} has been assigned to {result}')

   else:
    print(f"Error on line - {i}")
    print(f"Unsupported boolean operator: {operator}")
    return


# Handles NOT in our language
def perform_not(var, operand, int_mode, i):
    if operand in variables.keys():
        val = variables[operand]
    elif operand == 'no':
        val = False
    elif operand == "yes":
        val = True
    if val not in [True,False]:
        print(f"Error on line - {i}")
        print("Unsupported operand type!")
        return
    variables[var] = not val
    if int_mode:
        print(f'{var} has been assigned to {not val}')

# Handles comparisons in our language
def perform_comparison(var, operand1, operator, operand2, int_mode):
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
    if int_mode:
        print(f'{var} assigned to {val}')

# Handles conditionals in our language
def perform_conditional(var, value, condition1, do1, condition2, do2, int_mode, i):
    variables[var] = value
    condition_reg = re.compile("^([A-Z]|yes|no|\d+) (greater than|less than|equals) ([A-Z]|yes|no|\d+)!")
    con1 = condition_reg.match(condition1.replace("(", "").replace(")", ""))
    print(condition1.replace("(", "").replace(")", ""))
    l = con1.group(1)
    op = con1.group(2)
    r = con1.group(3)
    if evaluate_condition(l,op, r):
        execute_line(do1.replace("(", "").replace(")", ""), int_mode,i)
    print(condition2)
    con1 = condition_reg.match(condition2.replace("(", "").replace(")", ""))
    l = con1.group(1)
    op = con1.group(2)
    r = con1.group(3)
    if evaluate_condition(l,op, r):
        execute_line(do2.replace("(", "").replace(")", ""), int_mode,i)

# Handles while loops in our language
def perform_while_loop(condition, do_block, int_mode):
    #Parse condition
    condition_operands = condition.split()
    left_operand = condition_operands[0]
    operator = condition_operands[1] + ' ' + condition_operands[2]
    right_operand = condition_operands[3]

    while evaluate_condition(left_operand,operator, right_operand):
        execute_line(do_block, int_mode, i)

#Helper Function similar to perform_comparison but returns the result directly (Instead of storing in a variable). 
def evaluate_condition(left, op, right):
    v1 = variables[left] if left in variables else int(left)
    v2 = variables[right] if right in variables else int(right)

    #Evaluate condition
    if op == "greater than":
        return v1 > v2
    elif op == "less than":
        return v1 < v2
    elif op == "equals":
        return v1 == v2
    else:
        print(f"Unsupported operator: {op}")
        return False
    
# Handles print statements in our language
def print_value(var, i):
    if var in variables:
        print(f"{variables[var]}")
    else:
        print(f"Error on line - {i}")
        print(f"Error: '{var}' does not exist")

# Handles grouping in our language
def perform_grouping(var, operand1, operand2, operator1, operand3, operator2, operand4, int_mode, i):
    temp1 = perform_arithmetic("temp", operand1, operator1, operand2)
    temp2 = perform_arithmetic("temp", operand3, operator2, operand4)
    variables[var] = temp1 + temp2
    if int_mode:
        print(f"{var} has been assigned to {temp1 + temp2}!")


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
C is opposite D!
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
C is [A plus 1] plus [B plus 2]!"""

# Testing with the example programs:
#file_path = 'Program1.py'
#with open(file_path, 'r') as file:
#    program = file.read()
    
# program = '''
# X is 5!

# X is X plus 4!
# '''

def main():
    print('Welcome!')
    inp = input('''Enter i for interactive mode or r to read code 
from a file: ''').strip()
    if inp == 'i':
        interactive_mode()
    elif inp == 'r':
        file_path = input("Please enter file path: ")
        file_path = 'invalid_3.txt'
        with open(file_path, 'r') as file:
            program = file.read()
            lines = program.split("\n")
            i = 1
            for line in lines:
                execute_line(line.strip(), False,i)
                i += 1
            print("Finished Running!")
    else:
        print("Invalid Option, exiting ...")
        return
    
def interactive_mode():
    print('Welcome to interactive mode!')
    print('Type in bye to exit')
    while True:
        x = input(":->").strip()
        print(x)
        if x == 'bye':
            return
        execute_line(x, True)
main()