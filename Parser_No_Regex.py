import sys

# For command line arguments
if len(sys.argv) < 2:
    print("Example Usage: python3 Parser.py ProgramFile.py")
    sys.exit(1)

file_path = sys.argv[1]
variables = {}

def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
def is_uppercase(s):
    return s.isupper() and s.isalpha()


def execute_line(line):
    if not line:
        return
    if not line.endswith('!'):
        print(f"Error: Line doesn't end with '!': {line}")
        return
    parts = line.split()
    if not parts:
        print(f"Error: Unrecognized or incomplete syntax in line: {line}")
        return
    if not is_uppercase(parts[0]):
        print(f"Error: Variable names must be uppercase letters only! Found '{parts[0]}' in line: {line}")
    if parts[0] == 'as' and parts[1] == 'long' and parts[2] == 'as':
        # While loop expression
        loop_struct = line.split(' do ')
        if len(loop_struct) != 2:
            print(f"Error: Invalid while loop format {line}")
            return
        condition_part = loop_struct[0][11:] # Remove 'as long as '
        action_part= loop_struct[1]
        if condition_part.startswith('(') and condition_part.endswith(')') and action_part.startswith('(') and action_part.endswith(')'):
            condition = condition_part[1:-1] # Remove parentheses
            action = action_part[1:-1] # Remove parentheses
            perform_while_loop(condition, action)
        else:
            print(f'Error: Invalid format in while loop: {line}')
    elif parts[1] == 'is':
        var = parts[0]
        parts[2] = parts[2].rstrip('!')
        # Integer declaration:
        if is_integer(parts[2]):
            variables[var] = int(parts[2])
        elif parts[2].startswith('"') and parts[-1].endswith('!"'):
            variables[var] = ' '.join(parts[2:])[1:-2]
        # Boolean declaration: 
        elif parts[2] in ['yes', 'no']:
            variables[var] = parts[2] == 'yes'
        # Arithmetic expression: 
        elif len(parts) == 5 and parts[3] in ['plus', 'minus', 'times', 'divided by', 'modulus']:
            operand1 = parts[2]
            if operand1 not in variables and not is_integer(operand1):
                print(f"Error: Undefined variable used in arithmetic operation: {line}")
                return
            perform_arithmetic(var, operand1, parts[3], parts[4].rstrip('!'))
        # Boolean expression
        elif len(parts) == 5 and parts[3] in ['/\\', '\\/']:
            perform_boolean(var, parts[2],parts[3], parts[4].rstrip('!'))
        # NOT expression
        elif len(parts) == 4 and parts[2] == 'opposite' and parts[3].endswith('!'):
            operand = parts[3].rstrip('!')
            perform_not(var,operand)
        # Comparison expression
        elif len(parts) == 6 and parts[3] in ['greater than', 'less than', 'equals']:
            perform_comparison(var,parts[2],parts[3], parts[4])
        # Conditional statement
        elif "when" in line and "do" in line:
            value = parts[2].rstrip('!')
            if not is_integer(value):
                print(f"Error: Invalid initial value in conditional statement: {value}")
                return
            variables[var] = int(value)

            conditional_part = line.split(f"{var} is {value}! ")[1]
            condition_pairs = conditional_part.split(' or when ')

            for condition in condition_pairs:
                try:
                    cond, action = condition.split(') do (')
                    cond = cond.strip('when (')
                    action = action.strip(')')
                    condition_parts = cond.split()
                    if len(condition_parts) == 3:
                        left, op, right = condition_parts
                        right = right.rstrip('!')
                        if evaluate_condition(left,op, right):
                            execute_line(action)
                    else:
                        print(f"Error Invalid condition format {cond}")
                except ValueError:
                    print(f"Error: Could not parse condition and action in {condition}")
            
        # Grouping Expression
        elif parts[2].startswith('[') and ']' in parts[2] and 'plus' in parts[3:5] and parts[5].startswith('[') and parts[-1].endswith(']!'):
            group1 = parts[2].strip('[]').split()
            group2 = parts[5].strip('[]').split()
            if len(group1) == 3 and len(group2) == 3 and group1[1] == 'plus' and group2[1] == 'plus':
                perform_grouping(var,group1[0], group1[2], group1[1],group2[0],group2[2], group2[1])
            else:
                print(f"Error: Invalid format for grouping expression: {line}")

    else:
        print(f"Error: Unrecognized syntax in line: {line}") 


# Handles arithmetic in our language
def perform_arithmetic(var, operand1, operator, operand2):
    # print(f"Variables: {variables}")
    # print(f"Performing Arithmetic: {var} = {operand1} {operator} {operand2}")
    # print(f"Current Variables: {variables}")
    val1 = variables.get(operand1,0) if not is_integer(operand1) else int(operand1) 
    val2 = variables.get(operand2,0) if not is_integer(operand2) else int(operand2) 
    
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
    else:
        print(f"Unsupported operator: {operator}")
        return

    variables[var] = val
    print(f'{var} has been assigned to {val}')
    

# Handles booleans in our language    
def perform_boolean(var, operand1, operator, operand2):
   # Fetch values
   v1 = variables.get(operand1, False)
   v2 = variables.get(operand2, False)

   # Make sure operands are boolean
   if not isinstance(v1,bool) or not isinstance(v2,bool):
    print(f"Error: Operands for boolean operations must be boolean values. Got {v1} and {v2}.")
    return
   
   #AND operation
   if operator == '/\\':
    result = v1 and v2
    print(f'AND Operation: {var} has been assigned to {result}')
   #OR operation
   elif operator == '\\/':
    result = v1 or v2
    print(f'OR Operation: {var} has been assigned to {result}')

   else:
    print(f"Unsupported boolean operator: {operator}")
    return

   variables[var] = result


# Handles NOT in our language
def perform_not(var, operand):
    if operand in variables:
        val = variables[operand]
    elif operand == 'no':
        val = False
    elif operand == "yes":
        val = True
    else:
        print(f"Error: Unsupported operand '{operand}' for NOT operation.")
        return
    
    # Check if operand is a boolean
    if not isinstance(val,bool):
        print("Error: Operand for NOT operation must be a boolean value.")
        return
    
    # Perform operation
    variables[var] = not val
    print(f'{var} has been assigned to {not val}')

# Handles comparisons in our language
def perform_comparison(var, operand1, operator, operand2):
    val1 = int(operand1) if operand1.isdigit() else variables.get(operand1)
    val2 = int(operand2) if operand2.isdigit() else variables.get(operand2)

    # Check if variaables are known and operands are integers
    if val1 is None:
        print(f"Unknown or non-integer variable: {operand1}")
        return
    if val2 is None:
        print(f"Unknown or non-integer variable: {operand2}")
        return 

    # Perform comparison operation
    if operator == 'greater than':
        val = val1 > val2
    elif operator == 'less than':
        val = val1 < val2
    elif operator == 'equals':
        val = val1 == val2
    else:
        print(f"Unsupported comparison operator: {operator}")
        return

    variables[var] = val
    print(f'{var} has been assigned to {val}')


# Handles conditionals in our language
def perform_conditional(var, value, condition1, do1, condition2, do2):
    variables[var] = value
    
    parts1 = condition1.strip('()').split()
    if len(parts1) == 3 and evaluate_condition(parts1[0], parts1[1], parts1[2]):
        execute_line(do1.strip('()'))

    parts2 = condition2.strip('()').split()
    if len(parts2) == 3 and evaluate_condition(parts2[0], parts2[1], parts2[2]):
        execute_line(do2.strip('()'))

def evaluate_condition(left,op,right):
    val1 = int(left) if left.isdigit() else variables.get(left)
    val2 = int(right) if right.isdigit() else variables.get(right)

    if val1 is None or val2 is None:
        print(f"Error in evaluating condition: Unknown or invalid operands '{left}' and '{right}'")
        return False

    if op == 'greater than':
        return val1 > val2
    elif op == 'less than':
        return val1 < val2
    elif op == 'equals':
        return val1 == val2
    else:
        print(f"Unsupported comparison operator in condition: {op}")
        return False

# Handles while loops in our language
def perform_while_loop(condition, do_block):
    #Parse condition
    condition_operands = condition.split()
    if len(condition_operands) != 4:
        print("Error: Invalid condition format in while loop.")
        return

    left_operand = condition_operands[0]
    operator = condition_operands[1] + ' ' + condition_operands[2]
    right_operand = condition_operands[3]

    while evaluate_condition(left_operand,operator, right_operand):
        execute_line(do_block.strip('()'))



# Handles print statements in our language
def print_value(var):
    if var in variables:
        print(f"{variables[var]}")
    elif var.isdigit():
        print(var)
    elif var.startswith('"') and var.endswith('"'):
        print(var[1:-1]) # Remove quotes
    else:
        print(f"Error: '{var}' does not exist")

# Handles grouping in our language
def perform_grouping(var, operand1, operand2, operator1, operand3, operator2, operand4):
    temp1 = perform_arithmetic1("temp", operand1, operator1, operand2)
    temp2 = perform_arithmetic1("temp", operand3, operator2, operand4)
    
    if temp1 is not None and temp2 is not None:
        variables[var] = temp1 + temp2
        print(f"{var} has been assigned to {temp1 + temp2}!")
    else:
        print(f"Error in performing grouping operation for {var}")
    
def perform_arithmetic1(var, operand1, operator, operand2):
    
    val1 = int(operand1) if operand1.isdigit() else variables.get(operand1)
    val2 = int(operand2) if operand2.isdigit() else variables.get(operand2)
    
    if val1 is None or val2 is None:
        print(f"Error: Unknown or non-integer operands '{operand1}' and '{operand2}'")
        return None


    if operator == "plus":
        return val1 + val2
    elif operator == "divided by":
        return val1 / val2
    elif operator == "times":
        return val1 * val2
    elif operator == "minus":
        return val1 - val2
    elif operator == "modulus":
        return val1 % val2
    else:
        print(f"Unsupported operator: {operator}")
        return None

# Handles executions in our language
def execute_block(block):
    lines = block.split("\n")

    for line in lines:
        trimmed_line = line.strip()
        if trimmed_line:
            execute_line(trimmed_line)

try:
    with open(file_path, 'r') as file:
        program = file.read()
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found")
    sys.exit(1)

execute_block(program)
