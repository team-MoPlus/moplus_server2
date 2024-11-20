from typing import Union, List
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from time import time
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import DetailResultApplication, TestResult
from pdfmain import create_review_note
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import crud, models
import httpx
import asyncio
import os

load_dotenv()

API_URL = os.getenv("API_URL")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.mopl.kr"],  # Next.js 앱 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency Injection 
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()

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

@app.post("/detailResultApplication")
async def get_detail_result_application_from_client(detail_result: DetailResultApplication):
    try:
        detail_result = detail_result.model_dump()
        await create_review_note(detail_result)

        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test/rating/{practiceTestId}", tags=["test"])
async def get_rating(practiceTestId: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/rating/{practiceTestId}")
    return response.text


@app.get("/image-url")
def get_image_url(problem_id: int, db:Session=Depends(get_db)):
    problem_image_info = crud.get_image(db, problem_id)
    return problem_image_info.image_url

# 복습표 생성 요청
@app.post("/request-review")
async def request_review_note():
    try:
        # problem_info = crud.get_image(db, skip=0, limit=0)
        await create_review_note()

        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# PDF 다운로드 엔드포인트
@app.get("/download-review")
async def download_review_note():
    
    # PDF 파일 다운로드
    response = FileResponse(path="./output.pdf", filename='download_review.pdf', media_type="application/pdf")
    
    # 다운로드 완료 후 파일 삭제
    response.headers["Cache-Control"] = "no-cache"
    
    return response
