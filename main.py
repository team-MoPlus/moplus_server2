from typing import Union, List
from pydantic import BaseModel
from fastapi import FastAPI
from time import time
from fastapi.middleware.cors import CORSMiddleware


import httpx
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.mopl.kr"],  # Next.js 앱 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://dev.mopl.kr/api/v1"


class IncorrectProblem(BaseModel):
    problemNumber: str
    correctRate: float

class TestResult(BaseModel):
    id: int
    score: int
    solvingTime: str
    averageSolvingTime: str
    estimatedRating: int
    incorrectProblems: List[IncorrectProblem]

async def requestPracticeTests(client):
    response = await client.get(f"{API_URL}/practiceTests/2")
    return response.text

# async def requestRating(client, practiceTestId):
#     response = await client.get(f"{API_URL}/rating/{practiceTestId}")
#     return response.text

async def task():
    async with httpx.AsyncClient() as client:
        tasks = [requestPracticeTests(client) for i in range(100)]
        result = await asyncio.gather(*tasks)
        print(result)


@app.get("/", tags=["root"])
async def read_root():
    # start = time()
    # await task()
    # print("time: ", time() - start)
    return 'Hello'
    

@app.post("/test/resultInfo")
async def get_result_info_from_client(test_result: TestResult):
    return {"message": "Data received successfully"}


@app.get("/test/rating/{practiceTestId}", tags=["test"])
async def get_rating(practiceTestId: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/rating/{practiceTestId}")
    return response.text
