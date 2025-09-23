from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.matrix_core import (
    matrix_add,
    matrix_multiply,
    determinant_optimized as determinant,
    inverse,
    solve_system_gaussian
)
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
