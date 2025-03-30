import numpy as np

class Matrix:
    def __init__(self, data):
        self.rows = data
        self.num_rows = len(data)
        self.num_cols = len(data[0]) if self.num_rows > 0 else 0

    def __add__(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Несовместимые размеры для сложения")
        result = [
            [self.rows[i][j] + other.rows[i][j] for j in range(self.num_cols)]
            for i in range(self.num_rows)
        ]
        return Matrix(result)

    def __mul__(self, other):
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Несовместимые размеры для покомпонентного умножения")
        result = [
            [self.rows[i][j] * other.rows[i][j] for j in range(self.num_cols)]
            for i in range(self.num_rows)
        ]
        return Matrix(result)

    def __matmul__(self, other):
        if self.num_cols != other.num_rows:
            raise ValueError("Несовместимые размеры для матричного умножения")
        result = []
        for i in range(self.num_rows):
            row = []
            for j in range(other.num_cols):
                sum_val = sum(
                    self.rows[i][k] * other.rows[k][j] for k in range(self.num_cols)
                )
                row.append(sum_val)
            result.append(row)
        return Matrix(result)

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.rows])

if __name__ == "__main__":
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

    # Операции
    matrix_add = matrix1 + matrix2
    matrix_mul = matrix1 * matrix2
    matrix_matmul = matrix1 @ matrix2

    # Запись в файлы
    def write_matrix(matrix, filename):
        with open(filename, 'w') as f:
            for row in matrix.rows:
             f.write(' '.join(map(str, row)) + '\n')
    
    write_matrix(matrix_add, 'artifacts/matrix_add.txt')
    write_matrix(matrix_mul, 'artifacts/matrix_mul.txt')
    write_matrix(matrix_matmul, 'artifacts/matrix_matr_mul.txt')
