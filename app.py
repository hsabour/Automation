


"""
Functions defenition
"""


#define replace function
def replace_then(list):
    for i in range(len(list)):
        if list[i] == 'THEN':
            list[i] = 'or'
            if list[i-1] != ')':
                list[i-1] =  'not ' + list[i-1]
            else:
                j = i - 1
                count = 1
                while count > 0 and j > 1:
                    if list[j - 1] == '(':
                        count = count - 1
                        if count == 0:
                            list[j - 1] = 'not ('
                    elif list[j - 1] == ')':
                        count = count + 1
                    j = j - 1
    return list
  # define a function to simplify propositional sentence and replace them with 
  # their equivalance values.

def simplify_terms(str):
        str = str.replace('not False', 'True')
        str = str.replace('not True', 'False')
        str = str.replace('True or True', 'True')
        str = str.replace('False or False', 'False')
        str = str.replace('True and True', 'True')
        str = str.replace('False and False', 'False')
        str = str.replace('False and True', 'False')
        str = str.replace('True and False', 'False')
        str = str.replace('False or True', 'True')
        str = str.replace('True or False', 'True')
        str = str.replace('( True )', 'True')
        str = str.replace('( False )', 'False')

        return str

"""Question 1"""

#reading inputs
input_file = open("q1_in.txt", "r")
output_file = open('q1 out.txt', 'w')
# seperate input lines one by another and put each line in seperate list.
# then, seperate three parts; one for The propositional variables, 
# the second one for the truth assignment and third for the propositional sentence.
# for the truth assinment parts replaces AND, OR,...words with appropriate words
# and operations.
for line in input_file:
    parts = line.split('\t')
    print(parts)

    parts[1] = parts[1].replace("F", "False").replace("T", "True")

    parts[2] = parts[2].replace('AND', 'and').replace('OR', 'or')
    parts[2] = parts[2].replace('FALSE', 'False').replace('TRUE', 'True')
    parts[2] = parts[2].replace('-', 'not')
    parts[2] = parts[2].replace('EQ', '==')

    list = parts[2].split(' ')
    list = replace_then(list)       

    parts[2] = ' '.join(list)
    print('result:')

    my_vars = parts[0].split(',')
    my_values = parts[1].split(',')
    
    #assign values to variables
    for var, val in zip(my_vars, my_values):
        parts[2] = parts[2].replace(var, val)

    print(parts[2])
    # cleanup before passing it to eval:
    # before passing to eval, for example in the string wheresver there is not
    # false turn it to True.
    while parts[2] != simplify_terms(parts[2]):
        parts[2] = simplify_terms(parts[2])
    
    print(parts[2])
    output = eval(parts[2])
    output_file.write(str(output) + '\n')
    print(output)
    print("---------------")

input_file.close()
output_file.close()

"""question 2

get_combination function. 
it makes different combinations for variables
"""

def get_combination(chars, size, combinations=[]):
    if len(combinations) == 0:
        combinations = chars
    if size == 1:
        return combinations
    
    new_combinations = []
    for combination in combinations:
        for char in chars:
            new_combinations.append(combination + char)
    
    return get_combination(chars, size - 1, new_combinations)

input_file = open("q2_in.txt", "r")
output_file = open('q2 out.txt', 'w')

for line in input_file:
    parts = line.split('\t')
    my_vars = parts[0].split(',')
    
    parts[1] = parts[1].replace('FALSE', 'False').replace('TRUE', 'True')
    parts[1] = parts[1].replace('-', 'not')
    parts[1] = parts[1].replace('AND', 'and').replace('OR', 'or')
    parts[1] = parts[1].replace('EQ', '==')
    list = parts[1].split(' ')
    list = replace_then(list)
    parts[1] = ' '.join(list)

    combo_list = get_combination(['0', '1'], len(my_vars))
    result = []
    
    print(parts[1])
    for c in combo_list:
        part1_before_eval = parts[1]
        for var, val in zip(my_vars, c):
            part1_before_eval = part1_before_eval.replace(var, str(bool(int(val))))

        # cleanup before passing it to eval:
        while part1_before_eval != simplify_terms(part1_before_eval):
            part1_before_eval = simplify_terms(part1_before_eval)
        
        print(part1_before_eval)

        output = eval(part1_before_eval)
        result.append(output)

    print(result)

    nameOfResult = 'Contradiction'
    if all(result):
        nameOfResult = 'Tautology'
    elif any(result):
        nameOfResult = 'Contingency'
    #write into the outputfile: 
    output_file.write(str(nameOfResult) + '\n')

input_file.close()
output_file.close()