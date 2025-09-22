def matrix_add(a: list[list], b: list[list]) -> list[list]:
    # Проверка, что матрицы не пустые
    if len(a) == 0 or len(b) == 0 or len(a[0]) == 0 or len(b[0]) == 0:
        raise ValueError("Матрицы не могут быть пустыми")

    # Проверка размерности матриц
    if len(a) != len(b):
        raise ValueError("Матрицы должны иметь одинаковое количество строк")

    if len(a[0]) != len(b[0]):
        raise ValueError("Матрицы должны иметь одинаковое количество столбцов")

    # Проверка, что все строки имеют одинаковую длину
    for i in range(len(a)):
        if len(a[i]) != len(a[0]):
            raise ValueError("Все строки первой матрицы должны иметь одинаковую длину")

    for i in range(len(b)):
        if len(b[i]) != len(b[0]):
            raise ValueError("Все строки второй матрицы должны иметь одинаковую длину")

    # Создание результирующей матрицы
    result = []
    for i in range(len(a)):
        row = []
        for j in range(len(a[0])):
            row.append(a[i][j] + b[i][j])
        result.append(row)

    return result


def matrix_multiply(a: list[list], b: list[list]) -> list[list]:
    # Проверка, что матрицы не пустые
    if len(a) == 0 or len(b) == 0 or len(a[0]) == 0 or len(b[0]) == 0:
        raise ValueError("Матрицы не могут быть пустыми")

    # Проверка, что матрицы двумерные и корректной формы
    rows_a = len(a)
    cols_a = len(a[0])
    rows_b = len(b)
    cols_b = len(b[0])

    # Проверка, что все строки матрицы a имеют одинаковую длину
    for i in range(rows_a):
        if len(a[i]) != cols_a:
            raise ValueError("Все строки первой матрицы должны иметь одинаковую длину")

    # Проверка, что все строки матрицы b имеют одинаковую длину
    for i in range(rows_b):
        if len(b[i]) != cols_b:
            raise ValueError("Все строки второй матрицы должны иметь одинаковую длину")

    # Проверка совместимости размерностей для умножения
    if cols_a != rows_b:
        raise ValueError(
            f"Несовместимые размерности для умножения: "
            f"матрица A ({rows_a}x{cols_a}) и матрица B ({rows_b}x{cols_b}). "
            f"Количество столбцов A должно равняться количеству строк B"
        )

    # Создание результирующей матрицы размером rows_a x cols_b
    result = [[0 for _ in range(cols_b)] for _ in range(rows_a)]

    # Алгоритм умножения матриц
    for i in range(rows_a):  # Для каждой строки матрицы A
        for j in range(cols_b):  # Для каждого столбца матрицы B
            for k in range(cols_a):  # Для каждого элемента в строке A/столбце B
                result[i][j] += a[i][k] * b[k][j]

    return result


def determinant_optimized(matrix: list[list], col: int = 0) -> float:
    n = len(matrix)

    # Проверка, что матрица не пустая
    if not matrix:
        raise ValueError("Матрица не может быть пустой")

    # Проверка, что матрица квадратная
    for i in range(n):
        if len(matrix[i]) != n:
            raise ValueError(f"Матрица должна быть квадратной. Строка {i} имеет длину {len(matrix[i])}, ожидалось {n}")

    # Базовые случаи
    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    # Ищем столбец с максимальным количеством нулей для оптимизации
    max_zeros = -1
    best_col = col
    for j in range(n):
        zeros_count = sum(1 for i in range(n) if matrix[i][j] == 0)
        if zeros_count > max_zeros:
            max_zeros = zeros_count
            best_col = j

    # Разложение по лучшему столбцу
    det = 0
    for i in range(n):
        if matrix[i][best_col] == 0:
            continue  # Пропускаем нулевые элементы

        # Создаем минорную матрицу
        minor = []
        for k in range(n):
            if k != i:  # Пропускаем i-ю строку
                row = []
                for l in range(n):
                    if l != best_col:  # Пропускаем best_col-й столбец
                        row.append(matrix[k][l])
                minor.append(row)

        # Вычисляем алгебраическое дополнение
        sign = 1 if (i + best_col) % 2 == 0 else -1
        det += sign * matrix[i][best_col] * determinant_optimized(minor)

    return det


def inverse(matrix: list[list]) -> list[list]:
    # Проверка, что матрица не пустая
    if not matrix:
        raise ValueError("Матрица не может быть пустой")

    n = len(matrix)

    # Проверка, что матрица квадратная
    for i in range(n):
        if len(matrix[i]) != n:
            raise ValueError(f"Матрица должна быть квадратной. Строка {i} имеет длину {len(matrix[i])}, ожидалось {n}")

    # Вычисляем определитель
    det = determinant_optimized(matrix)

    # Проверка на вырожденность
    if abs(det) < 1e-10:  # Маленькое значение для учета погрешности вычислений
        raise ValueError("Матрица вырожденная (определитель = 0), обратной матрицы не существует")

    # Случай матрицы 1x1
    if n == 1:
        return [[1 / matrix[0][0]]]

    # Создаем матрицу алгебраических дополнений
    cofactor_matrix = []
    for i in range(n):
        cofactor_row = []
        for j in range(n):
            # Создаем минорную матрицу (исключаем i-ю строку и j-й столбец)
            minor = []
            for k in range(n):
                if k != i:
                    row = []
                    for l in range(n):
                        if l != j:
                            row.append(matrix[k][l])
                    minor.append(row)

            # Вычисляем минор и алгебраическое дополнение
            minor_det = determinant_optimized(minor)
            sign = 1 if (i + j) % 2 == 0 else -1
            cofactor = sign * minor_det
            cofactor_row.append(cofactor)
        cofactor_matrix.append(cofactor_row)

    # Транспонируем матрицу алгебраических дополнений (получаем присоединенную матрицу)
    adjugate = []
    for j in range(n):
        adjugate_row = []
        for i in range(n):
            adjugate_row.append(cofactor_matrix[i][j])
        adjugate.append(adjugate_row)

    # Делим каждый элемент присоединенной матрицы на определитель
    inverse_matrix = []
    for i in range(n):
        inverse_row = []
        for j in range(n):
            inverse_row.append(adjugate[i][j] / det)
        inverse_matrix.append(inverse_row)

    return inverse_matrix


def solve_system_gaussian(coefficients: list[list], constants: list) -> list:
    n = len(coefficients)

    # Проверка корректности входных данных
    if n == 0:
        raise ValueError("Система не может быть пустой")

    if len(constants) != n:
        raise ValueError("Размер вектора констант не совпадает с размером системы")

    for i in range(n):
        if len(coefficients[i]) != n:
            raise ValueError("Матрица коэффициентов должна быть квадратной")

    # Создаем расширенную матрицу
    augmented = [coefficients[i] + [constants[i]] for i in range(n)]

    # Прямой ход метода Гаусса
    rank = 0
    for col in range(n):
        # Поиск ненулевого элемента в текущем столбце
        pivot_row = -1
        for row in range(rank, n):
            if abs(augmented[row][col]) > 1e-12:
                pivot_row = row
                break

        if pivot_row == -1:
            # Все элементы в столбце нулевые, переходим к следующему столбцу
            continue

        # Перестановка строк (ставим ведущую строку на позицию rank)
        if pivot_row != rank:
            augmented[rank], augmented[pivot_row] = augmented[pivot_row], augmented[rank]

        # Нормализация ведущей строки
        pivot_value = augmented[rank][col]
        for j in range(col, n + 1):
            augmented[rank][j] /= pivot_value

        # Обнуление элементов ниже ведущего
        for row in range(rank + 1, n):
            factor = augmented[row][col]
            for j in range(col, n + 1):
                augmented[row][j] -= factor * augmented[rank][j]

        rank += 1

    # Проверка на совместность системы
    for row in range(rank, n):
        # Если в строке все коэффициенты нулевые, но свободный член не нулевой
        all_zeros = True
        for col in range(n):
            if abs(augmented[row][col]) > 1e-12:
                all_zeros = False
                break

        if all_zeros and abs(augmented[row][n]) > 1e-12:
            raise ValueError("Система несовместна: нет решений")

    # Если ранг меньше числа переменных
    if rank < n:
        # Проверяем, есть ли ненулевые свободные члены в нулевых строках
        for row in range(rank, n):
            if abs(augmented[row][n]) > 1e-12:
                # Нашли строку вида 0 = b, где b ≠ 0
                raise ValueError("Система несовместна: нет решений")

        # Если дошли сюда, значит система имеет бесконечно много решений
        raise ValueError("Система имеет бесконечно много решений")

    # Обратный ход метода Гаусса
    solution = [0] * n
    for i in range(n - 1, -1, -1):
        solution[i] = augmented[i][n]  # Свободный член
        for j in range(i + 1, n):
            solution[i] -= augmented[i][j] * solution[j]
        # augmented[i][i] уже равно 1 после нормализации

    return solution
