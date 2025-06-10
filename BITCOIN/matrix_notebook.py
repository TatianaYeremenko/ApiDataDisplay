# Matrix Operations with NumPy - Complete Guide
# ================================================

import numpy as np
import matplotlib.pyplot as plt

print("📊 Matrix Operations with NumPy")
print("=" * 40)

# 1. BASIC MATRIX CREATION
print("\n1️⃣ BASIC MATRIX CREATION")
print("-" * 25)

# Create a 3x3 matrix
matrix_a = np.array([[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 9]])

matrix_b = np.array([[9, 8, 7],
                     [6, 5, 4],
                     [3, 2, 1]])

print("Matrix A:")
print(matrix_a)
print("\nMatrix B:")
print(matrix_b)

# 2. MATRIX PROPERTIES
print("\n2️⃣ MATRIX PROPERTIES")
print("-" * 20)

print(f"Shape of A: {matrix_a.shape}")
print(f"Size of A: {matrix_a.size}")
print(f"Data type: {matrix_a.dtype}")
print(f"Number of dimensions: {matrix_a.ndim}")

# 3. MATRIX OPERATIONS
print("\n3️⃣ MATRIX OPERATIONS")
print("-" * 21)

# Addition
print("Matrix Addition (A + B):")
addition = matrix_a + matrix_b
print(addition)

# Subtraction
print("\nMatrix Subtraction (A - B):")
subtraction = matrix_a - matrix_b
print(subtraction)

# Element-wise multiplication
print("\nElement-wise Multiplication (A * B):")
element_mult = matrix_a * matrix_b
print(element_mult)

# Matrix multiplication (dot product)
print("\nMatrix Multiplication (A @ B):")
matrix_mult = matrix_a @ matrix_b
print(matrix_mult)

# 4. MATRIX TRANSFORMATIONS
print("\n4️⃣ MATRIX TRANSFORMATIONS")
print("-" * 25)

# Transpose
print("Transpose of A:")
transpose_a = matrix_a.T
print(transpose_a)

# Reshape
print("\nReshape A to 1x9:")
reshaped = matrix_a.reshape(1, 9)
print(reshaped)

print("\nReshape A to 9x1:")
reshaped_col = matrix_a.reshape(9, 1)
print(reshaped_col)

# 5. SPECIAL MATRICES
print("\n5️⃣ SPECIAL MATRICES")
print("-" * 19)

# Identity matrix
identity = np.eye(3)
print("3x3 Identity Matrix:")
print(identity)

# Zero matrix
zeros = np.zeros((3, 4))
print("\n3x4 Zero Matrix:")
print(zeros)

# Ones matrix
ones = np.ones((2, 3))
print("\n2x3 Ones Matrix:")
print(ones)

# Random matrix
np.random.seed(42)  # For reproducible results
random_matrix = np.random.randint(1, 10, (3, 3))
print("\n3x3 Random Matrix (1-9):")
print(random_matrix)

# 6. MATRIX INDEXING & SLICING
print("\n6️⃣ MATRIX INDEXING & SLICING")
print("-" * 30)

test_matrix = np.array([[10, 20, 30],
                        [40, 50, 60],
                        [70, 80, 90]])

print("Test Matrix:")
print(test_matrix)

print(f"\nElement at [1,2]: {test_matrix[1, 2]}")
print(f"First row: {test_matrix[0, :]}")
print(f"Last column: {test_matrix[:, -1]}")
print(f"2x2 submatrix (top-left):")
print(test_matrix[0:2, 0:2])

# 7. ADVANCED OPERATIONS
print("\n7️⃣ ADVANCED OPERATIONS")
print("-" * 22)

# Determinant
det_a = np.linalg.det(matrix_a)
print(f"Determinant of A: {det_a:.2f}")

# Eigenvalues and eigenvectors
eigenvals, eigenvecs = np.linalg.eig(matrix_a)
print(f"\nEigenvalues of A: {eigenvals}")

# Matrix inverse (using a non-singular matrix)
invertible_matrix = np.array([[2, 1],
                              [1, 1]])
inv_matrix = np.linalg.inv(invertible_matrix)
print(f"\nInvertible Matrix:")
print(invertible_matrix)
print(f"Its Inverse:")
print(inv_matrix)

# 8. PRACTICAL EXAMPLES
print("\n8️⃣ PRACTICAL EXAMPLES")
print("-" * 21)

# Linear system solving: Ax = b
A = np.array([[3, 2],
              [1, 4]])
b = np.array([7, 6])

x = np.linalg.solve(A, b)
print("Solving linear system Ax = b:")
print(f"A = \n{A}")
print(f"b = {b}")
print(f"Solution x = {x}")
print(f"Verification Ax = {A @ x}")

# 9. MATRIX STATISTICS
print("\n9️⃣ MATRIX STATISTICS")
print("-" * 20)

stats_matrix = np.array([[1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 9]])

print("Matrix:")
print(stats_matrix)
print(f"\nSum of all elements: {np.sum(stats_matrix)}")
print(f"Mean: {np.mean(stats_matrix):.2f}")
print(f"Standard deviation: {np.std(stats_matrix):.2f}")
print(f"Row sums: {np.sum(stats_matrix, axis=1)}")
print(f"Column sums: {np.sum(stats_matrix, axis=0)}")

# 10. VISUALIZATION
print("\n🔟 MATRIX VISUALIZATION")
print("-" * 23)

# Create a sample matrix for visualization
viz_matrix = np.random.rand(5, 5)

plt.figure(figsize=(12, 4))

# Plot 1: Matrix as heatmap
plt.subplot(1, 3, 1)
plt.imshow(viz_matrix, cmap='viridis')
plt.title('Matrix Heatmap')
plt.colorbar()

# Plot 2: Matrix as 3D surface
ax = plt.subplot(1, 3, 2, projection='3d')
x, y = np.meshgrid(range(5), range(5))
ax.plot_surface(x, y, viz_matrix, cmap='plasma')
ax.set_title('Matrix as 3D Surface')

# Plot 3: Matrix values as bar chart
plt.subplot(1, 3, 3)
plt.bar(range(viz_matrix.size), viz_matrix.flatten())
plt.title('Matrix Values as Bars')
plt.xlabel('Element Index')
plt.ylabel('Value')

plt.tight_layout()
plt.show()

print("\n✅ Matrix operations notebook complete!")
print("🎯 Key takeaways:")
print("   • Matrices are 2D NumPy arrays")
print("   • Use @ for matrix multiplication, * for element-wise")
print("   • NumPy provides powerful linear algebra functions")
print("   • Indexing uses [row, column] notation")
print("   • Visualizations help understand matrix data")