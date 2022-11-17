import re
import itertools
import os


def menu():
    k = input("\nPress E to exit / Press R to restart\n").upper()
    if k == 'E':
        pass
    elif k == 'R':
        os.system("python main.py")
    else:
        print("Invalid input")
        menu()


t = input("Press 1 for checking wff; ❤️🥸😤 \n"
          "Press 2 for checking value under interpretation; 😼🤖🤡\n"
          "Press 3 for checking if valid / satisfiable: 🤣😜🤠\n"
          "Press 4 for constructing the truth table: 🤩🐶🦍\n"
          "Press 5 for checking the logical equivalence of two propositions: 🍕🎃🛻\n"
          "Press 6 for checking the logical consequence: 🐔🎅🤙\n")

try:
    if 0 < int(t) < 7:
        if int(t) == 6:
            p_num = int(input("Enter the number of propositions: "))
            formula = '(('
            p_cont = 0
            for i in range(p_num):
                formula += str(input("Enter proposition: ")).replace(" ", "")
                if i < p_num - 1:
                    formula += '∧'
                    if i < p_num - 2:
                        formula += '('
                        p_cont += 1
            cons = str(input("Enter the consequence: "))
            formula += ')' * p_cont + ')⇒' + cons + ')'
            formula.replace(" ", "")
            print("The final formula is:" + formula)
            menu()
        else:
            formula = str(input("Enter proposition: ")).replace(" ", "")
        if int(t) == 2:
            interpretation = input("Enter interpretation: ").replace(" ", "")
            inter = {'0': 0, '1': 1}
            for i in range(len(interpretation)):
                if 'A' <= interpretation[i] <= 'Z':
                    if interpretation[i - 1] == '¬':
                        inter[interpretation[i]] = 0
                    else:
                        inter[interpretation[i]] = 1
            print(inter)
        elif int(t) == 3 or int(t) == 4 or int(t) == 5:
            valid = 1
            satisfiable = 0
            values = {'1': 1, '0': 0}
            pr1 = []
            pr2 = []
            check_5 = False
    else:
        raise ValueError
except ValueError:
    print("Invalid input")
    os.system("python main.py")

proposition_pattern = re.compile("[(][A-Z01][⇒∨⇔∧][A-Z01][)]")
negation_pattern = re.compile("[(][¬][A-Z01][)]")

and_pattern = re.compile("[(][A-Z01][∧][A-Z01][)]")
or_pattern = re.compile("[(][A-Z01][∨][A-Z01][)]")
implication_pattern = re.compile("[(][A-Z01][⇒][A-Z01][)]")
equivalence_pattern = re.compile("[(][A-Z01][⇔][A-Z01][)]")


def replace_value(s, i):
    if s[2] == '∧':
        return str(int(i[s[1]]) and i[s[3]])
    elif s[2] == '∨':
        return str(int(i[s[1]]) or int(i[s[3]]))
    elif s[2] == '⇒':
        return str(int(not i[s[1]] or i[s[3]]))
    elif s[2] == '⇔':
        return str(int(i[s[1]] == i[s[3]]))
    elif s[1] == '¬':
        return str(int(not i[s[2]]))


def value_under_interpretation(f, j):
    if int(t) == 2:
        f = list(f)
        for ch in range(len(f)):
            if f[ch] in j:
                f[ch] = str(j[f[ch]])
        f = "".join(f)
        print(f)
    while True:
        prop = re.search(proposition_pattern, f).group()
        if prop[2] == '∧':
            f = re.sub(and_pattern, replace_value(prop, j), f, count=1)
        elif prop[2] == '∨':
            f = re.sub(or_pattern, replace_value(prop, j), f, count=1)
        elif prop[2] == '⇒':
            f = re.sub(implication_pattern, replace_value(prop, j), f, count=1)
        elif prop[2] == '⇔':
            f = re.sub(equivalence_pattern, replace_value(prop, j), f, count=1)
        if int(t) == 2:
            print(f)
        negs = re.findall(negation_pattern, f)
        for neg in negs:
            f = re.sub(negation_pattern, replace_value(neg, j), f, count=1)
            if int(t) == 2:
                print(f)
        if f == '0' or f == '1':
            return f


if int(t) == 1:
    # check wff
    ok2 = 0
    if 'A' <= formula <= 'Z':
        ok2 = 1
    while True:
        ok = 0
        test = formula[:]
        formula = re.sub(negation_pattern, 'N', formula)
        formula = re.sub(proposition_pattern, 'P', formula)
        if test != formula:
            ok = 1
            print(formula)
        if test == 'N' or test == 'P' or ok2 == 1:
            print("Well formed formula, congrats! ❤")
            menu()
            break
        elif ok == 0:
            print("Not wff, failure! 💔")
            menu()
            break
elif int(t) == 2:
    # check under interpretation
    aux = True
    if value_under_interpretation(formula, inter) == '0':
        aux = False
    print("The value of the proposition under the given interpretation is: " + str(aux))
    menu()
elif int(t) == 3 or int(t) == 4 or int(t) == 5:
    # construct table and check valid / satisfiable
    check = 1
    while check == 1:
        for i in range(len(formula)):
            if 'A' <= formula[i] <= 'Z':
                values[formula[i]] = 0
        truth = [0, 1]
        combinations = list(itertools.product(truth, repeat=(len(values) - 2)))
        if int(t) == 4:
            for column in sorted(values):
                if column != '1' and column != '0':
                    print(column, end=' ')
            alignment = "{:" + str(int((len(formula) / 2 + 1))) + "d}"
            print(str(formula))
        for combi in combinations:
            i = 0
            for value in combi:
                key = sorted(values)[i + 2]
                values[key] = value
                i += 1
            if int(t) == 4:
                # construct (show) truth table
                for column in sorted(values):
                    if column != '1' and column != '0':
                        print(values[column], end=' ')
            if value_under_interpretation(formula, values) == '0':
                valid = 0
                if int(t) == 4:
                    print(alignment.format(0))
                elif int(t) == 5:
                    if check_5 is False:
                        pr1.append(0)
                    else:
                        pr2.append(0)
            elif value_under_interpretation(formula, values) == '1':
                satisfiable = 1
                if int(t) == 4:
                    print(alignment.format(1))
                elif int(t) == 5:
                    if check_5 is False:
                        pr1.append(1)
                    else:
                        pr2.append(1)
        check = 0
        if valid == 0:
            aux1 = 'invalid'
        else:
            aux1 = 'valid'
        if satisfiable == 0:
            aux2 = 'unsatisfiable'
        else:
            aux2 = 'satisfiable'
        if int(t) == 3:
            print("The proposition is {} and {}".format(aux1, aux2))
        elif int(t) == 5 and check_5 is False:
            values = {'1': 1, '0': 0}
            check = 1
            check_5 = True
            formula = str(input("Enter another proposition: ")).replace(" ", "")
    if int(t) == 5:
        if pr1 == pr2:
            print("The propositions are logical equivalent 😍")
        else:
            print("The propositions are not logical equivalent 😱")
    menu()
