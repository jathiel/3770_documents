##########################################
# Linear Programming Scripts
##########################################
#
# Johann Thiel
# ver 11.23.24
# Functions to solve linear
# programming problems.
#
##########################################

##########################################
# Generic linear programming solver that
# produces a sensitivity report
##########################################
# var   = list of variable names
# con   = list of constraint names
# ob    = list of coefficients of objective
#         functions
# M     = matrix of constraint coefficients
# c_bnd = list of constraint bounds
# v_bnd = list of variable bounds
# m     = list of inequality directions
#         +1 for <= and -1 for >=
# mx    = Boolean to determine if the 
#         problem is a maximization (True)
#         or minimization (False) problem.
#         Default is set to maximization.
# inte  = Boolean to determine if the
#         solution should be integer
#         valued. Default is for
#         continuous solutions (False).
##########################################

import numpy as np
import scipy as sp
from tabulate import tabulate

def bnd_print(arr):
    out_arr = arr.copy()
    if arr[0] == None:
        out_arr[0] = '-INF'
    else:
        out_arr[0] = str(arr[0])
    if arr[2] == None:
        out_arr[2] = 'INF'
    else:
        out_arr[2] = str(arr[2])
    return out_arr[0] + ' <= ' + out_arr[1] + ' <= ' + out_arr[2]

def lp(var, con, ob, M, c_bnd, v_bnd, m, mx=True, inte=False):
    ob = np.array(ob)
    M = np.array(M)
    c_bnd = np.array(c_bnd)
    m = np.array(m)
    integ = 1*inte
    if mx:
        res = sp.optimize.linprog(-ob, A_ub=M, b_ub=c_bnd, bounds=v_bnd, integrality=integ)
        print('MAX:', end=' ')
        #eq = ''
        #for i in range(len(ob)):
        #    if i == len(ob)-1:
        #    if ob[i]:
        #        eq += f'{ob[i]} X{i+1} + '
        #    else:
        #        print(f'{ob[i]} X{i+1} +', end=' ')
        #print(eq)
    else:
        res = sp.optimize.linprog(ob, A_ub=M, b_ub=c_bnd, bounds=v_bnd, integrality=integ)
        print('MIN:', end=' ')
        #for i in range(len(ob)):
        #    if i == len(ob)-1:
        #        print(f'{ob[i]} X{i+1}')
        #    else:
        #        print(f'{ob[i]} X{i+1} +', end=' ')
    eq = ''
    for i in range(len(ob)):
        eq += f'{ob[i]} X{i+1} + '
    print(eq[:-3])
    
    print(' ')
    print('CONSTRAINTS:')
    for i in range(len(M)):
        print('    ', end=' ')
    #    for j in range(len(M[0])):
    #        if j == len(M[0])-1:
    #            print(f'{M[i,j]} X{j+1}', end=' ')
    #        else:
    #            print(f'{M[i,j]} X{j+1} +', end=' ')
    #    print(f'<= {c_bnd[i]}')
        const = ''
        for j in range(len(M[0])):
            if M[i,j]:
                const += f'{m[i]*M[i,j]} X{j+1} + '
        print(const[:-3], end = ' ')
        if m[i] == 1:
            print(f'<= {c_bnd[i]}')
        else:
            print(f'>= {-c_bnd[i]}')
    #for i in range(len(v_bnd)):
    #    arr = [v_bnd[i][0],f'X{i+1}',v_bnd[i][1]]
    #    print('     ' + bnd_print(arr))
    #print(' ')
    #print(f'OPTIMUM VALUE FOUND AT STEP {res.nit}')
    print(' ')
    if mx:
        print(f'OBJECTIVE FUNCTION VALUE: {round(-res.fun,3)}')
    else:
        print(f'OBJECTIVE FUNCTION VALUE: {round(res.fun,3)}')
    print(' ')
    table = [['VARIABLE', 'VALUE']]
    table += [[var[i], round(res.x[i],3)] for i in range(len(var))]
    print(tabulate(table, headers="firstrow"))
    print(' ')
    table2 = [['ROW', 'SLACK', 'SHADOW PRICE']]
    if mx:
        table2 += [[con[i], 0+round(0+res.slack[i],3), round(0-res.ineqlin['marginals'][i],3)] for i in range(len(con))]
    else:
        table2 += [[con[i], 0+round(0+res.slack[i],3), round(0+m[i]*float(res.ineqlin['marginals'][i]),3)] for i in range(len(con))]
    print(tabulate(table2, headers="firstrow"))