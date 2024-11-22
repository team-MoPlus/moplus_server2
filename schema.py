from typing import List, Union
from pydantic import BaseModel

class Problem(BaseModel):
    problem_id: int
    practice_test_id: int
    problem_image_id: int
    point: int
    problem_number: str
    correct_rate: float
    problem_rating: str

    class Config:
        orm_mode = True

class ProblemImage(BaseModel):
    problem_image_id: int
    problem_id: int
    file_name: str
    image_file_extension: str
    image_key: str
    image_url: str

    class Config:
        orm_mode = True

class TestResult(BaseModel):
    test_result_id: int
    practice_test_id:int
    score: int
    solving_time: int
    deleted: bool
    created_at: str
    update_at: str

    class Config:
        orm_mode = True

    