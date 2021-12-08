import string
import sys
import os
import ast





def SemicolonChek(words=''):
    fl = False

    if words.endswith(';\n') and '#' not in words:
        fl = True
    else:
        jj = 0
        for i in range(len(words)):
            if words[i] == '#':
                jj = i
        for i in range(len(words)):
            if words[i] == ';' and jj > i:
                fl = True
    return fl


def Probel4(words, path, i, fl):
    if words.startswith(' '):
        jj = 0
        for ii in range(9):  # len(char)
            if words[ii] == ' ':
                jj += 1

        if jj % 4 != 0 and not fl:
            print(f'{path}: Line {i + 1}: S002 Indentation is not a multiple of four')


def TwoSpaces(word, path, i):
    char = word
    if not char.startswith('#'):
        fl = False
        for ii in range(len(char)):
            if char[ii] == '#' and (char[ii - 1] == ' ' and char[ii - 2] == ' '):
                fl = True

            if char[ii] == '#' and (char[ii - 1] != ' ' or char[ii - 2] != ' ') and not fl:
                print(f'{path}: Line {i + 1}: S004 At least two spaces required before inline comments')


def ManySpaces(string, path, i):
    if string.startswith('class'):
        if string[6] == ' ':
            print(f"{path}: Line {i + 1}: S007 Too many spaces after 'class'")
    else:
        if string[4] == ' ':
            print(f"{path}: Line {i + 1}: S007 Too many spaces after 'def'")
            return True


def ClassNames(string, path, i):
    # [S008] Class name class_name should be written in CamelCase;
    s = string.split(' ')
    # print(s[1])
    s = s[1].split(':')
    # print(s[0])
    if '(' in s[0]:
        s = s[0].split('(')
    s = s[0]
    # print(s) # class name
    count = 0
    for char in s:
        if char.isupper():
            count += 1
    if count < 1 and s != '':
        print(f"{path}: Line {i + 1}: S008 Class name '{s}' should be written in CamelCase")


def DefNames(stringg, path, i):
    stringg = stringg.split('def')[1]
    stringg = stringg.split('(')[0]
    fl = False
    for ii in stringg:
        if ii in string.ascii_uppercase:
            fl = True

    if fl:
        print(
            f'{path}: Line {i + 1}: S009 Function name {stringg.split("(")[0].split(" ")[1]} should be written in snake_case')


def TwoEnters(strings):
    var = []
    for i in range(len(strings) - 2):
        if strings[i] == '\n' and strings[i + 1] == '\n' and strings[i + 2] == '\n':
            var.append(i + 3)
    return var


def OpenFile(user_input=''):
    out_list = []
    if '.py' not in user_input:
        file_names = os.listdir(user_input)
        for file_name in file_names:
            if '.py' in file_name:
                out_list.append(file_name)
        return sorted(out_list)
    return user_input



def DefValueChek(input_strings, i):
    out = []

    if i + 3 < len(input_strings):
        b = i + 3
    else:
        b = len(input_strings)

    for ii in range(i, b):
        if ' = ' in input_strings[ii]:
            variable = input_strings[ii].strip(' ').split(' = ')[0]#[0].strip()
            #print(variable, 'line=', i+2)
            if variable[0] in string.ascii_uppercase:
                out.append(variable)
    return out



def DefArgsChek(line, path, i, input_strings):
    line = line.strip(' ')
    tree = ast.parse(line + '\n    pass')

    s011_error = DefValueChek(input_strings, i)
    #s011_error_len = len(s011_error)
    #print(s011_error, 'on line ', i + 2)

    function = tree.body[0].args

    for aa in function.args:  # args.args:  # name of args
        arg_name = aa.arg
        for a in aa.arg:
            if a in string.ascii_uppercase:
                print(f"{path}: Line {i + 1}: S010 Argument name '{arg_name}' should be snake_case")

# here s011
    #DefValueChek(path)
    #print(s011_error)
    #print(s011_error, 'on line ', i + 2)
    if s011_error:
        print(f"{path}: Line {i+2}: S011 Variable '{s011_error}' in function should be snake_case")


    for bb in function.defaults:
        if not isinstance(bb, ast.Constant):  # not const
            print(f'{path}: Line {i + 1}: S012 The default argument value is mutable.')


def ErrorFunc(file_name):
    # file_name = OpenFile(user_input)
    file = open(file_name, 'r')
    input_strings = file.readlines()
    fl = False
    for i in range(len(input_strings)):
        if len(input_strings[i]) > 79:
            print(f'{file_name}: Line {i + 1}: S001 Too long')

        Probel4(input_strings[i], file_name, i, fl)

        if ';' in input_strings[i]:
            if SemicolonChek(input_strings[i]):
                print(f'{file_name}: Line {i + 1}: S003 Unnecessary semicolon')

        if '#' in input_strings[i]:
            TwoSpaces(input_strings[i], file_name, i)

        if 'todo' in input_strings[i].lower() and '#' in input_strings[i]:  # and not input_strings[i].startswith('#'):
            print(f'{file_name}: Line {i + 1}: S005 TODO found')

        if i in TwoEnters(input_strings) and input_strings[i] != '\n':  # == '\n':
            print(f'{file_name}: Line {i + 1}: S006 More than two blank lines used before this line')

        if 'class' in input_strings[i]:  # or 'def' in input_strings[i]:
            ManySpaces(input_strings[i], file_name, i)
            ClassNames(input_strings[i], file_name, i)
            fl = True

        if 'def' in input_strings[i]:
            hh = 'def' + input_strings[i].split('def')[1]
            ff = ManySpaces(hh, file_name, i)
            DefNames(input_strings[i], file_name, i)
            fl = True
            DefArgsChek(input_strings[i], file_name, i, input_strings)

args = sys.argv
user_input = args[1]

if type(OpenFile(user_input)) is not str:

    for file_name in OpenFile(user_input):
        ErrorFunc(user_input + '/' + OpenFile(file_name))
else:
    ErrorFunc(OpenFile(user_input))
