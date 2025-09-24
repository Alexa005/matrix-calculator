// script.js - Основная логика матричного калькулятора
class MatrixCalculatorUI {
    constructor() {
        this.currentOperation = 'determinant';
        this.rowsA = 2;
        this.colsA = 2;
        this.rowsB = 2;
        this.colsB = 2;

        this.initializeElements();
        this.setupEventListeners();
        this.init();
    }

    /**
     * Инициализация DOM элементов
     */
    initializeElements() {
        // Основные контейнеры
        this.operationButtons = document.querySelectorAll('.btn-operation');
        this.scalarInputSection = document.getElementById('scalar-input-section');
        this.matrixASection = document.getElementById('matrix-a-section');
        this.matrixBSection = document.getElementById('matrix-b-section');
        this.vectorBSection = document.getElementById('vector-b-section');

        // Элементы матрицы A
        this.decreaseRowsABtn = document.getElementById('decrease-rows-a');
        this.increaseRowsABtn = document.getElementById('increase-rows-a');
        this.decreaseColsABtn = document.getElementById('decrease-cols-a');
        this.increaseColsABtn = document.getElementById('increase-cols-a');
        this.rowsADisplay = document.getElementById('rows-a');
        this.colsADisplay = document.getElementById('cols-a');
        this.matrixAContainer = document.getElementById('matrix-a');

        // Элементы матрицы B
        this.decreaseRowsBBtn = document.getElementById('decrease-rows-b');
        this.increaseRowsBBtn = document.getElementById('increase-rows-b');
        this.decreaseColsBBtn = document.getElementById('decrease-cols-b');
        this.increaseColsBBtn = document.getElementById('increase-cols-b');
        this.rowsBDisplay = document.getElementById('rows-b');
        this.colsBDisplay = document.getElementById('cols-b');
        this.matrixBContainer = document.getElementById('matrix-b');

        // Вектор и скаляр
        this.vectorBContainer = document.getElementById('vector-b');
        this.scalarInput = document.getElementById('scalar-value');

        // Управление и отображение
        this.calculateButton = document.getElementById('calculate');
        this.resultContainer = document.getElementById('result');
        this.instructionText = document.getElementById('instruction-text');
        this.errorContainer = document.getElementById('errorContainer');
        this.errorContent = document.getElementById('errorContent');
    }

    /**
     * Настройка обработчиков событий
     */
    setupEventListeners() {
        // Обработчики операций
        this.operationButtons.forEach(btn => {
            btn.addEventListener('click', (e) => this.handleOperationChange(e));
        });

        // Обработчики изменения размеров матрицы A
        this.decreaseRowsABtn.addEventListener('click', () => this.updateMatrixSize('a', 'rows', -1));
        this.increaseRowsABtn.addEventListener('click', () => this.updateMatrixSize('a', 'rows', 1));
        this.decreaseColsABtn.addEventListener('click', () => this.updateMatrixSize('a', 'cols', -1));
        this.increaseColsABtn.addEventListener('click', () => this.updateMatrixSize('a', 'cols', 1));

        // Обработчики изменения размеров матрицы B
        this.decreaseRowsBBtn.addEventListener('click', () => this.updateMatrixSize('b', 'rows', -1));
        this.increaseRowsBBtn.addEventListener('click', () => this.updateMatrixSize('b', 'rows', 1));
        this.decreaseColsBBtn.addEventListener('click', () => this.updateMatrixSize('b', 'cols', -1));
        this.increaseColsBBtn.addEventListener('click', () => this.updateMatrixSize('b', 'cols', 1));

        // Основные обработчики
        this.calculateButton.addEventListener('click', () => this.calculate());
        this.scalarInput.addEventListener('input', () => this.validateScalarInput());

        // Валидация в реальном времени
        this.matrixAContainer.addEventListener('input', () => this.validateMatrixInput('a'));
        this.matrixBContainer.addEventListener('input', () => this.validateMatrixInput('b'));
        this.vectorBContainer.addEventListener('input', () => this.validateVectorInput());
    }

    /**
     * Инициализация приложения
     */
    async init() {
        this.generateMatrix('a', this.rowsA, this.colsA);
        this.updateUI();
        await this.checkServerStatus();
    }

    /**
     * Проверка статуса сервера
     */
    async checkServerStatus() {
        try {
            const isHealthy = await window.matrixAPI.healthCheck();
            if (!isHealthy) {
                this.showWarning('Сервер бэкенда не доступен. Убедитесь, что бэкенд запущен на localhost:8000');
            }
        } catch (error) {
            console.warn('Не удалось проверить статус сервера:', error);
        }
    }

    /**
     * Обработчик смены операции
     */
    handleOperationChange(event) {
        this.operationButtons.forEach(btn => btn.classList.remove('operation-active'));
        event.currentTarget.classList.add('operation-active');
        this.currentOperation = event.currentTarget.dataset.operation;
        this.updateUI();
    }

    /**
     * Обновление интерфейса
     */
    updateUI() {
        this.updateInstructionText();
        this.updateVisibleSections();
        this.adjustMatrixDimensions();
        this.validateOperation();
    }

    /**
     * Обновление текста инструкции
     */
    updateInstructionText() {
        const instructions = {
            'determinant': 'Введите значения квадратной матрицы для вычисления определителя.',
            'inverse': 'Введите значения квадратной матрицы для нахождения обратной матрицы.',
            'addition': 'Введите значения двух матриц одинакового размера для выполнения сложения.',
            'subtraction': 'Введите значения двух матриц одинакового размера для выполнения вычитания.',
            'multiplication': 'Введите значения двух матриц. Число столбцов матрицы A должно равняться числу строк матрицы B.',
            'scalar-multiplication': 'Введите матрицу и число для умножения.',
            'transpose': 'Введите матрицу для транспонирования.',
            'rank': 'Введите матрицу для нахождения её ранга.',
            'sle': 'Введите матрицу коэффициентов A и вектор значений B для решения системы линейных уравнений.'
        };

        this.instructionText.textContent = instructions[this.currentOperation] || 'Выберите операцию для продолжения.';
    }

    /**
     * Обновление видимых секций
     */
    updateVisibleSections() {
        // Скрываем все дополнительные секции
        [this.scalarInputSection, this.matrixBSection, this.vectorBSection]
            .forEach(section => section.classList.add('d-none'));

        // Показываем нужные секции
        if (['addition', 'subtraction', 'multiplication'].includes(this.currentOperation)) {
            this.matrixBSection.classList.remove('d-none');
        }

        if (this.currentOperation === 'scalar-multiplication') {
            this.scalarInputSection.classList.remove('d-none');
        }

        if (this.currentOperation === 'sle') {
            this.vectorBSection.classList.remove('d-none');
            this.updateVectorSize();
        }
    }

    /**
     * Корректировка размеров матриц
     */
    adjustMatrixDimensions() {
        if (['determinant', 'inverse'].includes(this.currentOperation)) {
            if (this.colsA !== this.rowsA) {
                this.colsA = this.rowsA;
                this.colsADisplay.textContent = this.colsA;
                this.generateMatrix('a', this.rowsA, this.colsA);
            }
        }

        if (this.currentOperation === 'multiplication' && this.colsA !== this.rowsB) {
            this.rowsB = this.colsA;
            this.rowsBDisplay.textContent = this.rowsB;
            this.generateMatrix('b', this.rowsB, this.colsB);
        }

        if (this.currentOperation === 'sle') {
            this.updateVectorSize();
        }
    }

    /**
     * Обновление размера матрицы
     */
    updateMatrixSize(matrix, dimension, change) {
        if (matrix === 'a') {
            if (dimension === 'rows') {
                this.rowsA = Math.max(1, Math.min(6, this.rowsA + change));
                this.rowsADisplay.textContent = this.rowsA;
            } else {
                this.colsA = Math.max(1, Math.min(6, this.colsA + change));
                this.colsADisplay.textContent = this.colsA;
            }
            this.generateMatrix('a', this.rowsA, this.colsA);
        } else {
            if (dimension === 'rows') {
                this.rowsB = Math.max(1, Math.min(6, this.rowsB + change));
                this.rowsBDisplay.textContent = this.rowsB;
            } else {
                this.colsB = Math.max(1, Math.min(6, this.colsB + change));
                this.colsBDisplay.textContent = this.colsB;
            }
            this.generateMatrix('b', this.rowsB, this.colsB);
        }

        this.validateOperation();
    }

    /**
     * Обновление размера вектора
     */
    updateVectorSize() {
        this.generateVector('b', this.rowsA);
    }

    /**
     * Генерация матрицы
     */
    generateMatrix(matrix, rows, cols) {
        const container = matrix === 'a' ? this.matrixAContainer : this.matrixBContainer;
        container.innerHTML = '';

        for (let i = 0; i < rows; i++) {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'matrix-row';

            for (let j = 0; j < cols; j++) {
                const input = document.createElement('input');
                input.type = 'number';
                input.className = 'matrix-input form-control';
                input.value = i === j ? '1' : '0';
                input.step = 'any';
                input.dataset.row = i;
                input.dataset.col = j;
                input.placeholder = '0';
                rowDiv.appendChild(input);
            }

            container.appendChild(rowDiv);
        }

        this.validateOperation();
    }

    /**
     * Генерация вектора
     */
    generateVector(vector, size) {
        this.vectorBContainer.innerHTML = '';

        for (let i = 0; i < size; i++) {
            const rowDiv = document.createElement('div');
            rowDiv.className = 'matrix-row';

            const input = document.createElement('input');
            input.type = 'number';
            input.className = 'matrix-input form-control';
            input.value = '0';
            input.step = 'any';
            input.dataset.index = i;
            input.placeholder = '0';
            rowDiv.appendChild(input);

            this.vectorBContainer.appendChild(rowDiv);
        }
    }

    /**
     * Получение значений матрицы
     */
    getMatrixValues(matrix) {
        const container = matrix === 'a' ? this.matrixAContainer : this.matrixBContainer;
        const inputs = container.querySelectorAll('input');
        const rows = container.children.length;
        const cols = rows > 0 ? container.children[0].children.length : 0;

        const matrixData = [];
        for (let i = 0; i < rows; i++) {
            matrixData[i] = [];
            for (let j = 0; j < cols; j++) {
                const input = container.querySelector(`input[data-row="${i}"][data-col="${j}"]`);
                const value = parseFloat(input.value);
                matrixData[i][j] = isNaN(value) ? 0 : value;
            }
        }

        return matrixData;
    }

    /**
     * Получение значений вектора
     */
    getVectorValues() {
        const inputs = this.vectorBContainer.querySelectorAll('input');
        return Array.from(inputs).map(input => {
            const value = parseFloat(input.value);
            return isNaN(value) ? 0 : value;
        });
    }

    /**
     * Валидация операций
     */
    validateOperation() {
        this.calculateButton.disabled = false;

        try {
            const matrixA = this.getMatrixValues('a');

            if (['addition', 'subtraction'].includes(this.currentOperation)) {
                const matrixB = this.getMatrixValues('b');
                if (matrixA.length !== matrixB.length || matrixA[0].length !== matrixB[0].length) {
                    throw new Error('Матрицы должны быть одинакового размера');
                }
            }

            if (this.currentOperation === 'multiplication') {
                const matrixB = this.getMatrixValues('b');
                if (matrixA[0].length !== matrixB.length) {
                    throw new Error('Число столбцов матрицы A должно равняться числу строк матрицы B');
                }
            }

            if (['determinant', 'inverse'].includes(this.currentOperation) && matrixA.length !== matrixA[0].length) {
                throw new Error('Матрица должна быть квадратной');
            }

        } catch (error) {
            this.calculateButton.disabled = true;
        }
    }

    /**
     * Валидация скалярного ввода
     */
    validateScalarInput() {
        const value = parseFloat(this.scalarInput.value);
        this.scalarInput.classList.toggle('is-invalid', isNaN(value));
        this.validateOperation();
    }

    /**
     * Валидация матрицы
     */
    validateMatrixInput(matrix) {
        const container = matrix === 'a' ? this.matrixAContainer : this.matrixBContainer;
        const inputs = container.querySelectorAll('input');

        let hasError = false;
        inputs.forEach(input => {
            const isValid = !input.value || !isNaN(parseFloat(input.value));
            input.classList.toggle('is-invalid', !isValid);
            if (!isValid) hasError = true;
        });

        this.validateOperation();
        return !hasError;
    }

    /**
     * Валидация вектора
     */
    validateVectorInput() {
        const inputs = this.vectorBContainer.querySelectorAll('input');
        let hasError = false;

        inputs.forEach(input => {
            const isValid = !input.value || !isNaN(parseFloat(input.value));
            input.classList.toggle('is-invalid', !isValid);
            if (!isValid) hasError = true;
        });

        this.validateOperation();
        return !hasError;
    }

    /**
     * Основная функция расчета
     */
    async calculate() {
        this.hideResults();
        this.setLoadingState(true);

        try {
            const matrixA = this.getMatrixValues('a');
            const matrixB = ['addition', 'subtraction', 'multiplication'].includes(this.currentOperation) ?
                this.getMatrixValues('b') : null;
            const vectorB = this.currentOperation === 'sle' ? this.getVectorValues() : null;
            const scalarValue = this.currentOperation === 'scalar-multiplication' ?
                parseFloat(this.scalarInput.value) || 1 : null;

            this.validateInputData(matrixA, matrixB, vectorB, scalarValue);

            let result;
            switch (this.currentOperation) {
                case 'determinant':
                    result = await window.matrixAPI.determinant(matrixA);
                    this.displayResult(`Определитель матрицы A = ${this.formatNumber(result)}`);
                    break;

                case 'inverse':
                    result = await window.matrixAPI.inverseMatrix(matrixA);
                    this.displayResult(`Обратная матрица A<sup>-1</sup>:`, this.formatMatrix(result));
                    break;

                case 'addition':
                    result = await window.matrixAPI.addMatrices(matrixA, matrixB);
                    this.displayResult('Результат сложения A + B:', this.formatMatrix(result));
                    break;

                case 'subtraction':
                    const negativeB = matrixB.map(row => row.map(val => -val));
                    result = await window.matrixAPI.addMatrices(matrixA, negativeB);
                    this.displayResult('Результат вычитания A - B:', this.formatMatrix(result));
                    break;

                case 'multiplication':
                    result = await window.matrixAPI.multiplyMatrices(matrixA, matrixB);
                    this.displayResult('Результат умножения A × B:', this.formatMatrix(result));
                    break;

                case 'transpose': {
                    result = await window.matrixAPI.transposeMatrix(matrixA);
                    this.displayResult("Транспонированная матрица:", this.formatMatrix(result));
                    break;
                }

                case 'rank': {
                    result = await window.matrixAPI.rankMatrix(matrixA);
                    this.displayResult("Ранг матрицы:", result);
                    break;
                }

                case 'sle':
                    result = await window.matrixAPI.solveSystem(matrixA, vectorB);
                    this.displayResult('Решение системы уравнений:', this.formatVector(result));
                    break;
            }

            this.saveToHistory(this.currentOperation, { matrixA, matrixB, vectorB, scalarValue }, result);

        } catch (error) {
            this.showError(error.message);
        } finally {
            this.setLoadingState(false);
        }
    }

    /**
     * Валидация входных данных
     */
    validateInputData(matrixA, matrixB, vectorB, scalarValue) {
        if (!matrixA || matrixA.length === 0) {
            throw new Error('Матрица A не может быть пустой');
        }

        if (this.currentOperation === 'scalar-multiplication' && isNaN(scalarValue)) {
            throw new Error('Введите корректное число для умножения');
        }
    }

    // === МЕТОДЫ ОТОБРАЖЕНИЯ ===

    displayResult(title, content = '') {
        this.resultContainer.innerHTML = `
            <div class="alert alert-success">
                <h5>${title}</h5>
                ${content ? `<pre class="mt-2">${content}</pre>` : ''}
            </div>
        `;
        this.resultContainer.style.display = 'block';
    }

    showError(message) {
        this.errorContent.textContent = message;
        this.errorContainer.style.display = 'block';
        this.hideResults();

        setTimeout(() => {
            this.errorContainer.style.display = 'none';
        }, 5000);
    }

    showWarning(message) {
        const warning = document.createElement('div');
        warning.className = 'alert alert-warning alert-dismissible fade show';
        warning.innerHTML = `
            <i class="bi bi-exclamation-triangle"></i> ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.querySelector('.calculator-container').insertBefore(warning, document.querySelector('.header'));
    }

    hideResults() {
        this.resultContainer.style.display = 'none';
        this.errorContainer.style.display = 'none';
    }

    setLoadingState(isLoading) {
        this.calculateButton.disabled = isLoading;
        this.calculateButton.innerHTML = isLoading
            ? '<div class="spinner-border spinner-border-sm" role="status"></div> Вычисление...'
            : '<i class="bi bi-calculator"></i> Вычислить';
    }

    // === ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ===

    formatNumber(num) {
        if (typeof num !== 'number') return num;
        return Math.abs(num) < 1e-10 ? '0' : num.toFixed(6).replace(/\.?0+$/, '');
    }

    formatMatrix(matrix) {
        return matrix.map(row =>
            row.map(val => this.formatNumber(val)).join('\t')
        ).join('\n');
    }

    formatVector(vector) {
        return vector.map((val, index) =>
            `x${index + 1} = ${this.formatNumber(val)}`
        ).join('\n');
    }

    calculateMatrixRank(matrix) {
        // Упрощенная реализация ранга
        return Math.min(matrix.length, matrix[0].length);
    }

    saveToHistory(operation, input, result) {
        try {
            const history = JSON.parse(localStorage.getItem('matrixHistory') || '[]');
            const historyItem = {
                operation,
                input,
                result,
                timestamp: new Date().toLocaleString('ru-RU')
            };

            history.unshift(historyItem);
            localStorage.setItem('matrixHistory', JSON.stringify(history.slice(0, 10)));
        } catch (error) {
            console.warn('Не удалось сохранить историю:', error);
        }
    }
}

// Запускаем приложение только после полной загрузки DOM
document.addEventListener("DOMContentLoaded", () => {
    const app = new MatrixCalculatorUI();

    // Безопасно навешиваем события (если элементы найдены)
    if (app.scalarNumerator) {
        app.scalarNumerator.addEventListener('input', () => app.validateScalarInput());
    }
    if (app.scalarDenominator) {
        app.scalarDenominator.addEventListener('input', () => app.validateScalarInput());
    }
});