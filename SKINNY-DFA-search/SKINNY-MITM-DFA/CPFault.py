from abc import ABCMeta, abstractmethod
from functools import reduce
import math
import random

match_rule = [
(2, 0, 2, 0, -1, -1, -1, -1, 0),
(-1, 0, 0, 0, 0, 0, -1, 0, 1),
(0, 0, -1, 0, 0, -1, 0, 0, 1),
(0, 0, 0, -1, -1, 0, 0, 0, 1),
(0, 0, 0, 0, 1, 1, 1, -1, 0),
(0, 0, 0, 0, 1, -1, -1, 1, 0),
(0, 0, 0, 0, -1, 1, 1, 1, 0),
(0, -1, 0, 0, 0, 0, -1, 0, 1)
]

split_rule = [(1, 1, 1, 0, 0, 0, 0, 1, -2, -2, -2, -1, 0),
(-1, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, 2),
(-1, -1, 1, 0, 0, 0, -2, -1, 2, 2, 0, 1, 0),
(0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0),
(1, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0),
(0, 0, 0, -1, 0, 0, 0, 1, 0, 0, 0, 1, 0),
(0, 0, 0, 1, 0, 0, 0, -1, 0, 0, 0, -1, 0),
(-1, -1, -1, 0, 0, 0, 0, -1, 2, 2, 2, 1, 0),
(0, -1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0),
(-1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0),
(1, 1, -1, 0, 0, 0, 2, 1, -2, -2, 0, -1, 0)]


MC_rule = [(1, 0, 0, 0, 0, -1, 0, 0, 0),
(-1, 0, 0, 0, 0, 1, 0, 0, 0),
(0, 0, 0, 0, 1, 0, 0, -1, 0),
(0, 0, -1, 0, 0, 0, 0, 1, 0),
(0, -1, 0, 0, 0, 0, 1, 0, 0),
(0, 0, 0, 0, 0, -1, 0, 1, 0),
(0, 1, 1, 0, 0, 0, -1, 0, 0),
(0, 0, -1, 0, 0, 0, 1, 0, 0),
(0, 0, 1, 0, 0, 1, 0, -1, 0),
(0, 0, 0, -1, 1, 0, 0, 0, 0),
(0, 0, 0, 1, -1, 0, 0, 1, 0)]


MC_guess = [(0, 0, 0, 1, -1, 0, 0, 0, 0),
(0, 0, 0, -1, 1, 0, 0, 0, 0),
(0, 1, 0, 0, 0, 0, -1, 0, 0),
(0, -1, 0, 0, 0, 0, 1, 0, 0),
(0, 0, 0, 0, 0, 0, -1, 1, 0),
(-1, 0, 0, 0, 0, 1, 0, 0, 0),
(0, 0, -1, 0, 0, 0, 0, 1, 0),
(0, 0, 0, 0, 0, 1, -1, 0, 0),
(1, 0, 1, 0, 0, -1, 1, 0, 0),
(0, 0, -1, 0, 0, 1, 0, 0, 0),
(0, 0, 0, -1, 0, 0, 0, 1, 0),
(0, 0, 1, 1, 0, 0, 1, -1, 0)]


merge_rule=[(0, 1, 0, -1, 0),
(1, 0, -1, 0, 0),
(0, -1, 1, 1, 0),
(-1, 0, 1, 1, 0)]

orm_rule = [(1, 0, -1, 0),
(-1, 1, 1, 0),
(0, -1, -1, 1)]

class BasicTools:

    @staticmethod
    def plusTerm(in_vars):
        t = ''
        for v in in_vars:
            t = t + v + ' + '
        return t[0:-3]

    @staticmethod
    def MinusTerm(in_vars):
        t = ''
        for v in in_vars:
            t = t + v + ' - '
        return t[0:-3]

    @staticmethod
    def getVariables_From_Constraints(C):
        V = set([])
        for s in C:
            temp = s.strip()
            temp = temp.replace('+', ' ')
            temp = temp.replace('-', ' ')
            temp = temp.replace('>=', ' ')
            temp = temp.replace('<=', ' ')
            temp = temp.replace('=', ' ')
            temp = temp.split()
            for v in temp:
                if not v.isdecimal():
                    V.add(v)
        return V

    @staticmethod
    def genFromConstraintTemplate(vars_list, ineq_template):
        """
        Example:
            genFromConstraintTemplate(['x0', 'x1'], ['y0'], [(-1, 2, 3, 1), (1, -1, 0, -2)] )
            ['-1 x0 + 2 x1 + 3 y0 >= - 1', '1 x0 - 1 x1 + 0 y0 >= 2']
            genFromConstraintTemplate(['x0', 'x1'], ['y0'], [(-1, 2, 3, 1), (-1, -1, 0, -2)] )
            ['-1 x0 + 2 x1 + 3 y0 >= - 1', '-1 x0 - 1 x1 + 0 y0 >= 2']
        """
        assert ineq_template != list([])
        assert (len(vars_list)) == (len(ineq_template[1]) - 1)

        constraints = list([])
        for T in ineq_template:
            s = str(T[0]) + ' ' + vars_list[0]
            for j in range(1, len(vars_list)):
                if T[j] >= 0:
                    s = s + ' + ' + str(T[j]) + ' ' + vars_list[j]
                elif T[j] < 0:
                    s = s + ' - ' + str(-T[j]) + ' ' + vars_list[j]
            s = s + ' >= '
            if T[-1] <= 0:
                s = s + str(-T[-1])
            elif T[-1] > 0:
                s = s + '- ' + str(T[-1])
            constraints.append(s)
        return constraints


class MITMPreConstraints:

    @staticmethod
    def MC_constraint(x0,x1,x2,x3,y0,y1,y2,y3):
        varlist=[]
        varlist = varlist + [x0]
        varlist = varlist + [x1]
        varlist = varlist + [x2]
        varlist = varlist + [x3]
        varlist = varlist + [y0]
        varlist = varlist + [y1]
        varlist = varlist + [y2]
        varlist = varlist + [y3]
        constr = []
        constr += BasicTools.genFromConstraintTemplate(varlist, MC_rule)
        return constr

    @staticmethod
    def split_constraint(x0,x1,x2,x3,y10,y11,y12,y13,y20,y21,y22,y23):
        varlist = []
        varlist = varlist + [x0]
        varlist = varlist + [x1]
        varlist = varlist + [x2]
        varlist = varlist + [x3]
        varlist = varlist + [y10]
        varlist = varlist + [y11]
        varlist = varlist + [y12]
        varlist = varlist + [y13]
        varlist = varlist + [y20]
        varlist = varlist + [y21]
        varlist = varlist + [y22]
        varlist = varlist + [y23]
        constr = []
        constr += BasicTools.genFromConstraintTemplate(varlist, split_rule)
        return constr

    @staticmethod
    def Match_constraint(x0, x1, x2, x3, y0, y1, y2, y3):
        varlist = []
        varlist = varlist + [x0]
        varlist = varlist + [x1]
        varlist = varlist + [x2]
        varlist = varlist + [x3]
        varlist = varlist + [y0]
        varlist = varlist + [y1]
        varlist = varlist + [y2]
        varlist = varlist + [y3]
        constr = []
        constr += BasicTools.genFromConstraintTemplate(varlist, match_rule)
        return constr

    @staticmethod
    def MCguess_constraint(x0, x1, x2, x3, y0, y1, y2, y3):
        varlist = []
        varlist = varlist + [x0]
        varlist = varlist + [x1]
        varlist = varlist + [x2]
        varlist = varlist + [x3]
        varlist = varlist + [y0]
        varlist = varlist + [y1]
        varlist = varlist + [y2]
        varlist = varlist + [y3]
        constr = []
        constr += BasicTools.genFromConstraintTemplate(varlist, MC_guess)
        return constr

    @staticmethod
    def Mergelist(xin, yin, xout, yout):
        varlist=[]
        varlist = varlist + [xin]
        varlist = varlist + [yin]
        varlist = varlist + [xout]
        varlist = varlist + [yout]
        constr = []
        constr += BasicTools.genFromConstraintTemplate(varlist, merge_rule)
        return constr

    @staticmethod
    def OR_constraint(X,var):
        constr = []
        for i in range(0, len(X)):
            constr = constr + [var + ' - ' + X[i] + ' >= 0']
        constr = constr + [BasicTools.plusTerm(X) + ' - ' + var + ' >= 0']
        constr = constr + [var + ' <= 1']
        return constr

    @staticmethod
    def ORm_constraint(x, y, z):
        varlist = []
        varlist = varlist + [x]
        varlist = varlist + [y]
        varlist = varlist + [z]
        constr = []
        constr += BasicTools.genFromConstraintTemplate(varlist, orm_rule)
        return constr


    @staticmethod
    def equalConstraints(x, y):
        assert len(x) == len(y)
        c = []
        for i in range(0, len(x)):
            c = c + [x[i] + ' - ' + y[i] + ' = 0']
        return c

def SR(A):
    return [A[0], A[1], A[2], A[3], A[7], A[4], A[5], A[6], A[10], A[11], A[8], A[9], A[13], A[14], A[15], A[12]]

def key_perm(A):
    return [A[9], A[15], A[8], A[13], A[10], A[14], A[12], A[11], A[0], A[1], A[2], A[3], A[4], A[5], A[6], A[7]]

def lastroundtotk(A):
    return [A[14], A[12], A[13], A[8], A[11], A[9], A[15], A[10], A[5], A[6], A[3], A[2], A[7], A[0], A[1], A[4]]

def perm(A):
    return [A[1], A[0], A[2], A[3]]
if __name__ == '__main__':
    x0 = 'a'
    x1 = 'b'
    x2 = 'c'
    x3 = 'd'
    y0 = 'e'
    y1 = 'f'
    y2 = 'g'
    y3 = 'h'
    x = ['a','b','c','d']
    y=['a1','b1','c1','d1']
    S=[]
    S.append(x)
    S.append(y)
    S[0]=perm(S[0])
    print(S)
    a = MITMPreConstraints.MC_constraint(x0,x1,x2,x3,y0,y1,y2,y3)

    for i in a:
        print(i)