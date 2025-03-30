import numpy as np


class HashMixin:
    def __hash__(self):
        total_sum = np.sum(self.data)
        return int(total_sum + self.rows * self.cols)

class CacheMixin:
    _cache = {}

    @classmethod
    def invalidate_cache(cls):
        cls._cache = {}


class Matrix(HashMixin, CacheMixin):
    def __init__(self, data):
        self.data = np.array(data)
        self.rows, self.cols = self.data.shape

    def __hash__(self):
        total_sum = np.sum(self.data)
        return int(total_sum + self.rows * self.cols)

    def __matmul__(self, other):
        if self.cols != other.rows:
            raise ValueError("Несовместимые размеры для умножения")

        return Matrix(self.data @ other.data)

    def __eq__(self, other):
        return np.array_equal(self.data, other.data)

    def save(self, filename):
        np.savetxt(filename, self.data, fmt="%d")


# Поиск коллизий
def find_collision():
    np.random.seed(0)
    while True:
        A = Matrix(np.random.randint(0, 5, (2, 2)))
        C = Matrix(np.random.randint(0, 5, (2, 2)))
        if hash(A) == hash(C) and not (A == C):
            B = D = Matrix(np.random.randint(0, 5, (2, 2)))
            AB = A @ B
            CD = C @ D
            if not (AB == CD):
                return A, B, C, D, AB, CD


if __name__ == "__main__":
    A, B, C, D, AB, CD = find_collision()

    A.save("artifacts/A.txt")
    B.save("artifacts/B.txt")
    C.save("artifacts/C.txt")
    D.save("artifacts/D.txt")
    AB.save("artifacts/AB.txt")
    CD.save("artifacts/CD.txt")

    with open("artifacts/hash.txt", "w") as f:
        f.write(f"Hash(AB): {hash(AB)}\nHash(CD): {hash(CD)}")