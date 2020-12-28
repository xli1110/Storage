# Linear Programming
1 The Simplex Method \n
Solve the standard linear programming problem:
maximize c^{T}x
s. t. Ax <= b and x >= 0
by the simplex method.

Remind, enter A, b as usually, but enter -c into the varible c.
For example, try to minimize
x_{1} + x_{2}
s. t. ([1, 2], [3, 4])x <= (5, 6) and x >= 0
Then, 
    A = np.array([
        [1, 2], 
        [3, 4],
    ])
    b = np.array([5, 6])
    c = np.array([-1, -1])
.
