import io
from fastapi import FastAPI, HTTPException
from time import time
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import DetailResultApplication, PDFBody, TestResult
from models import TestResult
from pdfmain import create_review_note
from fastapi import FastAPI, Depends, HTTPException
import httpx
import asyncio
import os


load_dotenv()

API_URL = os.getenv("API_URL")

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://www.mopl.kr"],  # Next.js 앱 주소
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # Dependency Injection 
# def get_db():
#     db = SessionLocal()
#     try : 
#         yield db
#     finally:
#         db.close()

async def requestPracticeTests(client):
    response = await client.get(f"{API_URL}/practiceTests/2")
    return response.text


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

    

# PDF 다운로드 엔드포인트
@app.post("/download-review")
async def download_review_note(data: PDFBody):
    buffer = io.BytesIO()
    return create_review_note(data.test_result, data.file_name, buffer)
