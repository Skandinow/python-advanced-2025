import numpy as np


# Миксины
class ArithmeticMixin:
    def __add__(self, other):
        if self.data.shape != other.data.shape:
            raise ValueError("Несовместимые размеры для сложения")
        return self.__class__(self.data + other.data)

    def __mul__(self, other):
        if self.data.shape != other.data.shape:
            raise ValueError("Несовместимые размеры для умножения")
        return self.__class__(self.data * other.data)

    def __matmul__(self, other):
        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("Несовместимые размеры для матричного умножения")
        return self.__class__(self.data @ other.data)


class FileIOMixin:
    def write_to_file(self, filename):
        np.savetxt(filename, self.data, fmt="%d")


class PrettyPrintMixin:
    def __str__(self):
        return np.array_str(self.data)


class PropertiesMixin:
    @property
    def rows(self):
        return self.data.shape[0]

    @property
    def cols(self):
        return self.data.shape[1]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value


# Основной класс
class Matrix(ArithmeticMixin, FileIOMixin, PrettyPrintMixin, PropertiesMixin):
    def __init__(self, data):
        self.data = np.array(data)


if __name__ == "__main__":
    np.random.seed(0)
    matrix1 = Matrix(np.random.randint(0, 10, (10, 10)))
    matrix2 = Matrix(np.random.randint(0, 10, (10, 10)))

    matrix_add = matrix1 + matrix2
    matrix_mul = matrix1 * matrix2
    matrix_matmul = matrix1 @ matrix2

    matrix_add.write_to_file("artifacts/matrix_add.txt")
    matrix_mul.write_to_file("artifacts/matrix_mul.txt")
    matrix_matmul.write_to_file("artifacts/matrix_matr_mul.txt")