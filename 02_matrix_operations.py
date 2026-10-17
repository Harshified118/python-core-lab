"""
02_matrix_operations.py
Category: Basic / Linear Algebra & Algorithms

Description:
A pure-Python matrix manipulation suite without external dependencies:
- Matrix addition & subtraction
- Scalar multiplication
- Matrix multiplication: O(n^3)
- Matrix transposition
- 90-degree clockwise rotation
- Determinant calculation for 2x2 and 3x3 matrices
"""

from typing import List

Matrix = List[List[float]]


def is_valid_matrix(m: Matrix) -> bool:
    if not m or not isinstance(m, list) or not m[0]:
        return False
    row_len = len(m[0])
    return all(isinstance(row, list) and len(row) == row_len for row in m)


def shape(m: Matrix) -> tuple:
    if not is_valid_matrix(m):
        raise ValueError("Invalid matrix format.")
    return len(m), len(m[0])


def add_matrices(a: Matrix, b: Matrix) -> Matrix:
    if shape(a) != shape(b):
        raise ValueError("Matrices must have identical dimensions for addition.")
    return [[a[r][c] + b[r][c] for c in range(len(a[0]))] for r in range(len(a))]


def scalar_multiply(m: Matrix, scalar: float) -> Matrix:
    if not is_valid_matrix(m):
        raise ValueError("Invalid matrix format.")
    return [[val * scalar for val in row] for row in m]


def transpose(m: Matrix) -> Matrix:
    if not is_valid_matrix(m):
        raise ValueError("Invalid matrix format.")
    rows, cols = shape(m)
    return [[m[r][c] for r in range(rows)] for c in range(cols)]


def multiply_matrices(a: Matrix, b: Matrix) -> Matrix:
    r_a, c_a = shape(a)
    r_b, c_b = shape(b)
    if c_a != r_b:
        raise ValueError(f"Cannot multiply {r_a}x{c_a} with {r_b}x{c_b} matrix.")

    result = [[0.0 for _ in range(c_b)] for _ in range(r_a)]
    for i in range(r_a):
        for j in range(c_b):
            result[i][j] = sum(a[i][k] * b[k][j] for k in range(c_a))
    return result


def rotate_90_clockwise(m: Matrix) -> Matrix:
    """Rotates matrix 90 degrees clockwise (transpose followed by row reversal)."""
    transposed = transpose(m)
    return [row[::-1] for row in transposed]


def determinant_2x2(m: Matrix) -> float:
    if shape(m) != (2, 2):
        raise ValueError("Matrix must be 2x2.")
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def determinant_3x3(m: Matrix) -> float:
    if shape(m) != (3, 3):
        raise ValueError("Matrix must be 3x3.")
    a, b, c = m[0]
    sub1 = [[m[1][1], m[1][2]], [m[2][1], m[2][2]]]
    sub2 = [[m[1][0], m[1][2]], [m[2][0], m[2][2]]]
    sub3 = [[m[1][0], m[1][1]], [m[2][0], m[2][1]]]
    return a * determinant_2x2(sub1) - b * determinant_2x2(sub2) + c * determinant_2x2(sub3)


def print_matrix(name: str, m: Matrix):
    print(f"\n{name} ({shape(m)[0]}x{shape(m)[1]}):")
    for row in m:
        formatted = " ".join(f"{val:>6.1f}" for val in row)
        print(f"  [ {formatted} ]")


def main():
    print("=== 02: Matrix Operations Demo ===")
    mat_a = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
    ]
    mat_b = [
        [7.0, 8.0],
        [9.0, 1.0],
        [2.0, 3.0],
    ]

    print_matrix("Matrix A", mat_a)
    print_matrix("Matrix B", mat_b)

    # Transposition
    mat_a_t = transpose(mat_a)
    print_matrix("Transpose of A", mat_a_t)

    # Multiplication
    prod = multiply_matrices(mat_a, mat_b)
    print_matrix("Product A * B", prod)

    # 90-degree Rotation
    square = [
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
    ]
    print_matrix("Original Square Matrix", square)
    rotated = rotate_90_clockwise(square)
    print_matrix("Rotated 90° Clockwise", rotated)

    # Determinant
    det_3x3_matrix = [
        [6.0, 1.0, 1.0],
        [4.0, -2.0, 5.0],
        [2.0, 8.0, 7.0],
    ]
    print_matrix("Matrix for Determinant", det_3x3_matrix)
    det = determinant_3x3(det_3x3_matrix)
    print(f"\nDeterminant: {det:.2f} (Expected: -306.0)")


if __name__ == "__main__":
    main()
