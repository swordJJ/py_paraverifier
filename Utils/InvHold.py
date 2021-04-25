#author: Hongjian Jiang
from type import *
from smt2 import *
import re

def weakprecondition(statement, formula):
    '''
    :param statement: assignment or parallel assigement
    :param formula: given invariant formula
    :return: the string of the weakest precondtion
    '''
    #judge the type of the given statement
    resultFormula = FChaos()
    varsInformula = formula.getVars()
    if statement.isAssign():
        #single assign condition
        var = statement.getVar()
        exp = statement.getExp()
        if not str(var) in varsInformula: #assignment has no affection on formula
            resultFormula = str(formula)
        else:#has side effection
            resultFormula = (str(formula).replace(str(var),str(exp)))
    else:
        #parall assignment condition
        vars = statement.getVars()
        exps = statement.getExps()
        for i,v in enumerate(vars):
            if v in varsInformula:
                resultFormula= (str(formula).replace(v,exps[i]))
    return resultFormula


def invHoldCondition(statement, formula):
    '''
    :param statement: the statement of the guarded command
    :param formula: the invariant formula
    :return: the condition of which invhold meets
    '''
    smt2 = SMT2("x = Int('x') y = Int('y')")
    wp = weakprecondition(statement,formula)
    if smt2.check("solve(x > 2, y < 10, x + 2*y == 7)") == "sat":
        print("sat")
        flag = 1
    elif wp == formula:
        flag = 2
    else:
        flag = 3
    return flag


def invHoldForCondition3(guard, formula):
    '''
    :param guard: the formula of the guard command
    :param formula: the formula of the weakest precondition
    :return: the disconjunction of the guard and the formula
    '''
    negg = FNeg(guard)
    guard_str=re.findall(r'[(](.*)[)]', str(negg), re.S)
    formula_str=re.findall(r'[(](.*)[)]', str(formula), re.S)
    guard_str.append(formula_str[0])
    result = " & ".join(guard_str)
    return "!("+result+")"


if __name__ == '__main__':
    statement = SAssign(Var("n",[1]),EVar("C"))
    statement1 = SAssign("x",FChaos())
    formula = FNeg(FAndlist([FEqn(EVar(Var("n",[1])),EConst(Strc("C"))),FEqn(EVar(Var("n",[2])),EConst(Strc("C")))]))
    statement2 = SParallel([statement, statement1])
    wp = weakprecondition(statement2,formula)
    guard = FAndlist([FEqn(EVar(Var("n",[1])),EConst(Strc("T"))),FEqn(EVar(Var("x",[])),EConst(Boolc("True")))])
    print(invHoldForCondition3(guard, wp))