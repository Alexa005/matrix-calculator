// api.js - Клиент для работы с API матричного калькулятора
class MatrixAPIClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
        this.timeout = 10000; // 10 секунд таймаут
    }

    /**
     * Универсальная функция для отправки запросов к API
     */
    async _request(endpoint, data) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        try {
            const response = await fetch(`${this.baseURL}/${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
                signal: controller.signal
            });

            clearTimeout(timeoutId);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();

            if (result.error) {
                throw new Error(result.error);
            }

            return result.result;

        } catch (error) {
            clearTimeout(timeoutId);
            
            if (error.name === 'AbortError') {
                throw new Error('Превышено время ожидания ответа от сервера');
            }
            
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error('Не удалось подключиться к серверу. Проверьте, запущен ли бэкенд на localhost:8000');
            }
            
            throw error;
        }
    }

    /**
     * Проверка здоровья сервера
     */
    async healthCheck() {
        try {
            const response = await fetch(`${this.baseURL}/health`);
            const data = await response.json();
            return data.status === 'ok';
        } catch (error) {
            return false;
        }
    }

    /**
     * Вычисление определителя матрицы
     */
    async determinant(matrix) {
        this._validateMatrix(matrix, 'determinant');
        return await this._request('determinant', { matrix });
    }

    /**
     * Сложение двух матриц
     */
    async addMatrices(matrixA, matrixB) {
        this._validateMatrix(matrixA, 'addition');
        this._validateMatrix(matrixB, 'addition');
        
        if (matrixA.length !== matrixB.length || matrixA[0].length !== matrixB[0].length) {
            throw new Error('Матрицы должны быть одинакового размера для сложения');
        }

        return await this._request('add', { 
            matrix_a: matrixA, 
            matrix_b: matrixB 
        });
    }

    /**
     * Умножение двух матриц
     */
    async multiplyMatrices(matrixA, matrixB) {
        this._validateMatrix(matrixA, 'multiplication');
        this._validateMatrix(matrixB, 'multiplication');
        
        if (matrixA[0].length !== matrixB.length) {
            throw new Error('Число столбцов матрицы A должно равняться числу строк матрицы B');
        }

        return await this._request('multiply', { 
            matrix_a: matrixA, 
            matrix_b: matrixB 
        });
    }

    /**
     * Нахождение обратной матрицы
     */
    async inverseMatrix(matrix) {
        this._validateMatrix(matrix, 'inverse');
        
        if (matrix.length !== matrix[0].length) {
            throw new Error('Матрица должна быть квадратной для нахождения обратной матрицы');
        }

        return await this._request('inverse', { matrix });
    }

    /**
     * Решение системы линейных уравнений
     */
    async solveSystem(coefficients, constants) {
        this._validateMatrix(coefficients, 'sle');
        this._validateVector(constants, 'sle');
        
        if (coefficients.length !== constants.length) {
            throw new Error('Количество уравнений должно совпадать с количеством свободных членов');
        }

        return await this._request('solve', { 
            coefficients, 
            constants 
        });
    }

    async transposeMatrix(matrix) {
        this._validateMatrix(matrix, 'transpose');
        return await this._request('transpose', { matrix });
    }

    async rankMatrix(matrix) {
        this._validateMatrix(matrix, 'rank');
        return await this._request('rank', { matrix });
    }



    /**
     * Валидация матрицы
     */
    _validateMatrix(matrix, operation) {
        if (!Array.isArray(matrix) || matrix.length === 0) {
            throw new Error('Матрица должна быть непустым двумерным массивом');
        }

        const rows = matrix.length;
        const cols = matrix[0].length;

        if (!Array.isArray(matrix[0]) || cols === 0) {
            throw new Error('Матрица должна содержать непустые строки');
        }

        // Проверяем что все строки одинаковой длины
        for (let i = 1; i < rows; i++) {
            if (!Array.isArray(matrix[i]) || matrix[i].length !== cols) {
                throw new Error('Все строки матрицы должны иметь одинаковую длину');
            }
        }

        // Проверяем что все элементы - числа
        for (let i = 0; i < rows; i++) {
            for (let j = 0; j < cols; j++) {
                if (typeof matrix[i][j] !== 'number' || !isFinite(matrix[i][j])) {
                    throw new Error('Все элементы матрицы должны быть конечными числами');
                }
            }
        }

        // Специфичные проверки для операций
        if ((operation === 'determinant' || operation === 'inverse') && rows !== cols) {
            throw new Error('Матрица должна быть квадратной для этой операции');
        }
    }

    /**
     * Валидация вектора
     */
    _validateVector(vector, operation) {
        if (!Array.isArray(vector) || vector.length === 0) {
            throw new Error('Вектор должен быть непустым массивом');
        }

        for (let i = 0; i < vector.length; i++) {
            if (typeof vector[i] !== 'number' || !isFinite(vector[i])) {
                throw new Error('Все элементы вектора должны быть конечными числами');
            }
        }
    }
}

// Создаем глобальный экземпляр API
window.matrixAPI = new MatrixAPIClient();