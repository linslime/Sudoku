import pandas as pd
import numpy as np
import gurobipy

def data(a):
    return a

df = pd.read_excel(r'.\SudokuData.xlsx',sheet_name='Sheet3')
sudoku = df.values
print(sudoku)
list = np.zeros((9,9,9))
for i in range(len(sudoku)):
    for j in range(len(sudoku[1])):
        if sudoku[i][j] != 0:
            list[sudoku[i][j] - 1][i][j] = 1


MODEL = gurobipy.Model()

x = MODEL.addVars(9, 9, 9, vtype=gurobipy.GRB.BINARY, name="x")

MODEL.update()

MODEL.setObjective(0, gurobipy.GRB.MINIMIZE)

MODEL.addConstrs(gurobipy.quicksum(x[k,i,j] for k in range(9)) == data(1) for i in range(9 * data(1)) for j in range(9))
MODEL.addConstrs(gurobipy.quicksum(x[k,i,j] for i in range(9)) == 1 for k in range(9) for j in range(9))
MODEL.addConstrs(gurobipy.quicksum(x[k,i,j] for j in range(9)) == 1 for i in range(9) for k in range(9))
MODEL.addConstrs(x[k,i,j] + x[k,i,j + 1] + x[k,i,j + 2] + x[k,i + 1,j] + x[k,i + 1,j + 1] + x[k,i + 1,j + 2] + x[k,i + 2,j] + x[k,i + 2,j + 1] + x[k,i + 2,j + 2] == 1  for i in range(0,9,3) for j in range(0,9,3) for k in range(9))
MODEL.addConstrs(x[k,i,j] >= list[k,i,j] for k in range(9) for i in range(9) for j in range(9))

MODEL.Params.LogToConsole = True  # 显示求解过程
MODEL.Params.MIPGap = 0.0001  # 百分比界差
# MODEL.Params.TimeLimit = 10  # 限制求解时间为 100s
MODEL.optimize()

ans = np.zeros((9,9))
for k in range(9):
    for i in range(9):
        for j in range(9):
            if round(x[k,i,j].x) == 1:
                ans[i][j] = x[k,i,j].x * (k + 1)

print(ans)