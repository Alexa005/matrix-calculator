from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path

# Добавляем родительскую директорию в путь Python
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

try:
    from backend.matrix_core import (
        matrix_add,
        matrix_multiply,
        determinant_optimized as determinant,
        inverse,
        solve_system_gaussian
    )
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure backend/matrix_core.py exists and has the required functions")


    # Можно использовать заглушки для тестирования
    def matrix_add(a, b):
        raise ValueError("Backend module not available")


    def matrix_multiply(a, b):
        raise ValueError("Backend module not available")


    def determinant_optimized(matrix):
        raise ValueError("Backend module not available")


    def inverse(matrix):
        raise ValueError("Backend module not available")


    def solve_system_gaussian(coefficients, constants):
        raise ValueError("Backend module not available")


    determinant = determinant_optimized
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Модели запросов согласно договоренностям
class MatrixRequest(BaseModel):
    matrix: list[list[float]]

class TwoMatricesRequest(BaseModel):
    matrix_a: list[list[float]]
    matrix_b: list[list[float]]

class SLAERequest(BaseModel):
    coefficients: list[list[float]]
    constants: list[float]

@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Эндпоинт для определителя матрицы
@app.post("/determinant")
async def calculate_determinant(request: MatrixRequest):
    try:
        result = determinant(request.matrix)
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}


# Эндпоинт для сложения матриц
@app.post("/add")
async def add_matrices(request: TwoMatricesRequest):
    try:
        result = matrix_add(request.matrix_a, request.matrix_b)
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}


# Эндпоинт для умножения матриц
@app.post("/multiply")
async def multiply_matrices(request: TwoMatricesRequest):
    try:
        result = matrix_multiply(request.matrix_a, request.matrix_b)
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}


# Эндпоинт для обратной матрицы
@app.post("/inverse")
async def calculate_inverse(request: MatrixRequest):
    try:
        result = inverse(request.matrix)
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}


# Эндпоинт для решения СЛАУ
@app.post("/solve")
async def solve_system(request: SLAERequest):
    try:
        result = solve_system_gaussian(request.coefficients, request.constants)
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}


# Транспонирование
@app.post("/transpose")
async def transpose_matrix(request: MatrixRequest):
    try:
        from backend.matrix_core import transpose
        result = transpose(request.matrix)
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}

# Ранг
@app.post("/rank")
async def rank_matrix(request: MatrixRequest):
    try:
        from backend.matrix_core import rank
        result = rank(request.matrix)
        return {"result": result}
    except ValueError as e:
        return {"error": str(e)}


