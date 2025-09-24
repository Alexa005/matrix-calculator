import math
import pytest

from matrix import matrix_add
from matrix import matrix_multiply
from matrix import determinant_optimized
from matrix import inverse
from matrix import solve_system_gaussian
class TestMatrixAdd:
    """Тесты для функции matrix_add"""

    # Тесты успешных случаев
    def test_add_2x2_matrices(self):
        """Тест сложения двух матриц 2x2"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        expected = [[6, 8], [10, 12]]
        assert matrix_add(a, b) == expected

    def test_add_3x3_matrices(self):
        """Тест сложения двух матриц 3x3"""
        a = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        b = [[9, 8, 7], [6, 5, 4], [3, 2, 1]]
        expected = [[10, 10, 10], [10, 10, 10], [10, 10, 10]]
        assert matrix_add(a, b) == expected

    def test_add_1x1_matrices(self):
        """Тест сложения двух матриц 1x1"""
        a = [[5]]
        b = [[3]]
        expected = [[8]]
        assert matrix_add(a, b) == expected

    def test_add_with_negative_numbers(self):
        """Тест сложения матриц с отрицательными числами"""
        a = [[1, -2], [-3, 4]]
        b = [[-5, 6], [7, -8]]
        expected = [[-4, 4], [4, -4]]
        assert matrix_add(a, b) == expected

    def test_add_with_zeros(self):
        """Тест сложения матриц с нулевыми элементами"""
        a = [[0, 0], [0, 0]]
        b = [[1, 2], [3, 4]]
        expected = [[1, 2], [3, 4]]
        assert matrix_add(a, b) == expected

    def test_add_rectangular_matrices(self):
        """Тест сложения прямоугольных матриц"""
        a = [[1, 2, 3], [4, 5, 6]]
        b = [[7, 8, 9], [10, 11, 12]]
        expected = [[8, 10, 12], [14, 16, 18]]
        assert matrix_add(a, b) == expected

    # Тесты случаев с ошибками - разные размеры
    def test_add_different_row_count(self):
        """Тест ошибки при разном количестве строк"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6]]  # Только одна строка

        with pytest.raises(ValueError, match="Матрицы должны иметь одинаковое количество строк"):
            matrix_add(a, b)

    def test_add_different_column_count(self):
        """Тест ошибки при разном количестве столбцов"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6, 7], [8, 9, 10]]  # 3 столбца вместо 2

        with pytest.raises(ValueError, match="Матрицы должны иметь одинаковое количество столбцов"):
            matrix_add(a, b)

    def test_add_ragged_matrix_a(self):
        """Тест ошибки при неровной первой матрице"""
        a = [[1, 2], [3, 4, 5]]  # Вторая строка длиннее
        b = [[6, 7], [8, 9]]

        with pytest.raises(ValueError, match="Все строки первой матрицы должны иметь одинаковую длину"):
            matrix_add(a, b)

    def test_add_ragged_matrix_b(self):
        """Тест ошибки при неровной второй матрице"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8, 9]]  # Вторая строка длиннее

        with pytest.raises(ValueError, match="Все строки второй матрицы должны иметь одинаковую длину"):
            matrix_add(a, b)

    def test_add_both_ragged_matrices(self):
        """Тест ошибки при обеих неровных матрицах"""
        a = [[1, 2], [3, 4, 5]]
        b = [[6, 7], [8, 9, 10]]

        # Первая ошибка, которая будет обнаружена - неровная матрица A
        with pytest.raises(ValueError, match="Все строки первой матрицы должны иметь одинаковую длину"):
            matrix_add(a, b)

    # Тесты случаев с ошибками - пустые матрицы
    def test_add_empty_matrix_a(self):
        """Тест ошибки при пустой первой матрице"""
        a = []
        b = [[1, 2], [3, 4]]

        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_add(a, b)

    def test_add_empty_matrix_b(self):
        """Тест ошибки при пустой второй матрице"""
        a = [[1, 2], [3, 4]]
        b = []

        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_add(a, b)

    def test_add_both_empty_matrices(self):
        """Тест ошибки при обеих пустых матрицах"""
        a = []
        b = []

        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_add(a, b)

    def test_add_empty_row_matrix_a(self):
        """Тест ошибки при матрице с пустой строкой"""
        a = [[]]  # Матрица с одной пустой строкой
        b = [[1]]

        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_add(a, b)

    def test_add_empty_row_matrix_b(self):
        """Тест ошибки при второй матрице с пустой строкой"""
        a = [[1]]
        b = [[]]  # Матрица с одной пустой строкой

        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_add(a, b)

    # Тесты пограничных случаев
    def test_add_large_matrices(self):
        """Тест сложения больших матриц"""
        a = [[i + j for j in range(10)] for i in range(10)]
        b = [[(i + j) * 2 for j in range(10)] for i in range(10)]
        expected = [[(i + j) * 3 for j in range(10)] for i in range(10)]

        result = matrix_add(a, b)
        assert result == expected

    def test_add_float_matrices(self):
        """Тест сложения матриц с числами с плавающей точкой"""
        a = [[1.5, 2.3], [3.7, 4.1]]
        b = [[0.5, 1.7], [2.3, 3.9]]
        expected = [[2.0, 4.0], [6.0, 8.0]]

        result = matrix_add(a, b)
        assert result == expected

    def test_commutative_property(self):
        """Тест коммутативного свойства: A + B = B + A"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]

        result1 = matrix_add(a, b)
        result2 = matrix_add(b, a)

        assert result1 == result2

    def test_associative_property(self):
        """Тест ассоциативного свойства: (A + B) + C = A + (B + C)"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        c = [[9, 10], [11, 12]]

        result1 = matrix_add(matrix_add(a, b), c)
        result2 = matrix_add(a, matrix_add(b, c))

        assert result1 == result2

class TestMatrixAddErrorMessages:
    """Тесты для проверки конкретных сообщений об ошибках"""

    def test_error_message_different_rows(self):
        """Тест конкретного сообщения об ошибке для разного количества строк"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6]]

        with pytest.raises(ValueError) as exc_info:
            matrix_add(a, b)

        assert "Матрицы должны иметь одинаковое количество строк" in str(exc_info.value)

    def test_error_message_different_columns(self):
        """Тест конкретного сообщения об ошибке для разного количества столбцов"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6, 7], [8, 9, 10]]

        with pytest.raises(ValueError) as exc_info:
            matrix_add(a, b)

        assert "Матрицы должны иметь одинаковое количество столбцов" in str(exc_info.value)

    def test_error_message_ragged_a(self):
        """Тест конкретного сообщения об ошибке для неровной матрицы A"""
        a = [[1, 2], [3, 4, 5]]
        b = [[6, 7], [8, 9]]

        with pytest.raises(ValueError) as exc_info:
            matrix_add(a, b)

        assert "Все строки первой матрицы должны иметь одинаковую длину" in str(exc_info.value)

    def test_error_message_ragged_b(self):
        """Тест конкретного сообщения об ошибке для неровной матрицы B"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8, 9]]

        with pytest.raises(ValueError) as exc_info:
            matrix_add(a, b)

        assert "Все строки второй матрицы должны иметь одинаковую длину" in str(exc_info.value)

    def test_error_message_empty(self):
        """Тест конкретного сообщения об ошибке для пустых матриц"""
        a = []
        b = [[1, 2]]

        with pytest.raises(ValueError) as exc_info:
            matrix_add(a, b)

        assert "Матрицы не могут быть пустыми" in str(exc_info.value)


class TestMatrixMultiply:
    """Тесты для функции умножения матриц"""

    def test_basic_multiplication(self):
        """Тест базового умножения матриц 2x2"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]
        expected = [[19, 22], [43, 50]]
        assert matrix_multiply(a, b) == expected

    def test_rectangular_matrices(self):
        """Тест умножения прямоугольных матриц"""
        a = [[1, 2, 3]]  # 1x3
        b = [[4], [5], [6]]  # 3x1
        expected = [[32]]  # 1x1
        assert matrix_multiply(a, b) == expected

        a = [[1, 2], [3, 4], [5, 6]]  # 3x2
        b = [[7, 8, 9], [10, 11, 12]]  # 2x3
        expected = [[27, 30, 33], [61, 68, 75], [95, 106, 117]]  # 3x3
        assert matrix_multiply(a, b) == expected

    def test_identity_matrix(self):
        """Тест умножения на единичную матрицу"""
        a = [[1, 2, 3], [4, 5, 6]]
        identity = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        assert matrix_multiply(a, identity) == a

    def test_zero_matrix(self):
        """Тест умножения на нулевую матрицу"""
        a = [[1, 2], [3, 4]]
        zero = [[0, 0], [0, 0]]
        expected = [[0, 0], [0, 0]]
        assert matrix_multiply(a, zero) == expected

    def test_float_numbers(self):
        """Тест с дробными числами"""
        a = [[0.5, 1.5], [2.0, 3.5]]
        b = [[2.0, 1.0], [0.5, 2.0]]
        expected = [[1.75, 3.5], [5.75, 9.0]]
        result = matrix_multiply(a, b)

        # Сравнение с учетом погрешности вычислений с плавающей точкой
        for i in range(len(expected)):
            for j in range(len(expected[0])):
                assert abs(result[i][j] - expected[i][j]) < 1e-10

    def test_single_element_matrices(self):
        """Тест с матрицами 1x1"""
        a = [[5]]
        b = [[3]]
        expected = [[15]]
        assert matrix_multiply(a, b) == expected

    def test_negative_numbers(self):
        """Тест с отрицательными числами"""
        a = [[-1, 2], [3, -4]]
        b = [[-2, 1], [-3, 2]]
        expected = [[-4, 3], [6, -5]]
        assert matrix_multiply(a, b) == expected


class TestMatrixMultiplyErrors:
    """Тесты на обработку ошибок"""

    def test_empty_matrix_a(self):
        """Тест пустой первой матрицы"""
        a = []
        b = [[1, 2], [3, 4]]
        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_multiply(a, b)

    def test_empty_matrix_b(self):
        """Тест пустой второй матрицы"""
        a = [[1, 2], [3, 4]]
        b = []
        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_multiply(a, b)

    def test_empty_row_matrix_a(self):
        """Тест матрицы с пустой строкой"""
        a = [[]]
        b = [[1, 2], [3, 4]]
        with pytest.raises(ValueError, match="Матрицы не могут быть пустыми"):
            matrix_multiply(a, b)

    def test_uneven_rows_matrix_a(self):
        """Тест неравномерной первой матрицы"""
        a = [[1, 2], [3, 4, 5]]  # Вторая строка длиннее
        b = [[1, 2], [3, 4]]
        with pytest.raises(ValueError, match="Все строки первой матрицы должны иметь одинаковую длину"):
            matrix_multiply(a, b)

    def test_uneven_rows_matrix_b(self):
        """Тест неравномерной второй матрицы"""
        a = [[1, 2], [3, 4]]
        b = [[1, 2], [3, 4, 5]]  # Вторая строка длиннее
        with pytest.raises(ValueError, match="Все строки второй матрицы должны иметь одинаковую длину"):
            matrix_multiply(a, b)

    def test_incompatible_dimensions(self):
        """Тест несовместимых размерностей"""
        a = [[1, 2, 3]]  # 1x3
        b = [[1, 2]]  # 1x2 (должна быть 3x?)
        with pytest.raises(ValueError) as exc_info:
            matrix_multiply(a, b)
        assert "Несовместимые размерности для умножения" in str(exc_info.value)

    def test_specific_dimension_error_message(self):
        """Тест конкретного сообщения об ошибке размерностей"""
        a = [[1, 2, 3]]  # 1x3
        b = [[1], [2]]  # 2x1
        with pytest.raises(ValueError) as exc_info:
            matrix_multiply(a, b)
        error_msg = str(exc_info.value)
        assert "матрица A (1x3)" in error_msg
        assert "матрица B (2x1)" in error_msg
        assert "Количество столбцов A должно равняться количеству строк B" in error_msg

    def test_large_matrices(self):
        """Тест с большими матрицами (опционально)"""
        a = [[1] * 10 for _ in range(5)]  # 5x10
        b = [[2] * 3 for _ in range(10)]  # 10x3
        expected = [[20] * 3 for _ in range(5)]  # 5x3

        result = matrix_multiply(a, b)
        assert result == expected

    def test_commutativity_failure(self):
        """Тест, что умножение матриц не коммутативно (A×B ≠ B×A)"""
        a = [[1, 2], [3, 4]]
        b = [[5, 6], [7, 8]]

        ab = matrix_multiply(a, b)
        ba = matrix_multiply(b, a)

        # Убедимся, что результаты разные
        assert ab != ba


class TestDeterminantBasic:
    """Тесты базовых случаев определителя"""

    def test_empty_matrix(self):
        """Тест пустой матрицы"""
        with pytest.raises(ValueError, match="Матрица не может быть пустой"):
            determinant_optimized([])

    def test_non_square_matrix(self):
        """Тест неквадратной матрицы"""
        matrix = [[1, 2, 3], [4, 5, 6]]  # 2x3
        with pytest.raises(ValueError, match="Матрица должна быть квадратной"):
            determinant_optimized(matrix)

    def test_irregular_matrix(self):
        """Тест матрицы с неравными строками"""
        matrix = [[1, 2], [3, 4, 5]]  # Вторая строка длиннее
        with pytest.raises(ValueError, match="Матрица должна быть квадратной"):
            determinant_optimized(matrix)

    def test_1x1_matrix(self):
        """Тест матрицы 1x1"""
        matrix = [[5]]
        assert determinant_optimized(matrix) == 5

        matrix = [[-3]]
        assert determinant_optimized(matrix) == -3

        matrix = [[0]]
        assert determinant_optimized(matrix) == 0

    def test_2x2_matrix(self):
        """Тест матрицы 2x2"""
        matrix = [[1, 2], [3, 4]]
        assert determinant_optimized(matrix) == 1 * 4 - 2 * 3

        matrix = [[5, -1], [2, 3]]
        assert determinant_optimized(matrix) == 5 * 3 - (-1) * 2

        matrix = [[0, 0], [0, 0]]  # Нулевая матрица
        assert determinant_optimized(matrix) == 0

    def test_3x3_matrix(self):
        """Тест матрицы 3x3"""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # Правило Саррюса: 1*5*9 + 2*6*7 + 3*4*8 - 3*5*7 - 2*4*9 - 1*6*8
        expected = 1 * 5 * 9 + 2 * 6 * 7 + 3 * 4 * 8 - 3 * 5 * 7 - 2 * 4 * 9 - 1 * 6 * 8
        assert determinant_optimized(matrix) == expected

        matrix = [[2, 0, 1], [1, 3, 2], [4, 1, 1]]
        expected = 2 * (3 * 1 - 2 * 1) - 0 * (1 * 1 - 2 * 4) + 1 * (1 * 1 - 3 * 4)
        assert determinant_optimized(matrix) == expected


class TestDeterminantSpecialCases:
    """Тесты специальных случаев"""

    def test_identity_matrix(self):
        """Тест единичной матрицы"""
        for n in range(1, 6):  # Тестируем размеры от 1 до 5
            matrix = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
            assert determinant_optimized(matrix) == 1

    def test_diagonal_matrix(self):
        """Тест диагональной матрицы"""
        matrix = [[2, 0, 0], [0, 3, 0], [0, 0, 4]]
        assert determinant_optimized(matrix) == 2 * 3 * 4

        matrix = [[1, 0, 0, 0], [0, 5, 0, 0], [0, 0, 2, 0], [0, 0, 0, 3]]
        assert determinant_optimized(matrix) == 1 * 5 * 2 * 3

    def test_triangular_matrix(self):
        """Тест треугольных матриц"""
        # Верхняя треугольная
        matrix = [[1, 2, 3], [0, 4, 5], [0, 0, 6]]
        assert determinant_optimized(matrix) == 1 * 4 * 6

        # Нижняя треугольная
        matrix = [[1, 0, 0], [2, 3, 0], [4, 5, 6]]
        assert determinant_optimized(matrix) == 1 * 3 * 6

    def test_zero_matrix(self):
        """Тест нулевой матрицы"""
        for n in range(1, 5):
            matrix = [[0 for _ in range(n)] for _ in range(n)]
            assert determinant_optimized(matrix) == 0

    def test_matrix_with_zeros(self):
        """Тест матриц с нулевыми элементами (проверка оптимизации)"""
        # Матрица с нулевым столбцом - определитель должен быть 0
        matrix = [[1, 0, 2], [3, 0, 4], [5, 0, 6]]
        assert determinant_optimized(matrix) == 0

        # Матрица с нулевой строкой - определитель должен быть 0
        matrix = [[0, 0, 0], [1, 2, 3], [4, 5, 6]]
        assert determinant_optimized(matrix) == 0


class TestDeterminantLargeMatrices:
    """Тесты больших матриц"""

    def test_4x4_matrix(self):
        """Тест матрицы 4x4"""
        matrix = [[1, 0, 2, 1], [0, 1, 1, 0], [2, 1, 1, 1], [1, 0, 1, 2]]
        # Разложение по первому столбцу
        expected = -5
        assert determinant_optimized(matrix) == expected

    def test_5x5_matrix(self):
        """Тест матрицы 5x5"""
        matrix = [
            [1, 2, 0, 0, 0],
            [3, 4, 0, 0, 0],
            [0, 0, 2, 0, 0],
            [0, 0, 0, 3, 0],
            [0, 0, 0, 0, 4]
        ]
        # Блочная матрица - определитель равен произведению определителей блоков
        block1_det = 1 * 4 - 2 * 3
        block2_det = 2 * 3 * 4
        expected = block1_det * block2_det
        assert determinant_optimized(matrix) == expected


class TestDeterminantFloatingPoint:
    """Тесты с плавающей точкой"""

    def test_float_matrix(self):
        """Тест матрицы с дробными числами"""
        matrix = [[1.5, 2.5], [3.5, 4.5]]
        expected = 1.5 * 4.5 - 2.5 * 3.5
        result = determinant_optimized(matrix)
        assert abs(result - expected) < 1e-10

    def test_mixed_numbers(self):
        """Тест матрицы со смешанными типами чисел"""
        matrix = [[1, 2.5], [3, 4]]
        expected = 1 * 4 - 2.5 * 3
        result = determinant_optimized(matrix)
        assert abs(result - expected) < 1e-10


class TestDeterminantProperties:
    """Тесты математических свойств определителя"""

    def test_determinant_of_transpose(self):
        """Тест, что det(A) = det(A^T)"""
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        transpose = [[matrix[j][i] for j in range(3)] for i in range(3)]

        det_a = determinant_optimized(matrix)
        det_at = determinant_optimized(transpose)

        assert abs(det_a - det_at) < 1e-10

    def test_swapping_rows_changes_sign(self):
        """Тест, что перестановка строк меняет знак определителя"""
        matrix = [[1, 2], [3, 4]]
        swapped = [[3, 4], [1, 2]]

        det_original = determinant_optimized(matrix)
        det_swapped = determinant_optimized(swapped)

        assert det_swapped == -det_original

    def test_scaling_row_scales_determinant(self):
        """Тест, что умножение строки на скаляр умножает определитель на скаляр"""
        matrix = [[1, 2], [3, 4]]
        scaled = [[2, 4], [3, 4]]  # Первая строка умножена на 2

        det_original = determinant_optimized(matrix)
        det_scaled = determinant_optimized(scaled)

        assert det_scaled == 2 * det_original


class TestDeterminantEdgeCases:
    """Тесты граничных случаев"""

    def test_singular_matrix(self):
        """Тест вырожденной матрицы"""
        # Матрица с линейно зависимыми строками
        matrix = [[1, 2, 3], [2, 4, 6], [7, 8, 9]]  # Вторая строка = 2 * первая
        assert determinant_optimized(matrix) == 0

    def test_almost_singular_matrix(self):
        """Тест почти вырожденной матрицы"""
        matrix = [[1, 2], [2, 4.000001]]  # Почти линейно зависимые строки
        det = determinant_optimized(matrix)
        assert 0.00000099999 < det < 0.00000100111

    def test_large_values(self):
        """Тест с большими числами"""
        matrix = [[10 ** 6, 2 * 10 ** 6], [3 * 10 ** 6, 4 * 10 ** 6]]
        expected = (10 ** 6) * (4 * 10 ** 6) - (2 * 10 ** 6) * (3 * 10 ** 6)
        assert determinant_optimized(matrix) == expected

    def test_negative_determinant(self):
        """Тест отрицательного определителя"""
        matrix = [[0, 1], [1, 0]]  # Антидиагональная матрица
        assert determinant_optimized(matrix) == -1


def test_recursive_calls():
    """Тест рекурсивных вызовов (проверка оптимизации по столбцам)"""
    # Матрица, где первый столбец имеет меньше нулей, чем второй
    # Алгоритм должен выбрать столбец с максимальным количеством нулей
    matrix = [[1, 0, 2], [3, 0, 4], [5, 0, 6]]

    # Определитель должен быть 0 из-за нулевого столбца
    assert determinant_optimized(matrix) == 0


class TestInverseBasic:
    """Тесты базовых случаев обратной матрицы"""

    def test_empty_matrix(self):
        """Тест пустой матрицы"""
        with pytest.raises(ValueError, match="Матрица не может быть пустой"):
            inverse([])

    def test_non_square_matrix(self):
        """Тест неквадратной матрицы"""
        matrix = [[1, 2, 3], [4, 5, 6]]  # 2x3
        with pytest.raises(ValueError, match="Матрица должна быть квадратной"):
            inverse(matrix)

    def test_irregular_matrix(self):
        """Тест матрицы с неравными строками"""
        matrix = [[1, 2], [3, 4, 5]]  # Вторая строка длиннее
        with pytest.raises(ValueError, match="Матрица должна быть квадратной"):
            inverse(matrix)


class TestInverse1x1:
    """Тесты для матриц 1x1"""

    def test_1x1_positive(self):
        """Тест матрицы 1x1 с положительным числом"""
        matrix = [[5]]
        expected = [[0.2]]
        result = inverse(matrix)
        assert result == expected

    def test_1x1_negative(self):
        """Тест матрицы 1x1 с отрицательным числом"""
        matrix = [[-3]]
        expected = [[-1 / 3]]
        result = inverse(matrix)
        assert math.isclose(result[0][0], expected[0][0])

    def test_1x1_float(self):
        """Тест матрицы 1x1 с дробным числом"""
        matrix = [[2.5]]
        expected = [[0.4]]
        result = inverse(matrix)
        assert math.isclose(result[0][0], expected[0][0])

    def test_1x1_singular(self):
        """Тест вырожденной матрицы 1x1"""
        matrix = [[0]]
        with pytest.raises(ValueError, match="Матрица вырожденная"):
            inverse(matrix)


class TestInverse2x2:
    """Тесты для матриц 2x2"""

    def test_2x2_regular(self):
        """Тест обычной матрицы 2x2"""
        matrix = [[1, 2], [3, 4]]
        det = 1 * 4 - 2 * 3
        expected = [[4 / det, -2 / det], [-3 / det, 1 / det]]
        result = inverse(matrix)

        for i in range(2):
            for j in range(2):
                assert math.isclose(result[i][j], expected[i][j])

    def test_2x2_identity(self):
        """Тест единичной матрицы 2x2"""
        matrix = [[1, 0], [0, 1]]
        expected = [[1, 0], [0, 1]]
        result = inverse(matrix)
        assert result == expected

    def test_2x2_singular(self):
        """Тест вырожденной матрицы 2x2"""
        matrix = [[1, 2], [2, 4]]  # Вторая строка = 2 * первая
        with pytest.raises(ValueError, match="Матрица вырожденная"):
            inverse(matrix)

    def test_2x2_float(self):
        """Тест матрицы 2x2 с дробными числами"""
        matrix = [[1.5, 2.5], [3.5, 4.5]]
        det = 1.5 * 4.5 - 2.5 * 3.5
        expected = [[4.5 / det, -2.5 / det], [-3.5 / det, 1.5 / det]]
        result = inverse(matrix)

        for i in range(2):
            for j in range(2):
                assert math.isclose(result[i][j], expected[i][j], rel_tol=1e-10)


class TestInverse3x3:
    """Тесты для матриц 3x3"""

    def test_3x3_regular(self):
        """Тест обычной матрицы 3x3"""
        matrix = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
        # Проверяем через свойство A * A^(-1) = I
        inv_matrix = inverse(matrix)

        # Умножаем матрицу на обратную
        result = matrix_multiply(matrix, inv_matrix)

        # Должны получить единичную матрицу
        for i in range(3):
            for j in range(3):
                if i == j:
                    assert math.isclose(result[i][j], 1.0, abs_tol=1e-10)
                else:
                    assert math.isclose(result[i][j], 0.0, abs_tol=1e-10)

    def test_3x3_identity(self):
        """Тест единичной матрицы 3x3"""
        matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        expected = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        result = inverse(matrix)

        for i in range(3):
            for j in range(3):
                assert math.isclose(result[i][j], expected[i][j])

    def test_3x3_diagonal(self):
        """Тест диагональной матрицы 3x3"""
        matrix = [[2, 0, 0], [0, 3, 0], [0, 0, 4]]
        expected = [[0.5, 0, 0], [0, 1 / 3, 0], [0, 0, 0.25]]
        result = inverse(matrix)

        for i in range(3):
            for j in range(3):
                assert math.isclose(result[i][j], expected[i][j])

    def test_3x3_singular(self):
        """Тест вырожденной матрицы 3x3"""
        matrix = [[1, 2, 3], [2, 4, 6], [7, 8, 9]]  # Вторая строка = 2 * первая
        with pytest.raises(ValueError, match="Матрица вырожденная"):
            inverse(matrix)


class TestInverseLargeMatrices:
    """Тесты для больших матриц"""

    def test_4x4_regular(self):
        """Тест матрицы 4x4"""
        matrix = [
            [4, 3, 2, 1],
            [3, 4, 3, 2],
            [2, 3, 4, 3],
            [1, 2, 3, 4]
        ]

        inv_matrix = inverse(matrix)
        result = matrix_multiply(matrix, inv_matrix)

        # Проверяем, что получили единичную матрицу
        for i in range(4):
            for j in range(4):
                if i == j:
                    assert math.isclose(result[i][j], 1.0, abs_tol=1e-10)
                else:
                    assert math.isclose(result[i][j], 0.0, abs_tol=1e-10)

    def test_5x5_symmetric(self):
        """Тест симметричной матрицы 5x5"""
        # Создаем симметричную положительно определенную матрицу
        matrix = []
        for i in range(5):
            row = []
            for j in range(5):
                row.append(1.0 / (1 + abs(i - j)))  # Элементы убывают с расстоянием от диагонали
            matrix.append(row)

        inv_matrix = inverse(matrix)
        result = matrix_multiply(matrix, inv_matrix)

        # Проверяем единичную матрицу
        for i in range(5):
            for j in range(5):
                if i == j:
                    assert math.isclose(result[i][j], 1.0, abs_tol=1e-8)
                else:
                    assert math.isclose(result[i][j], 0.0, abs_tol=1e-8)


class TestInverseProperties:
    """Тесты математических свойств обратной матрицы"""

    def test_inverse_of_inverse(self):
        """Тест, что (A^(-1))^(-1) = A"""
        matrix = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]
        inv_matrix = inverse(matrix)
        inv_inv_matrix = inverse(inv_matrix)

        for i in range(3):
            for j in range(3):
                assert math.isclose(inv_inv_matrix[i][j], matrix[i][j], rel_tol=1e-10)

    def test_identity_inverse(self):
        """Тест, что обратная к единичной - сама единичная"""
        identity_3x3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        inv_identity = inverse(identity_3x3)

        assert inv_identity == identity_3x3

    def test_diagonal_inverse(self):
        """Тест обратной диагональной матрицы"""
        matrix = [[2, 0, 0], [0, 3, 0], [0, 0, 4]]
        expected = [[0.5, 0, 0], [0, 1 / 3, 0], [0, 0, 0.25]]
        result = inverse(matrix)

        for i in range(3):
            for j in range(3):
                assert math.isclose(result[i][j], expected[i][j])

    def test_orthogonal_matrix(self):
        """Тест ортогональной матрицы (обратная = транспонированная)"""
        # Матрица поворота на 90 градусов
        matrix = [[0, -1], [1, 0]]
        inv_matrix = inverse(matrix)
        transpose = [[matrix[j][i] for j in range(2)] for i in range(2)]

        for i in range(2):
            for j in range(2):
                assert math.isclose(inv_matrix[i][j], transpose[i][j])

    def test_large_numbers(self):
        """Тест с большими числами"""
        matrix = [[1e6, 2e6], [3e6, 4e6]]
        det = 1e6 * 4e6 - 2e6 * 3e6
        expected = [[4e6 / det, -2e6 / det], [-3e6 / det, 1e6 / det]]

        inv_matrix = inverse(matrix)

        for i in range(2):
            for j in range(2):
                assert math.isclose(inv_matrix[i][j], expected[i][j])

    def test_mixed_number_types(self):
        """Тест со смешанными типами чисел"""
        matrix = [[1, 2.5], [3, 4]]
        inv_matrix = inverse(matrix)
        result = matrix_multiply(matrix, inv_matrix)

        for i in range(2):
            for j in range(2):
                if i == j:
                    assert math.isclose(result[i][j], 1.0, abs_tol=1e-10)
                else:
                    assert math.isclose(result[i][j], 0.0, abs_tol=1e-10)


class TestGaussianBasicErrors:
    """Тесты базовых ошибок входных данных"""

    def test_empty_system(self):
        """Тест пустой системы"""
        with pytest.raises(ValueError, match="Система не может быть пустой"):
            solve_system_gaussian([], [])

    def test_constants_size_mismatch(self):
        """Тест несовпадения размеров матрицы и вектора констант"""
        coefficients = [[1, 2], [3, 4]]
        constants = [5]  # Должно быть 2 элемента
        with pytest.raises(ValueError, match="Размер вектора констант не совпадает с размером системы"):
            solve_system_gaussian(coefficients, constants)

    def test_non_square_matrix(self):
        """Тест неквадратной матрицы коэффициентов"""
        coefficients = [[1, 2, 3], [4, 5, 6]]  # 2x3
        constants = [7, 8]
        with pytest.raises(ValueError, match="Матрица коэффициентов должна быть квадратной"):
            solve_system_gaussian(coefficients, constants)

    def test_irregular_matrix(self):
        """Тест матрицы с неравными строками"""
        coefficients = [[1, 2], [3, 4, 5]]  # Вторая строка длиннее
        constants = [6, 7]
        with pytest.raises(ValueError, match="Матрица коэффициентов должна быть квадратной"):
            solve_system_gaussian(coefficients, constants)


class TestGaussian1x1:
    """Тесты для систем 1x1"""

    def test_1x1_positive(self):
        """Тест системы 1x1 с положительным коэффициентом"""
        coefficients = [[5]]
        constants = [10]
        expected = [2.0]
        result = solve_system_gaussian(coefficients, constants)
        assert math.isclose(result[0], expected[0])

    def test_1x1_negative(self):
        """Тест системы 1x1 с отрицательным коэффициентом"""
        coefficients = [[-3]]
        constants = [6]
        expected = [-2.0]
        result = solve_system_gaussian(coefficients, constants)
        assert math.isclose(result[0], expected[0])

    def test_1x1_float(self):
        """Тест системы 1x1 с дробными числами"""
        coefficients = [[2.5]]
        constants = [7.5]
        expected = [3.0]
        result = solve_system_gaussian(coefficients, constants)
        assert math.isclose(result[0], expected[0])

    def test_1x1_zero_coefficient(self):
        """Тест системы 1x1 с нулевым коэффициентом"""
        coefficients = [[0]]
        constants = [5]
        with pytest.raises(ValueError, match="Система несовместна: нет решений"):
            solve_system_gaussian(coefficients, constants)

    def test_1x1_zero_constant(self):
        """Тест системы 1x1 с нулевой константой и нулевым коэффициентом"""
        coefficients = [[0]]
        constants = [0]
        with pytest.raises(ValueError, match="Система имеет бесконечно много решений"):
            solve_system_gaussian(coefficients, constants)


class TestGaussian2x2:
    """Тесты для систем 2x2"""

    def test_2x2_regular(self):
        """Тест обычной системы 2x2"""
        coefficients = [[2, 1], [1, 3]]
        constants = [5, 10]
        # Решение: x = 1, y = 3
        expected = [1.0, 3.0]
        result = solve_system_gaussian(coefficients, constants)

        for i in range(2):
            assert math.isclose(result[i], expected[i], abs_tol=1e-10)

    def test_2x2_identity(self):
        """Тест с единичной матрицей"""
        coefficients = [[1, 0], [0, 1]]
        constants = [3, 4]
        expected = [3.0, 4.0]
        result = solve_system_gaussian(coefficients, constants)
        assert result == expected

    def test_2x2_need_pivoting(self):
        """Тест с необходимостью выбора ведущего элемента"""
        coefficients = [[0, 1], [2, 3]]
        constants = [4, 5]
        # Решение: x = -3.5, y = 4
        expected = [-3.5, 4.0]
        result = solve_system_gaussian(coefficients, constants)

        for i in range(2):
            assert math.isclose(result[i], expected[i], abs_tol=1e-10)

    def test_2x2_inconsistent(self):
        """Тест несовместной системы 2x2"""
        coefficients = [[1, 2], [2, 4]]  # Вторая строка = 2 * первая
        constants = [3, 7]  # Но 2*3 ≠ 7
        with pytest.raises(ValueError, match="Система несовместна: нет решений"):
            solve_system_gaussian(coefficients, constants)

    def test_2x2_infinite_solutions(self):
        """Тест системы с бесконечным числом решений"""
        coefficients = [[1, 2], [2, 4]]  # Вторая строка = 2 * первая
        constants = [3, 6]  # И 2*3 = 6
        with pytest.raises(ValueError, match="Система имеет бесконечно много решений"):
            solve_system_gaussian(coefficients, constants)


class TestGaussian3x3:
    """Тесты для систем 3x3"""

    def test_3x3_regular(self):
        """Тест обычной системы 3x3"""
        coefficients = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
        constants = [8, -11, -3]
        # Решение: x = 2, y = 3, z = -1
        expected = [2.0, 3.0, -1.0]
        result = solve_system_gaussian(coefficients, constants)

        for i in range(3):
            assert math.isclose(result[i], expected[i], abs_tol=1e-10)

    def test_3x3_triangular(self):
        """Тест с треугольной матрицей"""
        coefficients = [[1, 2, 3], [0, 4, 5], [0, 0, 6]]
        constants = [6, 7, 8]
        # Решение: z = 8/6, y = (7 - 5z)/4, x = (6 - 2y - 3z)
        expected_z = 8 / 6
        expected_y = (7 - 5 * expected_z) / 4
        expected_x = (6 - 2 * expected_y - 3 * expected_z)
        expected = [expected_x, expected_y, expected_z]

        result = solve_system_gaussian(coefficients, constants)

        for i in range(3):
            assert math.isclose(result[i], expected[i], abs_tol=1e-10)

    def test_3x3_inconsistent(self):
        """Тест несовместной системы 3x3"""
        coefficients = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Третья строка = первая + вторая
        constants = [1, 2, 5]  # Но 1 + 2 ≠ 5
        with pytest.raises(ValueError, match="Система несовместна: нет решений"):
            solve_system_gaussian(coefficients, constants)

    def test_3x3_infinite_solutions(self):
        """Тест системы 3x3 с бесконечным числом решений"""
        coefficients = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]  # Третья строка = первая + вторая
        constants = [1, 2, 3]  # И 1 + 2 = 3
        with pytest.raises(ValueError, match="Система имеет бесконечно много решений"):
            solve_system_gaussian(coefficients, constants)


class TestGaussianLargeSystems:
    """Тесты для больших систем"""

    def test_4x4_regular(self):
        """Тест системы 4x4"""
        coefficients = [
            [4, 1, 2, 3],
            [1, 5, 2, 1],
            [2, 2, 6, 1],
            [3, 1, 1, 7]
        ]
        constants = [10, 9, 11, 12]

        result = solve_system_gaussian(coefficients, constants)

        # Проверяем, что решение удовлетворяет уравнениям
        for i in range(4):
            lhs = sum(coefficients[i][j] * result[j] for j in range(4))
            assert math.isclose(lhs, constants[i], abs_tol=1e-10)

    def test_5x5_diagonal(self):
        """Тест системы 5x5 с диагональной матрицей"""
        coefficients = [[0 for _ in range(5)] for _ in range(5)]
        constants = [0 for _ in range(5)]

        for i in range(5):
            coefficients[i][i] = i + 1
            constants[i] = (i + 1) * 2

        expected = [2.0] * 5  # x_i = 2 для всех i
        result = solve_system_gaussian(coefficients, constants)

        for i in range(5):
            assert math.isclose(result[i], expected[i], abs_tol=1e-10)


class TestGaussianSpecialCases:
    """Тесты специальных случаев"""

    def test_zero_diagonal_with_pivoting(self):
        """Тест с нулями на диагонали, требующими перестановки"""
        coefficients = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
        constants = [3, 2, 1]
        expected = [1.0, 2.0, 3.0]  # После перестановки: x=1, y=2, z=3
        result = solve_system_gaussian(coefficients, constants)

        for i in range(3):
            assert math.isclose(result[i], expected[i], abs_tol=1e-10)

    def test_all_zeros_coefficients(self):
        """Тест, когда все коэффициенты нулевые"""
        coefficients = [[0, 0], [0, 0]]
        constants = [0, 0]
        with pytest.raises(ValueError, match="Система имеет бесконечно много решений"):
            solve_system_gaussian(coefficients, constants)

    def test_all_zeros_coefficients_inconsistent(self):
        """Тест нулевых коэффициентов с ненулевыми константами"""
        coefficients = [[0, 0], [0, 0]]
        constants = [1, 2]
        with pytest.raises(ValueError, match="Система несовместна: нет решений"):
            solve_system_gaussian(coefficients, constants)

    def test_rank_deficient(self):
        """Тест системы с недостаточным рангом"""
        coefficients = [[1, 2, 3], [2, 4, 6], [3, 6, 9]]  # Все строки пропорциональны
        constants = [1, 2, 3]  # Совместная система
        with pytest.raises(ValueError, match="Система имеет бесконечно много решений"):
            solve_system_gaussian(coefficients, constants)


class TestGaussianPrecision:
    """Тесты точности вычислений"""

    def test_ill_conditioned_system(self):
        """Тест плохо обусловленной системы"""
        # Матрица Гильберта - известная плохо обусловленная матрица
        n = 3
        hilbert = []
        for i in range(n):
            row = []
            for j in range(n):
                row.append(1.0 / (i + j + 1))
            hilbert.append(row)

        # Простое решение: x = [1, 1, 1]
        constants = [sum(hilbert[i]) for i in range(n)]
        expected = [1.0] * n

        result = solve_system_gaussian(hilbert, constants)

        # Проверяем с меньшей точностью из-за плохой обусловленности
        for i in range(n):
            assert math.isclose(result[i], expected[i], abs_tol=1e-8)

    def test_very_large_numbers(self):
        """Тест с очень большими числами"""
        coefficients = [[1e12, 2e12], [3e12, 4e12]]
        constants = [5e12, 6e12]

        result = solve_system_gaussian(coefficients, constants)

        # Проверяем решение
        for i in range(2):
            lhs = sum(coefficients[i][j] * result[j] for j in range(2))
            assert math.isclose(lhs, constants[i], rel_tol=1e-10)

class TestGaussianFloatPrecision:
    """Тесты с плавающей точкой"""

    def test_float_precision(self):
        """Тест точности с дробными числами"""
        coefficients = [[0.1, 0.2], [0.3, 0.4]]
        constants = [0.5, 0.6]

        result = solve_system_gaussian(coefficients, constants)

        # Проверяем решение
        for i in range(2):
            lhs = sum(coefficients[i][j] * result[j] for j in range(2))
            assert math.isclose(lhs, constants[i], abs_tol=1e-10)

    def test_repeated_solutions(self):
        """Тест многократного решения одинаковых систем"""
        coefficients = [[2, 1], [1, 3]]
        constants = [5, 10]
        expected = [1.0, 3.0]

        # Решаем несколько раз для проверки стабильности
        for _ in range(5):
            result = solve_system_gaussian(coefficients, constants)
            for i in range(2):
                assert math.isclose(result[i], expected[i], abs_tol=1e-10)


def test_gaussian_elimination_steps():
    """Тест, проверяющий корректность шагов метода Гаусса"""
    # Система, требующая перестановки строк
    coefficients = [[0, 1], [1, 0]]
    constants = [2, 1]

    result = solve_system_gaussian(coefficients, constants)
    expected = [1.0, 2.0]

    for i in range(2):
        assert math.isclose(result[i], expected[i], abs_tol=1e-10)
