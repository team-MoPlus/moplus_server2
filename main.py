from typing import Union, List
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi import FastAPI
from time import time
from fastapi.middleware.cors import CORSMiddleware


import httpx
import asyncio

from pdfmain import create_review_note

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


# 사진 다운로드
# @app.get("/image/{imageId}")
# async def get_image_by_id(photo_id: int, db: Session = Depends(get_db)):
#     find_photo: Photo = db.query(Photo).filter_by(photo_id=photo_id).first()
#     return FileResponse(find_photo.src)


# PDF 다운로드 엔드포인트
@app.get("/download-review")
async def download_review_note():
    await create_review_note()

    # PDF 파일 다운로드
    response = FileResponse(path="./output.pdf", filename='download_review.pdf', media_type="application/pdf")
    
    # 다운로드 완료 후 파일 삭제
    response.headers["Cache-Control"] = "no-cache"
    
    return response