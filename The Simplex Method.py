import numpy as np


def simplex(A, b, c, r, t, v):
    """
    The Simplex Method with Regard to a Standard Problem
    - Initialize the Optimal Value v as 0
    - Determine tehe Current Case
    - Pivot until It Reaches the Base Case
    - Conclude the Final Results
    """

    M = np.shape(A)[0]
    N = np.shape(A)[1]

    """Determine Cases"""
    case = case_determination(b, c)

    if case == 1:  # Base Case
        solution(M, N, b, c, r, t, v)
        return
    else:  # Recursive Case
        h, k = pivot_index(A, b, c, M, N, case)
        if h < 0 or k < 0:
            # Protection
            # The problem can be infeasible or unbounded.
            return
        else:
            A, b, c, r, t, v = pivot(A, b, c, r, t, M, N, v, h, k)
            return simplex(A, b, c, r, t, v)


def case_determination(b, c):
    """Determine the Current Case in Terms of b and c."""

    # Case 1
    if b.min() >= 0 and c.min() >= 0:
        return 1
    # Case 2
    if b.min() >= 0 and c.min() < 0:
        return 2
    # Case 3
    if b.min() < 0:
        return 3


def pivot_index(A, b, c, M, N, case):
    """Find the pivot A[h, k] in cases 2 or 3."""

    """Case 2"""
    if case == 2:
        """Find the Column Index k"""
        for j in range(N):
            if c[j] < 0:
                k = j
                break

        """Find the Row Index h"""
        # Compute the values of b[i] / A[i, k]
        h_value = []
        h_index = []
        for i in range(M):
            if A[i, k] > 0:
                h_value.append(b[i] / A[i, k])
                h_index.append(i)

        if h_value:
            h = h_index[h_value.index(min(h_value))]
        else:
            # Protection
            print("The standard problem is unbounded feasible.")
            return -1, -1

        return h, k

    """Case 3"""
    if case == 3:
        """Find the First Negative Row in b"""
        for i in range(M):
            if b[i] < 0:
                f = i
                break

        """Find the Column Index k"""
        k = -1
        for j in range(N):
            if A[f, j] < 0:
                k = j
                break
        # Protection
        if k == -1:
            print("The standard problem is infeasible.")
            return -1, -1

        """Find the Row Index h"""
        # Compute the values of b[i] / A[i, k]
        f_value = b[f] / A[f, k]
        h_value = []
        h_index = []
        for i in range(N):
            if b[i] >= 0 and A[i, k] > 0:
                h_value.append(b[i] / A[i, k])
                h_index.append(i)

        if not h_value:
            h = f
        else:
            if f_value < min(h_value):
                h = f
            else:
                h = h_index[h_value.index(min(h_value))]

        return h, k


def pivot(A, b, c, r, t, M, N, v, h, k):
    """Pivot the Simplex Tableau"""

    """Combine Matrices"""
    S = np.empty((M + 1, N + 1))
    S[:M, :N] = A
    S[:M, N] = b
    S[M, :N] = c
    S[M, N] = v

    """Pivot Operation"""
    S_hat = np.empty((M + 1, N + 1))
    p = S[h, k]
    for i in range(M + 1):
        for j in range(N + 1):
            if i == h and j == k:
                S_hat[i, j] = 1 / p
            if i == h and j != k:
                S_hat[i, j] = S[h, j] / p
            if i != h and j == k:
                S_hat[i, j] = -S[i, k] / p
            if i != h and j != k:
                S_hat[i, j] = S[i, j] - S[h, j] * S[i, k] / p

    """Decompose Matrix"""
    A = S_hat[:M, :N]
    b = S_hat[:M, N]
    c = S_hat[M, :N]
    v = S_hat[M, N]

    """Pivot r and t"""
    swap = np.empty((1, 2))
    swap[0, :] = r[k]
    r[k] = t[h]
    t[h] = swap

    return A, b, c, r, t, v


def solution(M, N, b, c, r, t, v):
    """Process r, t, b, and c to find the solution(optimal vector/value)."""

    """The Standard Problem"""
    print("Optimal Vector x for the Primal:")
    for i in range(M):
        if t[i, 0] == 0:
            print("x_" + str(int(t[i, 1])) + " = " + str(b[i]))
    for j in range(N):
        if r[j, 0] == 0:
            print("x_" + str(int(r[j, 1])) + " = 0")

    """The Dual Problem"""
    print("Optimal Vector y for the Dual:")
    for i in range(M):
        if t[i, 0] == 1:
            print("y_" + str(int(t[i, 1])) + " = 0")
    for j in range(N):
        if r[j, 0] == 1:
            print("y_" + str(int(r[j, 1])) + " = " + str(c[j]))

    """Value"""
    print("The Optimal Value: " + str(v))

    return


def initialization(A):
    """Initialize r, t, and v"""

    M = np.shape(A)[0]
    N = np.shape(A)[1]

    """
    r & t
    - The First Column: 0 denotes x; 1 denotes y.
    - The Second Column: Denotes the subscript of x or y.
    """
    r = np.empty((N, 2))
    r[:, 0] = 0
    r[:, 1] = range(1, N + 1)

    t = np.empty((M, 2))
    t[:, 0] = 1
    t[:, 1] = range(1, M + 1)

    v = 0

    return r, t, v


"""Test Samples"""
if __name__ == '__main__':
    # Sample 1
    A = np.array([
        [2, 1, -7],
        [-1, 0, 4],
        [1, 2, -6],
    ])
    b = np.array([3, -1, 2])
    c = np.array([1, -2, -1])

    # Sample 2
    A = np.array([
        [1, -1, -2, -1],
        [2, 0, 1, -4],
        [-2, 1, 0, 1],
    ])
    b = np.array([4, 2, 1])
    c = np.array([-1, 2, 3, 1])

    # Sample 3
    A = np.array([
        [-3, 3, 1],
        [2, -1, -2],
        [-1, 0, 1],
    ])
    b = np.array([3, 1, 1])
    c = np.array([1, 1, -2])

    # Implementation
    r, t, v = initialization(A)
    simplex(A, b, c, r, t, v)
