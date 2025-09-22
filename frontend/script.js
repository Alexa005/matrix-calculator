document.addEventListener('DOMContentLoaded', function () {
    // Элементы DOM
    const operationButtons = document.querySelectorAll('.btn-operation');
    const scalarInputSection = document.getElementById('scalar-input-section');
    const matrixASection = document.getElementById('matrix-a-section');
    const matrixBSection = document.getElementById('matrix-b-section');
    const vectorBSection = document.getElementById('vector-b-section');

    // Кнопки изменения размера матрицы A
    const decreaseRowsABtn = document.getElementById('decrease-rows-a');
    const increaseRowsABtn = document.getElementById('increase-rows-a');
    const decreaseColsABtn = document.getElementById('decrease-cols-a');
    const increaseColsABtn = document.getElementById('increase-cols-a');
    const rowsADisplay = document.getElementById('rows-a');
    const colsADisplay = document.getElementById('cols-a');

    // Кнопки изменения размера матрицы B
    const decreaseRowsBBtn = document.getElementById('decrease-rows-b');
    const increaseRowsBBtn = document.getElementById('increase-rows-b');
    const decreaseColsBBtn = document.getElementById('decrease-cols-b');
    const increaseColsBBtn = document.getElementById('increase-cols-b');
    const rowsBDisplay = document.getElementById('rows-b');
    const colsBDisplay = document.getElementById('cols-b');

    const matrixAContainer = document.getElementById('matrix-a');
    const matrixBContainer = document.getElementById('matrix-b');
    const vectorBContainer = document.getElementById('vector-b');
    const calculateButton = document.getElementById('calculate');
    const resultContainer = document.getElementById('result');
    const instructionText = document.getElementById('instruction-text');
    const scalarInput = document.getElementById('scalar-value');

    // Текущие настройки
    let currentOperation = 'determinant';
    let rowsA = 2, colsA = 2;
    let rowsB = 2, colsB = 2;

    // Инициализация
    generateMatrix('a', rowsA, colsA);
    updateOperationUI();

    // Обработчики событий
    operationButtons.forEach(button => {
        button.addEventListener('click', function () {
            operationButtons.forEach(btn => btn.classList.remove('operation-active'));
            this.classList.add('operation-active');
            currentOperation = this.dataset.operation;
            updateOperationUI();
        });
    });

    // Обработчики для изменения размера матрицы A
    decreaseRowsABtn.addEventListener('click', () => updateMatrixSize('a', 'rows', -1));
    increaseRowsABtn.addEventListener('click', () => updateMatrixSize('a', 'rows', 1));
    decreaseColsABtn.addEventListener('click', () => updateMatrixSize('a', 'cols', -1));
    increaseColsABtn.addEventListener('click', () => updateMatrixSize('a', 'cols', 1));

    // Обработчики для изменения размера матрицы B
    decreaseRowsBBtn.addEventListener('click', () => updateMatrixSize('b', 'rows', -1));
    increaseRowsBBtn.addEventListener('click', () => updateMatrixSize('b', 'rows', 1));
    decreaseColsBBtn.addEventListener('click', () => updateMatrixSize('b', 'cols', -1));
    increaseColsBBtn.addEventListener('click', () => updateMatrixSize('b', 'cols', 1));

    calculateButton.addEventListener('click', calculate);

    // Функция для преобразования строки в число (поддерживает дроби)
    function parseNumber(input) {
        if (!input) return 0;

        // Удаляем пробелы
        input = input.trim();

        // Проверяем, является ли ввод дробью
        if (input.includes('/')) {
            const parts = input.split('/');
            if (parts.length === 2) {
                const numerator = parseFloat(parts[0]);
                const denominator = parseFloat(parts[1]);
                if (denominator !== 0 && !isNaN(numerator) && !isNaN(denominator)) {
                    return numerator / denominator;
                }
            }
        }

        // Пробуем преобразовать в число
        const result = parseFloat(input);
        return isNaN(result) ? 0 : result;
    }

    // Функции
    function updateOperationUI() {
        // Обновляем инструкцию
        switch (currentOperation) {
            case 'determinant':
                instructionText.textContent = 'Введите значения квадратной матрицы для вычисления определителя.';
                break;
            case 'inverse':
                instructionText.textContent = 'Введите значения квадратной матрицы для нахождения обратной матрицы.';
                break;
            case 'addition':
                instructionText.textContent = 'Введите значения двух матриц одинакового размера для выполнения сложения.';
                break;
            case 'subtraction':
                instructionText.textContent = 'Введите значения двух матриц одинакового размера для выполнения вычитания.';
                break;
            case 'multiplication':
                instructionText.textContent = 'Введите значения двух матриц. Число столбцов матрицы A должно равняться числу строк матрицы B.';
                break;
            case 'scalar-multiplication':
                instructionText.textContent = 'Введите матрицу и число для умножения. Можно использовать дроби (1/2) и десятичные числа (0.5).';
                break;
            case 'transpose':
                instructionText.textContent = 'Введите матрицу для транспонирования.';
                break;
            case 'rank':
                instructionText.textContent = 'Введите матрицу для нахождения её ранга.';
                break;
            case 'sle':
                instructionText.textContent = 'Введите матрицу коэффициентов A и вектор значений B для решения системы линейных уравнений.';
                break;
        }

        // Показываем/скрываем секции в зависимости от операции
        scalarInputSection.classList.add('d-none');
        matrixBSection.classList.add('d-none');
        vectorBSection.classList.add('d-none');

        if (currentOperation === 'addition' || currentOperation === 'subtraction' || currentOperation === 'multiplication') {
            matrixBSection.classList.remove('d-none');
            updateMatrixSize('b', 'rows', 0); // Обновляем без изменения размера
            updateMatrixSize('b', 'cols', 0); // Обновляем без изменения размера
        }

        if (currentOperation === 'scalar-multiplication') {
            scalarInputSection.classList.remove('d-none');
        }

        if (currentOperation === 'sle') {
            vectorBSection.classList.remove('d-none');
            updateVectorSize();
        }

        // Для операций с квадратными матрицами ограничиваем размер
        if (currentOperation === 'determinant' || currentOperation === 'inverse') {
            colsADisplay.textContent = rowsA;
            colsA = rowsA;
            generateMatrix('a', rowsA, colsA);
        }
    }

    function updateMatrixSize(matrix, dimension, change) {
        if (matrix === 'a') {
            if (dimension === 'rows') {
                rowsA = Math.max(1, Math.min(6, rowsA + change));
                rowsADisplay.textContent = rowsA;

                // Для квадратных матриц обновляем также столбцы
                if (currentOperation === 'determinant' || currentOperation === 'inverse') {
                    colsA = rowsA;
                    colsADisplay.textContent = colsA;
                }
            } else if (dimension === 'cols') {
                colsA = Math.max(1, Math.min(6, colsA + change));
                colsADisplay.textContent = colsA;
            }
            generateMatrix('a', rowsA, colsA);
        } else if (matrix === 'b') {
            if (dimension === 'rows') {
                rowsB = Math.max(1, Math.min(6, rowsB + change));
                rowsBDisplay.textContent = rowsB;
            } else if (dimension === 'cols') {
                colsB = Math.max(1, Math.min(6, colsB + change));
                colsBDisplay.textContent = colsB;
            }
            generateMatrix('b', rowsB, colsB);
        }
    }

    function updateVectorSize() {
        generateVector('b', rowsA);
    }

    function generateMatrix(matrix, rows, cols) {
        const container = matrix === 'a' ? matrixAContainer : matrixBContainer;
        container.innerHTML = '';

        for (let i = 0; i < rows; i++) {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'matrix-row';

            for (let j = 0; j < cols; j++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'matrix-input form-control';
                input.value = i === j ? '1' : '0';
                input.step = 'any'; // Разрешаем ввод дробей
                input.dataset.row = i;
                input.dataset.col = j;
                rowDiv.appendChild(input);
            }

            container.appendChild(rowDiv);
        }
    }

    function generateVector(vector, size) {
        const container = vectorBContainer;
        container.innerHTML = '';

        for (let i = 0; i < size; i++) {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'matrix-row';

            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'matrix-input form-control';
            input.value = '0';
            input.step = 'any'; // Разрешаем ввод дробей
            input.dataset.index = i;
            rowDiv.appendChild(input);

            container.appendChild(rowDiv);
        }
    }

    function getMatrixValues(matrix) {
        const container = matrix === 'a' ? matrixAContainer : matrixBContainer;
        const inputs = container.querySelectorAll('input');
        const rows = container.children.length;
        const cols = rows > 0 ? container.children[0].children.length : 0;

        const matrixData = [];
        for (let i = 0; i < rows; i++) {
            matrixData[i] = [];
            for (let j = 0; j < cols; j++) {
                const input = container.querySelector(`input[data-row="${i}"][data-col="${j}"]`);
                matrixData[i][j] = parseNumber(input.value);
            }
        }

        return matrixData;
    }

    function getVectorValues() {
        const inputs = vectorBContainer.querySelectorAll('input');
        const vectorData = [];

        for (let i = 0; i < inputs.length; i++) {
            vectorData.push(parseNumber(inputs[i].value));
        }

        return vectorData;
    }

    function calculate() {
        const matrixA = getMatrixValues('a');
        const matrixB = ['addition', 'subtraction', 'multiplication'].includes(currentOperation) ? getMatrixValues('b') : null;
        const vectorB = currentOperation === 'sle' ? getVectorValues() : null;
        const scalarValue = currentOperation === 'scalar-multiplication' ? parseNumber(scalarInput.value) : null;

        // Здесь будет вызов API к бэкенду
        // Временно просто отображаем результат с помощью функций-заглушек

        let resultHTML = '';

        switch (currentOperation) {
            case 'determinant':
                resultHTML = `<p>Определитель матрицы A:</p><h3>${simulateDeterminant(matrixA)}</h3>`;
                break;
            case 'inverse':
                resultHTML = `<p>Обратная матрица A<sup>-1</sup>:</p><pre>${formatMatrix(simulateInverse(matrixA))}</pre>`;
                break;
            case 'addition':
                resultHTML = `<p>Результат сложения матриц A + B:</p><pre>${formatMatrix(simulateAddition(matrixA, matrixB))}</pre>`;
                break;
            case 'subtraction':
                resultHTML = `<p>Результат вычитания матриц A - B:</p><pre>${formatMatrix(simulateSubtraction(matrixA, matrixB))}</pre>`;
                break;
            case 'multiplication':
                resultHTML = `<p>Результат умножения матриц A × B:</p><pre>${formatMatrix(simulateMultiplication(matrixA, matrixB))}</pre>`;
                break;
            case 'scalar-multiplication':
                resultHTML = `<p>Результат умножения матрицы A на ${scalarInput.value}:</p><pre>${formatMatrix(simulateScalarMultiplication(matrixA, scalarValue))}</pre>`;
                break;
            case 'transpose':
                resultHTML = `<p>Транспонированная матрица A<sup>T</sup>:</p><pre>${formatMatrix(simulateTranspose(matrixA))}</pre>`;
                break;
            case 'rank':
                resultHTML = `<p>Ранг матрицы A:</p><h3>${simulateRank(matrixA)}</h3>`;
                break;
            case 'sle':
                resultHTML = `<p>Решение СЛАУ:</p><pre>${formatVector(simulateSLE(matrixA, vectorB))}</pre>`;
                break;
        }

        resultContainer.innerHTML = resultHTML;

        // В реальном приложении здесь будет fetch запрос к API
    }

    // Функции-заглушки для имитации вычислений
    function simulateDeterminant(matrix) {
        // Заглушка для вычисления определителя
        if (matrix.length === 2 && matrix[0].length === 2) {
            return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]).toFixed(4);
        }
        return "Для демонстрации";
    }

    function simulateInverse(matrix) {
        // Заглушка для обратной матрицы
        if (matrix.length === 2 && matrix[0].length === 2) {
            const det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0];
            if (det === 0) return "Матрица вырождена";

            return [
                [matrix[1][1] / det, -matrix[0][1] / det],
                [-matrix[1][0] / det, matrix[0][0] / det]
            ];
        }
        return [[1, 0], [0, 1]]; // Заглушка для матриц большего размера
    }

    function simulateAddition(matrixA, matrixB) {
        // Заглушка для сложения матриц
        const result = [];
        for (let i = 0; i < matrixA.length; i++) {
            result[i] = [];
            for (let j = 0; j < matrixA[i].length; j++) {
                result[i][j] = matrixA[i][j] + matrixB[i][j];
            }
        }
        return result;
    }

    function simulateSubtraction(matrixA, matrixB) {
        // Заглушка для вычитания матриц
        const result = [];
        for (let i = 0; i < matrixA.length; i++) {
            result[i] = [];
            for (let j = 0; j < matrixA[i].length; j++) {
                result[i][j] = matrixA[i][j] - matrixB[i][j];
            }
        }
        return result;
    }

    function simulateMultiplication(matrixA, matrixB) {
        // Заглушка для умножения матриц
        const result = [];
        for (let i = 0; i < matrixA.length; i++) {
            result[i] = [];
            for (let j = 0; j < matrixB[0].length; j++) {
                result[i][j] = 0;
                for (let k = 0; k < matrixA[0].length; k++) {
                    result[i][j] += matrixA[i][k] * matrixB[k][j];
                }
            }
        }
        return result;
    }

    function simulateScalarMultiplication(matrix, scalar) {
        // Заглушка для умножения матрицы на число
        const result = [];
        for (let i = 0; i < matrix.length; i++) {
            result[i] = [];
            for (let j = 0; j < matrix[i].length; j++) {
                result[i][j] = matrix[i][j] * scalar;
            }
        }
        return result;
    }

    function simulateTranspose(matrix) {
        // Заглушка для транспонирования матрицы
        const result = [];
        for (let j = 0; j < matrix[0].length; j++) {
            result[j] = [];
            for (let i = 0; i < matrix.length; i++) {
                result[j][i] = matrix[i][j];
            }
        }
        return result;
    }

    function simulateRank(matrix) {
        // Заглушка для нахождения ранга матрицы
        return Math.min(matrix.length, matrix[0].length);
    }

    function simulateSLE(matrixA, vectorB) {
        // Заглушка для решения СЛАУ
        const result = [];
        for (let i = 0; i < vectorB.length; i++) {
            result.push((vectorB[i] / matrixA[i][i]).toFixed(4));
        }
        return result;
    }

    function formatMatrix(matrix) {
        if (typeof matrix === 'string') return matrix;

        return matrix.map(row =>
            row.map(val => typeof val === 'number' ? val.toFixed(4) : val).join('\t')
        ).join('\n');
    }

    function formatVector(vector) {
        return vector.map(val => typeof val === 'number' ? val.toFixed(4) : val).join('\n');
    }
});