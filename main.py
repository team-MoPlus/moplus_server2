import io
from typing import Union, List
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from time import time
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import DetailResultApplication, PDFBody, TestResult
from models import TestResult
from pdfmain import create_review_note
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
import crud, models
import httpx
import asyncio
import os
from reportlab.pdfgen import canvas
from urllib.parse import quote


load_dotenv()

API_URL = os.getenv("API_URL")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.mopl.kr"],  # Next.js 앱 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Cache-Control"],
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
    return {"message": "Data received successfully", "response": test_result}

@app.post("/detailResultApplication")
async def get_detail_result_application_from_client(param: PDFBody):
    try:
        detail_result = param.test_result.model_dump()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Success"}


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
# @app.post("/request-review")
# async def request_review_note():
#     try:
#         # problem_info = crud.get_image(db, skip=0, limit=0)
#         await create_review_note()

#         return {"status": "OK"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    

# PDF 다운로드 엔드포인트
@app.post("/download-review")
async def download_review_note(data: PDFBody):
    buffer = io.BytesIO()
    return create_review_note(data.test_result, data.file_name, buffer)

    # headers = {
    #     "Content-Disposition": f"attachment; filename*=UTF-8''{data.file_name}",
    # }

    # return StreamingResponse(buffer, headers=headers, media_type="application/pdf")
